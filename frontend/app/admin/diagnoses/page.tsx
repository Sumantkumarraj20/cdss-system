"use client";

import { FormEvent, useState } from "react";
import { api } from "@/lib/api";
import { useMedicalSearch } from "@/lib/hooks/useMedicalSearch";

export default function AdminDiagnoses() {
  const { results, ready, setQuery, query } = useMedicalSearch();
  const [form, setForm] = useState({ name: "", icd10_code: "", description: "" });
  const [msg, setMsg] = useState<string | null>(null);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setMsg(null);
    try {
      await api.post("/admin/diagnoses", form);
      setMsg("Created diagnosis");
    } catch (error: any) {
      setMsg(error?.response?.data?.detail || "Failed");
    }
  };

  return (
    <main className="p-8 space-y-6">
      <h1 className="text-2xl font-semibold">Admin • Diagnoses</h1>
      <form onSubmit={submit} className="grid gap-3 max-w-xl border p-4 rounded">
        <input required placeholder="Name" className="border px-3 py-2 rounded" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
        <input placeholder="ICD10 code" className="border px-3 py-2 rounded" value={form.icd10_code} onChange={(e) => setForm({ ...form, icd10_code: e.target.value })} />
        <textarea placeholder="Description" className="border px-3 py-2 rounded" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
        <button className="bg-slate-900 text-white px-4 py-2 rounded w-fit">Create</button>
        {msg && <p className="text-sm">{msg}</p>}
      </form>

      <section className="space-y-2">
        <div className="flex items-center gap-2">
          <input
            className="border px-3 py-2 rounded w-64"
            placeholder="Search cached diagnoses"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          {!ready && <span className="text-sm text-slate-500">Loading cache…</span>}
        </div>
        {ready && (
          <ul className="grid gap-1 text-sm">
            {results.diagnoses.slice(0, 30).map((d) => (
              <li key={d.id} className="border px-3 py-2 rounded">
                <div className="font-medium">{d.name}</div>
                {d.icd10_code && <div className="text-slate-500">{d.icd10_code}</div>}
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
