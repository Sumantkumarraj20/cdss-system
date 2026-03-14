"use client";

import { addRxPlugin, createRxDatabase, RxCollection, RxDatabase } from "rxdb";
import { getRxStorageDexie } from "rxdb/plugins/storage-dexie";
import { RxDBLeaderElectionPlugin } from "rxdb/plugins/leader-election";
import { RxDBUpdatePlugin } from "rxdb/plugins/update";
import { replicateRxCollection, RxReplicationState } from "rxdb/plugins/replication";

import {
  collections,
  DrugDoc,
  DiagnosisDoc,
  PresentationDoc,
  SymptomDoc,
} from "./schema";

const DB_NAME = "cdss-local";
const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";
const tokenKey = "cdss_token";

const authHeaders = () => {
  if (typeof window === "undefined") return {};
  const token = localStorage.getItem(tokenKey);
  return token ? { Authorization: `Bearer ${token}` } : {};
};

type AppCollections = {
  drugs: RxCollection<DrugDoc>;
  diagnoses: RxCollection<DiagnosisDoc>;
  presentations: RxCollection<PresentationDoc>;
  symptoms: RxCollection<SymptomDoc>;
};

export type AppDatabase = RxDatabase<AppCollections>;

let dbPromise: Promise<AppDatabase> | null = null;

function initPlugins() {
  addRxPlugin(RxDBUpdatePlugin);
  addRxPlugin(RxDBLeaderElectionPlugin);
}

async function createDb() {
  if (typeof window === "undefined") {
    throw new Error("RxDB can only be created in the browser");
  }

  initPlugins();

  const db = await createRxDatabase<AppCollections>({
    name: DB_NAME,
    eventReduce: true,
    multiInstance: true,
    storage: getRxStorageDexie(),
  });

  await db.addCollections(collections as any);
  return db;
}

export async function getDb() {
  if (!dbPromise) {
    dbPromise = createDb();
  }
  return dbPromise;
}

type Replications = {
  drugs: RxReplicationState<DrugDoc, unknown>;
  diagnoses: RxReplicationState<DiagnosisDoc, unknown>;
  presentations: RxReplicationState<PresentationDoc, unknown>;
};

async function replicateCollection<T, C = unknown>(
  collection: RxCollection<T>,
  endpoint: string
): Promise<RxReplicationState<T, C>> {
  return replicateRxCollection<T, C>({
    collection,
    replicationIdentifier: `sync-${endpoint}`,
    live: true,
    retryTime: 10_000,
    autoStart: true,
    pull: {
      async handler(lastCheckpoint: C | null | undefined, batchSize: number) {
        const res = await fetch(
          `${API_BASE}/sync/${endpoint}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              ...authHeaders(),
            } as Record<string, string>,
            body: JSON.stringify({
              checkpoint: lastCheckpoint,
              limit: batchSize,
            }),
          }
        );
        if (!res.ok) {
          throw new Error(`Pull ${endpoint} failed: ${res.status}`);
        }
        const data = await res.json();
        const checkpoint = (data.checkpoint as C | undefined) ?? (lastCheckpoint ?? undefined);
        return {
          documents: data.documents ?? [],
          checkpoint,
        };
      },
      batchSize: 50,
    },
    push: {
      async handler(rows: any[]) {
        const res = await fetch(
          `${API_BASE}/sync/${endpoint}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              ...authHeaders(),
            } as Record<string, string>,
            body: JSON.stringify({ documents: rows }),
          }
        );
        if (!res.ok) {
          throw new Error(`Push ${endpoint} failed: ${res.status}`);
        }
        return [];
      },
      batchSize: 50,
    },
  });
}

export async function startReplications(): Promise<Replications> {
  const db = await getDb();
  return {
    drugs: await replicateCollection(db.drugs, "drugs"),
    diagnoses: await replicateCollection(db.diagnoses, "diagnoses"),
    presentations: await replicateCollection(db.presentations, "presentations"),
  };
}
