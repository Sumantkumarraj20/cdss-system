"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  BookOpen,
  HeartPulse,
  Pill,
  ShieldCheck,
  Stethoscope,
} from "lucide-react";

import { api } from "@/lib/api";
import { useDebouncedValue } from "@/lib/hooks/useDebouncedValue";
import {
  DecisionSupportResponse,
  DrugsResponse,
  SearchResult,
} from "@/lib/types";

const cardClass =
  "bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm";

async function fetchClinicalSearch(q: string) {
  const res = await api.get<SearchResult[]>("/clinical/search", { params: { q } });
  return res.data;
}

async function fetchDrugs(endpoint: string, key: string, value: string) {
  const res = await api.get<DrugsResponse>(`/clinical/${endpoint}`, {
    params: { [key]: value },
  });
  return res.data.items;
}

function DrugList({
  title,
  description,
  items,
}: {
  title: string;
  description?: string;
  items: { id: string; name: string; generic_name?: string | null }[];
}) {
  if (!items.length) return null;
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-500 mb-1">{title}</p>
          {description && <p className="text-sm text-slate-500">{description}</p>}
        </div>
        <Pill className="text-blue-500" size={18} />
      </div>
      <div className="grid sm:grid-cols-2 gap-2">
        {items.map((d) => (
          <Link
            key={d.id}
            href={`/drugs/${d.id}`}
            className="block border border-slate-200 dark:border-slate-800 rounded-lg px-3 py-2 hover:border-blue-500 transition-colors"
          >
            <div className="font-medium text-slate-900 dark:text-slate-50">{d.name}</div>
            {d.generic_name && (
              <div className="text-sm text-slate-500">{d.generic_name}</div>
            )}
          </Link>
        ))}
      </div>
    </div>
  );
}

export default function ClinicalDashboard() {
  const [q, setQ] = useState("");
  const debounced = useDebouncedValue(q, 400);

  const [sideEffect, setSideEffect] = useState("");
  const [disease, setDisease] = useState("");
  const [contra, setContra] = useState("");
  const [interaction, setInteraction] = useState("");
  const [ecgEffect, setEcgEffect] = useState("");

  const [symptoms, setSymptoms] = useState("chest pain, dyspnea");
  const [signs, setSigns] = useState("tachycardia");
  const [vitals, setVitals] = useState("hr:110, bp:90/60");

  const searchQuery = useQuery({
    queryKey: ["clinical-search", debounced],
    queryFn: () => fetchClinicalSearch(debounced),
    enabled: debounced.trim().length > 0,
  });

  const drugsBySideEffect = useQuery({
    queryKey: ["drugs-side-effect", sideEffect],
    queryFn: () => fetchDrugs("drugs-by-side-effect", "name", sideEffect),
    enabled: sideEffect.trim().length > 1,
  });
  const drugsByDisease = useQuery({
    queryKey: ["drugs-disease", disease],
    queryFn: () => fetchDrugs("drugs-by-disease", "name", disease),
    enabled: disease.trim().length > 1,
  });
  const drugsByContra = useQuery({
    queryKey: ["drugs-contra", contra],
    queryFn: () => fetchDrugs("drug-contraindications", "condition", contra),
    enabled: contra.trim().length > 1,
  });
  const drugsInteractions = useQuery({
    queryKey: ["drugs-interactions", interaction],
    queryFn: () => fetchDrugs("drug-interactions", "drug", interaction),
    enabled: interaction.trim().length > 1,
  });
  const drugsByEcg = useQuery({
    queryKey: ["drugs-ecg", ecgEffect],
    queryFn: () => fetchDrugs("drugs-by-ecg-effect", "effect", ecgEffect),
    enabled: ecgEffect.trim().length > 1,
  });

  const decisionSupport = useMutation({
    mutationKey: ["decision-support"],
    mutationFn: async (): Promise<DecisionSupportResponse> => {
      const payload = {
        symptoms: symptoms
          .split(/[,\n]/)
          .map((s) => s.trim())
          .filter(Boolean),
        signs: signs
          .split(/[,\n]/)
          .map((s) => s.trim())
          .filter(Boolean),
        vitals: vitals
          .split(/[,\n]/)
          .map((s) => s.trim())
          .filter(Boolean)
          .reduce<Record<string, string>>((acc, cur) => {
            const [k, v] = cur.split(":");
            if (k && v) acc[k.trim()] = v.trim();
            return acc;
          }, {}),
      };
      const res = await api.post<DecisionSupportResponse>("/clinical/decision-support", payload);
      return res.data;
    },
  });

  const grouped = useMemo(() => {
    const data = searchQuery.data || [];
    return {
      presentations: data.filter((r) => r.type === "presentation"),
      diagnoses: data.filter((r) => r.type === "diagnosis"),
      symptoms: data.filter((r) => r.type === "symptom"),
      drugs: data.filter((r) => r.type === "drug"),
    };
  }, [searchQuery.data]);

  return (
    <div className="bg-slate-50 dark:bg-slate-950 min-h-screen pb-16">
      <div className="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <div className={`${cardClass} p-6 md:p-8 space-y-4`}>
          <div className="flex items-start justify-between gap-4 flex-wrap">
            <div>
              <p className="text-xs uppercase tracking-wide text-blue-600 font-semibold mb-2">Clinical Workspace</p>
              <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-50">Search across presentations, diagnoses, and drugs</h1>
              <p className="text-slate-600 dark:text-slate-400 mt-2 max-w-2xl">
                Live data powered by the CDSS backend. Type to search, open presentation bundles, or jump to drug monographs.
              </p>
            </div>
            <Link
              href="/drugs"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700"
            >
              <Pill size={18} /> Drug Explorer
            </Link>
          </div>

          <div className="relative">
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search presentations, diagnoses, symptoms, drugs"
              className="w-full px-4 py-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
            />
            <span className="absolute right-4 top-1/2 -translate-y-1/2 text-sm text-slate-400">{q.length}/50</span>
          </div>

          {debounced && (
            <div className="mt-4 grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-200">
                  <BookOpen size={18} /> Presentations
                </div>
                {searchQuery.isLoading && <p className="text-sm text-slate-500">Searching…</p>}
                {!searchQuery.isLoading && grouped.presentations.length === 0 && (
                  <p className="text-sm text-slate-500">No presentations found.</p>
                )}
                <div className="grid gap-2">
                  {grouped.presentations.map((p) => (
                    <Link
                      key={p.name}
                      href={`/clinical/presentations/${encodeURIComponent(p.name)}`}
                      className="flex items-center justify-between px-4 py-3 rounded-lg border border-slate-200 dark:border-slate-800 hover:border-blue-500"
                    >
                      <span>{p.name}</span>
                      <ArrowRight size={16} />
                    </Link>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-200">
                  <Stethoscope size={18} /> Diagnoses & Symptoms
                </div>
                <div className="grid gap-2">
                  {grouped.diagnoses.map((d) => (
                    <div key={`diag-${d.name}`} className="px-4 py-3 rounded-lg border border-slate-200 dark:border-slate-800">
                      <p className="font-medium">{d.name}</p>
                      <p className="text-xs text-slate-500">Diagnosis</p>
                    </div>
                  ))}
                  {grouped.symptoms.map((s) => (
                    <div key={`sym-${s.name}`} className="px-4 py-3 rounded-lg border border-slate-200 dark:border-slate-800">
                      <p className="font-medium">{s.name}</p>
                      <p className="text-xs text-slate-500">Symptom</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          <div className={`${cardClass} p-6 space-y-4 lg:col-span-2`}>
            <div className="flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-200">
              <ShieldCheck size={18} /> Drug Safety & Selection
            </div>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Query the curated knowledge graph for drugs causing side-effects, suitable for diseases, contraindicated conditions, interactions, and ECG effects.
            </p>

            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-xs font-semibold text-slate-600">Side effect</label>
                <input
                  value={sideEffect}
                  onChange={(e) => setSideEffect(e.target.value)}
                  placeholder="e.g., dizziness"
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900"
                />
                {drugsBySideEffect.isFetching && <p className="text-xs text-slate-500">Loading…</p>}
                <DrugList title="Likely cause" items={drugsBySideEffect.data ?? []} />
              </div>

              <div className="space-y-2">
                <label className="text-xs font-semibold text-slate-600">Disease / indication</label>
                <input
                  value={disease}
                  onChange={(e) => setDisease(e.target.value)}
                  placeholder="e.g., hypertension"
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900"
                />
                {drugsByDisease.isFetching && <p className="text-xs text-slate-500">Loading…</p>}
                <DrugList title="Indicated" items={drugsByDisease.data ?? []} />
              </div>

              <div className="space-y-2">
                <label className="text-xs font-semibold text-slate-600">Contraindicated condition</label>
                <input
                  value={contra}
                  onChange={(e) => setContra(e.target.value)}
                  placeholder="e.g., pregnancy"
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900"
                />
                {drugsByContra.isFetching && <p className="text-xs text-slate-500">Loading…</p>}
                <DrugList title="Avoid" description="Not recommended in this condition" items={drugsByContra.data ?? []} />
              </div>

              <div className="space-y-2">
                <label className="text-xs font-semibold text-slate-600">Interactions</label>
                <input
                  value={interaction}
                  onChange={(e) => setInteraction(e.target.value)}
                  placeholder="Drug name to check"
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900"
                />
                {drugsInteractions.isFetching && <p className="text-xs text-slate-500">Loading…</p>}
                <DrugList title="Interacts with" items={drugsInteractions.data ?? []} />
              </div>

              <div className="space-y-2">
                <label className="text-xs font-semibold text-slate-600">ECG effect</label>
                <input
                  value={ecgEffect}
                  onChange={(e) => setEcgEffect(e.target.value)}
                  placeholder="e.g., QT prolongation"
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900"
                />
                {drugsByEcg.isFetching && <p className="text-xs text-slate-500">Loading…</p>}
                <DrugList title="Produces effect" items={drugsByEcg.data ?? []} />
              </div>
            </div>
          </div>

          <div className={`${cardClass} p-6 space-y-4`}>
            <div className="flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-200">
              <Activity size={18} /> Decision Support
            </div>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Lightweight rules + differential ranking. Separate values with commas.
            </p>
            <div className="space-y-3">
              <textarea
                value={symptoms}
                onChange={(e) => setSymptoms(e.target.value)}
                className="w-full rounded-lg border border-slate-200 dark:border-slate-800 px-3 py-2 bg-white dark:bg-slate-900"
                rows={2}
                placeholder="Symptoms (comma separated)"
              />
              <textarea
                value={signs}
                onChange={(e) => setSigns(e.target.value)}
                className="w-full rounded-lg border border-slate-200 dark:border-slate-800 px-3 py-2 bg-white dark:bg-slate-900"
                rows={2}
                placeholder="Signs (comma separated)"
              />
              <textarea
                value={vitals}
                onChange={(e) => setVitals(e.target.value)}
                className="w-full rounded-lg border border-slate-200 dark:border-slate-800 px-3 py-2 bg-white dark:bg-slate-900"
                rows={2}
                placeholder="Vitals as key:value"
              />
              <button
                onClick={() => decisionSupport.mutate()}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg py-2 font-semibold"
              >
                Run decision support
              </button>
              {decisionSupport.isPending && <p className="text-xs text-slate-500">Running…</p>}
              {decisionSupport.error && (
                <p className="text-xs text-red-600">{(decisionSupport.error as any)?.message || "Failed"}</p>
              )}
              {decisionSupport.data && (
                <div className="space-y-2">
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-500">Suggestions</p>
                    <ul className="list-disc pl-4 text-sm space-y-1">
                      {decisionSupport.data.suggestions.length === 0 && (
                        <li className="text-slate-500">No explicit suggestions triggered.</li>
                      )}
                      {decisionSupport.data.suggestions.map((s) => (
                        <li key={s}>{s}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-500">Ranked differentials</p>
                    <ol className="list-decimal pl-4 text-sm space-y-1">
                      {decisionSupport.data.ranked_differentials.length === 0 && (
                        <li className="text-slate-500">No matches</li>
                      )}
                      {decisionSupport.data.ranked_differentials.map((d) => (
                        <li key={d}>{d}</li>
                      ))}
                    </ol>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className={`${cardClass} p-6 space-y-3`}>
          <div className="flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-200">
            <HeartPulse size={18} /> Quick links
          </div>
          <div className="flex flex-wrap gap-3 text-sm">
            <Link className="px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-800 hover:border-blue-500" href="/clinical/presentations/Chest Pain">
              Chest Pain bundle
            </Link>
            <Link className="px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-800 hover:border-blue-500" href="/clinical/presentations/Sepsis">
              Sepsis bundle
            </Link>
            <Link className="px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-800 hover:border-blue-500" href="/drugs">
              Drug search
            </Link>
            <Link className="px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-800 hover:border-blue-500" href="/admin">
              Admin console
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
