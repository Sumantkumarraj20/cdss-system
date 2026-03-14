"use client";

import Link from "next/link";
import { useState } from "react";
import { api, setAuthToken } from "@/lib/api";

export default function AdminHome() {
  const [token, setToken] = useState("");
  const [status, setStatus] = useState<"idle" | "ok" | "error">("idle");

  const handleSave = async () => {
    try {
      const res = await api.post("/auth/login", { token });
      setAuthToken(res.data.access_token || token);
      setStatus("ok");
    } catch {
      setStatus("error");
    }
  };

  return (
    <div className="space-y-10">
      {/* Page Header */}
      <section>
        <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
          Admin Console
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
          Manage clinical knowledge resources used by the CDSS engine.
        </p>
      </section>

      {/* Token Card */}
      <section className="max-w-xl bg-white dark:bg-slate-900 border dark:border-slate-800 rounded-lg p-5 space-y-4">
        <div>
          <h2 className="text-sm font-medium text-slate-800 dark:text-slate-200">
            Authentication Token
          </h2>
          <p className="text-xs text-slate-500">
            Paste your admin API token to enable editing.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <input
            className="border dark:border-slate-700 rounded-md px-3 py-2 w-full text-sm bg-white dark:bg-slate-950"
            placeholder="CDSS_API_TOKEN"
            value={token}
            onChange={(e) => setToken(e.target.value)}
          />

          <button
            onClick={handleSave}
            className="px-4 py-2 rounded-md bg-slate-900 text-white hover:bg-slate-800 text-sm"
          >
            Save
          </button>
        </div>

        {status === "ok" && (
          <p className="text-green-600 text-xs">Token saved successfully.</p>
        )}

        {status === "error" && (
          <p className="text-red-600 text-xs">Invalid token.</p>
        )}
      </section>

      {/* Knowledge Management */}
      <section className="space-y-3">
        <h2 className="text-sm font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">
          Knowledge Modules
        </h2>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <Link
            href="/admin/drugs"
            className="border dark:border-slate-800 bg-white dark:bg-slate-900 rounded-lg p-5 hover:border-blue-500 transition"
          >
            <h3 className="font-medium text-slate-900 dark:text-slate-100">
              Drugs
            </h3>
            <p className="text-xs text-slate-500 mt-1">
              Manage medication database used by CDSS.
            </p>
          </Link>

          <Link
            href="/admin/diagnoses"
            className="border dark:border-slate-800 bg-white dark:bg-slate-900 rounded-lg p-5 hover:border-blue-500 transition"
          >
            <h3 className="font-medium text-slate-900 dark:text-slate-100">
              Diagnoses
            </h3>
            <p className="text-xs text-slate-500 mt-1">
              Maintain disease and condition knowledge base.
            </p>
          </Link>

          <Link
            href="/admin/presentations"
            className="border dark:border-slate-800 bg-white dark:bg-slate-900 rounded-lg p-5 hover:border-blue-500 transition"
          >
            <h3 className="font-medium text-slate-900 dark:text-slate-100">
              Presentations
            </h3>
            <p className="text-xs text-slate-500 mt-1">
              Manage symptom and presentation logic.
            </p>
          </Link>
        </div>
      </section>
    </div>
  );
}
