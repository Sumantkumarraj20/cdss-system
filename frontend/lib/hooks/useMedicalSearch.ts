"use client";

import { useMemo, useState, useEffect } from "react";
import Fuse from "fuse.js";
import type { IFuseOptions } from "fuse.js";

import { getDb } from "../db";
import { DrugDoc, DiagnosisDoc, PresentationDoc, SymptomDoc } from "../schema";

type GroupedResults = {
  drugs: DrugDoc[];
  diagnoses: DiagnosisDoc[];
  presentations: PresentationDoc[];
  symptoms: SymptomDoc[];
};

const fuseOptions: IFuseOptions<any> = {
  includeScore: true,
  threshold: 0.3,
  keys: ["name", "generic_name", "summary", "description"],
};

async function loadDocs() {
  const db = await getDb();
  const [drugs, diagnoses, presentations, symptoms] = await Promise.all([
    db.drugs.find().exec(),
    db.diagnoses.find().exec(),
    db.presentations.find().exec(),
    db.symptoms.find().exec(),
  ]);
  return {
    drugs: drugs.map((d) => d.toJSON()) as DrugDoc[],
    diagnoses: diagnoses.map((d) => d.toJSON()) as DiagnosisDoc[],
    presentations: presentations.map((d) => d.toJSON()) as PresentationDoc[],
    symptoms: symptoms.map((d) => d.toJSON()) as SymptomDoc[],
  };
}

export function useMedicalSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<GroupedResults>({
    drugs: [],
    diagnoses: [],
    presentations: [],
    symptoms: [],
  });

  const [fuse, setFuse] = useState<Fuse<any> | null>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    let active = true;
    loadDocs().then((data) => {
      if (!active) return;
      const combined = [
        ...data.drugs.map((d) => ({ ...d, __type: "drugs" })),
        ...data.diagnoses.map((d) => ({ ...d, __type: "diagnoses" })),
        ...data.presentations.map((d) => ({ ...d, __type: "presentations" })),
        ...data.symptoms.map((d) => ({ ...d, __type: "symptoms" })),
      ];
      setFuse(new Fuse(combined, fuseOptions));
      setLoaded(true);
    });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (!fuse || !query.trim()) {
      setResults({ drugs: [], diagnoses: [], presentations: [], symptoms: [] });
      return;
    }
    const start = performance.now();
    const hits = fuse.search(query).slice(0, 50);
    const grouped: GroupedResults = {
      drugs: [],
      diagnoses: [],
      presentations: [],
      symptoms: [],
    };
    hits.forEach(({ item }) => {
      const { __type, ...doc } = item;
      if (grouped[__type as keyof GroupedResults]) {
        // @ts-ignore
        grouped[__type].push(doc);
      }
    });
    const duration = performance.now() - start;
    if (duration > 20) {
      console.warn(`Search took ${duration.toFixed(2)}ms > 20ms target`);
    }
    setResults(grouped);
  }, [query, fuse]);

  return useMemo(
    () => ({
      query,
      setQuery,
      results,
      ready: Boolean(fuse),
      loaded,
    }),
    [query, results, fuse, loaded]
  );
}
