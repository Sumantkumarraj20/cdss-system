"use client";

import { FormEvent, useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useMedicalSearch } from "@/lib/hooks/useMedicalSearch";

export default function AdminDrugs() {
  const { results, ready } = useMedicalSearch();
  const [form, setForm] = useState({
    name: "",
    generic_name: "",
    chemical_class: "",
    therapeutic_class: "",
    mechanism: "",
    habit_forming: false,
    pregnancy_category: "",
    lactation_safety: "",
    side_effects: "",
    diseases: "",
    contraindications: "",
  });
  const [msg, setMsg] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setMsg(null);
    try {
      await api.post("/admin/drugs", {
        ...form,
        side_effects: form.side_effects.split(",").map((s) => s.trim()).filter(Boolean),
        diseases: form.diseases.split(",").map((s) => s.trim()).filter(Boolean),
        contraindications: form.contraindications.split(",").map((s) => s.trim()).filter(Boolean),
      });
      setMsg("Created drug");
    } catch (error: any) {
      setMsg(error?.response?.data?.detail || "Failed to create drug");
    }
  };

  return (
    <main className="p-8 space-y-6">
      <h1 className="text-2xl font-semibold">Admin • Drugs</h1>

      <form onSubmit={handleSubmit} className="grid gap-3 max-w-2xl border p-4 rounded">
        <div className="grid grid-cols-2 gap-3">
          <input required placeholder="Name" className="border px-3 py-2 rounded" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          <input placeholder="Generic name" className="border px-3 py-2 rounded" value={form.generic_name} onChange={(e) => setForm({ ...form, generic_name: e.target.value })} />
          <input placeholder="Chemical class" className="border px-3 py-2 rounded" value={form.chemical_class} onChange={(e) => setForm({ ...form, chemical_class: e.target.value })} />
          <input placeholder="Therapeutic class" className="border px-3 py-2 rounded" value={form.therapeutic_class} onChange={(e) => setForm({ ...form, therapeutic_class: e.target.value })} />
          <input placeholder="Mechanism" className="border px-3 py-2 rounded" value={form.mechanism} onChange={(e) => setForm({ ...form, mechanism: e.target.value })} />
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={form.habit_forming} onChange={(e) => setForm({ ...form, habit_forming: e.target.checked })} />
            Habit forming
          </label>
          <input placeholder="Pregnancy category" className="border px-3 py-2 rounded" value={form.pregnancy_category} onChange={(e) => setForm({ ...form, pregnancy_category: e.target.value })} />
          <input placeholder="Lactation safety" className="border px-3 py-2 rounded" value={form.lactation_safety} onChange={(e) => setForm({ ...form, lactation_safety: e.target.value })} />
        </div>
        <textarea placeholder="Side effects (comma separated)" className="border px-3 py-2 rounded" value={form.side_effects} onChange={(e) => setForm({ ...form, side_effects: e.target.value })} />
        <textarea placeholder="Diseases/uses (comma separated)" className="border px-3 py-2 rounded" value={form.diseases} onChange={(e) => setForm({ ...form, diseases: e.target.value })} />
        <textarea placeholder="Contraindications (comma separated)" className="border px-3 py-2 rounded" value={form.contraindications} onChange={(e) => setForm({ ...form, contraindications: e.target.value })} />
        <button className="bg-slate-900 text-white px-4 py-2 rounded w-fit">Create</button>
        {msg && <p className="text-sm">{msg}</p>}
      </form>

      <section>
        <h2 className="text-lg font-semibold mb-2">Local search snapshot</h2>
        {!ready && <p className="text-sm text-slate-500">Loading cache…</p>}
        {ready && (
          <ul className="grid gap-1 text-sm">
            {results.drugs.slice(0, 20).map((d) => (
              <li key={d.id} className="border px-3 py-2 rounded">
                <div className="font-medium">{d.name}</div>
                <div className="text-slate-600">{d.generic_name}</div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
