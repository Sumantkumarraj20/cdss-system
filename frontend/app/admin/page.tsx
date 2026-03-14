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
      setAuthToken(res.data.token);
      setStatus("ok");
    } catch {
      setStatus("error");
    }
  };

  return (
    <main className="p-8 space-y-6">
      <h1 className="text-3xl font-semibold">Admin Console</h1>
      <section className="space-y-2 max-w-lg">
        <p className="text-sm text-slate-600">Paste your bearer token to unlock admin routes.</p>
        <div className="flex gap-2">
          <input
            className="border rounded px-3 py-2 w-full"
            placeholder="CDSS_API_TOKEN"
            value={token}
            onChange={(e) => setToken(e.target.value)}
          />
          <button
            onClick={handleSave}
            className="bg-slate-900 text-white px-4 py-2 rounded"
          >
            Save
          </button>
        </div>
        {status === "ok" && <p className="text-green-600 text-sm">Token saved.</p>}
        {status === "error" && <p className="text-red-600 text-sm">Invalid token.</p>}
      </section>

      <section className="grid gap-3">
        <Link className="underline text-blue-600" href="/admin/drugs">
          Manage Drugs
        </Link>
        <Link className="underline text-blue-600" href="/admin/diagnoses">
          Manage Diagnoses
        </Link>
        <Link className="underline text-blue-600" href="/admin/presentations">
          Manage Presentations
        </Link>
      </section>
    </main>
  );
}
