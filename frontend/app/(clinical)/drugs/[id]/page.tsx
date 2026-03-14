"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, Pill, ShieldAlert } from "lucide-react";

import { api } from "@/lib/api";
import { DrugDetail } from "@/lib/types";

async function fetchDrug(id: string) {
  const res = await api.get<DrugDetail>(`/drugs/${id}`);
  return res.data;
}

export default function DrugDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const id = params.id;

  const { data, isLoading, error } = useQuery({
    queryKey: ["drug", id],
    queryFn: () => fetchDrug(id),
    enabled: Boolean(id),
  });

  return (
    <div className="bg-slate-50 dark:bg-slate-950 min-h-screen">
      <div className="max-w-5xl mx-auto px-4 py-10 space-y-6">
        <button
          onClick={() => router.back()}
          className="inline-flex items-center gap-2 text-sm text-blue-600 hover:underline"
        >
          <ArrowLeft size={16} /> Back
        </button>

        {isLoading && <p className="text-slate-600">Loading drug…</p>}
        {error && (
          <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700">
            Failed to load drug details.
          </div>
        )}

        {data && (
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm p-6 space-y-4">
            <div className="flex items-center gap-3">
              <Pill className="text-blue-500" />
              <div>
                <p className="text-xs uppercase tracking-wide text-blue-600 font-semibold">Drug monograph</p>
                <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-50">{data.name}</h1>
                {data.generic_name && (
                  <p className="text-sm text-slate-500">Generic: {data.generic_name}</p>
                )}
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4 text-sm text-slate-700 dark:text-slate-300">
              <div className="space-y-1">
                <p><span className="font-semibold">Chemical class:</span> {data.chemical_class || "—"}</p>
                <p><span className="font-semibold">Therapeutic class:</span> {data.therapeutic_class || "—"}</p>
                <p><span className="font-semibold">Mechanism:</span> {data.mechanism || "—"}</p>
              </div>
              <div className="space-y-1">
                <p><span className="font-semibold">Pregnancy category:</span> {data.pregnancy_category || "—"}</p>
                <p><span className="font-semibold">Lactation safety:</span> {data.lactation_safety || "—"}</p>
                <p className="flex items-center gap-2">
                  <span className="font-semibold">Habit forming:</span>
                  {data.habit_forming ? (
                    <span className="px-2 py-1 rounded bg-amber-100 text-amber-700">Yes</span>
                  ) : (
                    <span className="px-2 py-1 rounded bg-green-100 text-green-700">No</span>
                  )}
                </p>
              </div>
            </div>

            <div className="grid md:grid-cols-3 gap-4">
              {[{
                title: "Side effects",
                items: data.side_effects,
              }, {
                title: "Indications / diseases",
                items: data.diseases,
              }, {
                title: "Contraindications",
                items: data.contraindications,
              }].map((section) => (
                <div key={section.title} className="border border-slate-200 dark:border-slate-800 rounded-xl p-4 bg-slate-50/60 dark:bg-slate-900/50">
                  <p className="text-sm font-semibold mb-2 text-slate-800 dark:text-slate-100">{section.title}</p>
                  <ul className="list-disc pl-4 text-sm space-y-1 text-slate-700 dark:text-slate-300">
                    {section.items.length === 0 && <li className="text-slate-500">No data</li>}
                    {section.items.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>

            <div className="flex items-center gap-2 text-xs text-slate-500">
              <ShieldAlert size={14} />
              Data pulled from /drugs/{id} endpoint. Use admin console for edits.
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
