"use client";

import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { AlertTriangle, ArrowLeft, CheckCircle2, ListChecks } from "lucide-react";

import { api } from "@/lib/api";
import { PresentationBundle } from "@/lib/types";

async function fetchBundle(name: string) {
  const res = await api.get<PresentationBundle>(`/clinical/presentations/${encodeURIComponent(name)}`);
  return res.data;
}

export default function PresentationPage() {
  const params = useParams<{ name: string }>();
  const router = useRouter();
  const name = decodeURIComponent(params.name || "");

  const { data, isLoading, error } = useQuery({
    queryKey: ["presentation", name],
    queryFn: () => fetchBundle(name),
    enabled: Boolean(name),
  });

  const sections = useMemo(
    () => (
      data
        ? [
            { title: "Red flags", icon: <AlertTriangle className="text-red-500" size={18} />, items: data.red_flags },
            { title: "Differentials", icon: <ListChecks className="text-amber-500" size={18} />, items: data.differentials },
            { title: "Investigations", icon: <CheckCircle2 className="text-green-500" size={18} />, items: data.investigations },
            { title: "Treatments", icon: <CheckCircle2 className="text-blue-500" size={18} />, items: data.treatments },
          ]
        : []
    ),
    [data]
  );

  return (
    <div className="bg-slate-50 dark:bg-slate-950 min-h-screen">
      <div className="max-w-5xl mx-auto px-4 py-10 space-y-6">
        <button
          onClick={() => router.back()}
          className="inline-flex items-center gap-2 text-sm text-blue-600 hover:underline"
        >
          <ArrowLeft size={16} /> Back
        </button>

        {isLoading && <p className="text-slate-600">Loading presentation…</p>}
        {error && (
          <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700">
            Failed to load presentation. Ensure the name is exact.
          </div>
        )}

        {data && (
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm p-6 space-y-6">
            <div className="flex items-center justify-between flex-wrap gap-3">
              <div>
                <p className="text-xs uppercase tracking-wide text-blue-600 font-semibold">Presentation bundle</p>
                <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-50">{data.presentation}</h1>
                <p className="text-slate-600 dark:text-slate-400 mt-1">Red flags, investigations, and treatments pulled live from the API.</p>
              </div>
              <Link
                href={`/clinical`}
                className="px-4 py-2 rounded-md border border-slate-200 dark:border-slate-700 hover:border-blue-500 text-sm"
              >
                Open clinical workspace
              </Link>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              {sections.map((section) => (
                <div key={section.title} className="border border-slate-200 dark:border-slate-800 rounded-xl p-4 space-y-2 bg-slate-50/60 dark:bg-slate-900/50">
                  <div className="flex items-center gap-2 text-sm font-semibold text-slate-800 dark:text-slate-100">
                    {section.icon}
                    {section.title}
                  </div>
                  <ul className="list-disc pl-5 text-sm space-y-1 text-slate-700 dark:text-slate-300">
                    {section.items.length === 0 && <li className="text-slate-500">No data</li>}
                    {section.items.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
