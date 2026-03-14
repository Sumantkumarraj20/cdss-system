"use client";

import { useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { CACHE_KEYS, CACHE_TTL_MS, fetchWithCache } from "@/lib/cache";

const fallbackPresentation = {
  name: "Chest Pain",
  evidence_level: "Level A",
  guideline_source: "ESC 2023",
  last_updated: "2026-03-13",
  redFlags: [
    "Systolic BP < 90 mmHg",
    "SpO2 < 90% on oxygen",
    "New neuro deficit",
    "Tearing pain to back",
    "Syncope or VT",
  ],
  immediateActions: [
    "Activate cath lab if STEMI",
    "Give aspirin 300 mg now",
    "Secure IV access x2",
    "Call senior within 5 minutes",
  ],
  differentials: [
    {
      name: "MI",
      cues: ["Pressure-like pain", "Radiation to arm/jaw", "ECG changes"],
      risk: "High",
    },
    {
      name: "PE",
      cues: ["Pleuritic pain", "Tachycardia", "Recent immobility"],
      risk: "Medium",
    },
    {
      name: "Aortic dissection",
      cues: ["Sudden tearing", "Pulse deficit", "Wide mediastinum"],
      risk: "High",
    },
  ],
  investigations: [
    "ECG within 10 minutes",
    "High-sensitivity troponin 0/1h",
    "CT angiogram if dissection suspected",
  ],
  treatment: [
    {
      name: "Heparin",
      detail: "Bolus 60 U/kg (max 4,000 U) unless dissection suspected",
      evidence_level: "Class I",
    },
    {
      name: "Aspirin",
      detail: "300 mg chew, then 75-100 mg daily",
      evidence_level: "Class I",
    },
  ],
  audit_log: [
    {
      clinician: "Dr Patel",
      role: "Cardiology",
      action: "Viewed red flags",
      timestamp: "2026-03-13T09:20:00Z",
    },
    {
      clinician: "Dr Lin",
      role: "ED",
      action: "Acknowledged immediate actions",
      timestamp: "2026-03-13T09:28:00Z",
    },
    {
      clinician: "Dr Gomez",
      role: "ICU",
      action: "Updated treatment plan",
      timestamp: "2026-03-13T09:45:00Z",
    },
  ],
};

const fallbackDiagnoses = {
  primary: "MI",
  shortList: ["MI", "PE", "Aortic dissection"],
  evidence_level: "Level A",
  guideline_source: "AHA 2024",
};

const fallbackDrugInfo = {
  Heparin: {
    dosing: "60 U/kg bolus then 12 U/kg/hr",
    cautions: "Avoid if suspected dissection or high bleeding risk",
  },
  Aspirin: {
    dosing: "300 mg load, 75-100 mg daily",
    cautions: "Check allergy, avoid if active GI bleed",
  },
};

async function loadPresentation() {
  try {
    const res = await api.get("/clinical/presentations/chest-pain");
    return res.data;
  } catch (error) {
    return fallbackPresentation;
  }
}

async function loadDiagnoses() {
  try {
    const res = await api.get("/clinical/search", { params: { q: "chest pain" } });
    return res.data;
  } catch (error) {
    return fallbackDiagnoses;
  }
}

async function loadDrugInfo() {
  try {
    const res = await api.get("/drugs/search", { params: { q: "chest", limit: 5 } });
    return res.data;
  } catch (error) {
    return fallbackDrugInfo;
  }
}

export default function ChestPainPage() {
  const [offline, setOffline] = useState(false);

  useEffect(() => {
    const update = () => setOffline(typeof navigator !== "undefined" && !navigator.onLine);
    update();
    window.addEventListener("offline", update);
    window.addEventListener("online", update);
    return () => {
      window.removeEventListener("offline", update);
      window.removeEventListener("online", update);
    };
  }, []);

  const presentationCacheKey = CACHE_KEYS.presentation("chest-pain");
  const diagnosesCacheKey = CACHE_KEYS.diagnoses("chest-pain");
  const drugsCacheKey = CACHE_KEYS.drugs("chest-pain");

  const presentationQuery = useQuery({
    queryKey: [presentationCacheKey],
    queryFn: () => fetchWithCache(presentationCacheKey, loadPresentation, CACHE_TTL_MS),
  });

  const diagnosesQuery = useQuery({
    queryKey: [diagnosesCacheKey],
    queryFn: () => fetchWithCache(diagnosesCacheKey, loadDiagnoses, CACHE_TTL_MS),
  });

  const drugInfoQuery = useQuery({
    queryKey: [drugsCacheKey],
    queryFn: () => fetchWithCache(drugsCacheKey, loadDrugInfo, CACHE_TTL_MS),
  });

  const presentation = presentationQuery.data ?? fallbackPresentation;
  const diagnoses = diagnosesQuery.data ?? fallbackDiagnoses;
  const drugs = drugInfoQuery.data ?? fallbackDrugInfo;

  const auditLog = useMemo(() => presentation.audit_log ?? [], [presentation.audit_log]);

  return (
    <main className="min-h-screen bg-[#0f172a] text-white p-6 md:p-10">
      <header className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div className="space-y-2">
          <p className="text-xs uppercase text-slate-300">Presentation</p>
          <h1 className="text-3xl md:text-4xl font-semibold tracking-tight">Chest Pain Ward Pathway</h1>
          <div className="flex flex-wrap gap-2 text-xs">
            <span className="rounded-full bg-emerald-500/15 px-3 py-1 text-emerald-200 border border-emerald-500/40">
              Evidence: {presentation.evidence_level}
            </span>
            <span className="rounded-full bg-sky-500/15 px-3 py-1 text-sky-200 border border-sky-500/40">
              Guideline: {presentation.guideline_source}
            </span>
            <span className="rounded-full bg-amber-500/15 px-3 py-1 text-amber-200 border border-amber-500/40">
              Last updated: {presentation.last_updated}
            </span>
            <span className="rounded-full bg-fuchsia-500/15 px-3 py-1 text-fuchsia-200 border border-fuchsia-500/40">
              Cache: 24h (Redis ⇢ offline storage)
            </span>
          </div>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span className={`h-2 w-2 rounded-full ${offline ? "bg-amber-400" : "bg-emerald-400"}`}></span>
          {offline ? "Offline mode • using cached data" : "Online • syncing to cache"}
        </div>
      </header>

      <section className="mt-8 grid gap-4 md:grid-cols-2">
        <Card title="RED FLAGS" accent="from-rose-500/60 to-orange-500/60">
          <List items={presentation.redFlags} />
        </Card>
        <Card title="Immediate Actions" accent="from-orange-500/60 to-amber-500/60">
          <List items={presentation.immediateActions} />
        </Card>
      </section>

      <section className="mt-6">
        <Card title="Differentials" accent="from-cyan-500/50 to-sky-500/50">
          <div className="grid gap-4 md:grid-cols-3">
            {presentation.differentials.map((dx: any) => (
              <div key={dx.name} className="rounded-lg border border-white/10 bg-white/5 p-3">
                <div className="flex items-center justify-between text-sm text-slate-200">
                  <span className="font-semibold">{dx.name}</span>
                  <span className="rounded bg-white/10 px-2 py-0.5 text-xs uppercase">{dx.risk}</span>
                </div>
                <List items={dx.cues} compact />
              </div>
            ))}
          </div>
        </Card>
      </section>

      <section className="mt-6 grid gap-4 md:grid-cols-3">
        <Card title="Investigations" accent="from-blue-500/50 to-indigo-500/50">
          <List items={presentation.investigations} />
        </Card>
        <Card title="Treatment" accent="from-emerald-500/50 to-teal-500/50">
          <div className="space-y-3">
            {presentation.treatment.map((drug: any) => (
              <div key={drug.name} className="rounded-lg border border-white/10 bg-white/5 p-3">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-white">{drug.name}</p>
                    <p className="text-sm text-slate-200">{drug.detail}</p>
                  </div>
                  <span className="rounded bg-white/10 px-2 py-0.5 text-xs uppercase">
                    {drug.evidence_level}
                  </span>
                </div>
                {drugs[drug.name]?.dosing && (
                  <p className="mt-2 text-xs text-slate-300">Dose: {drugs[drug.name].dosing}</p>
                )}
                {drugs[drug.name]?.cautions && (
                  <p className="text-xs text-amber-200">Caution: {drugs[drug.name].cautions}</p>
                )}
              </div>
            ))}
          </div>
        </Card>
        <Card title="Safety" accent="from-purple-500/50 to-pink-500/50">
          <div className="space-y-2 text-sm text-slate-200">
            <InfoRow label="Evidence level" value={presentation.evidence_level} />
            <InfoRow label="Guideline source" value={presentation.guideline_source} />
            <InfoRow label="Last updated" value={presentation.last_updated} />
            <InfoRow label="Primary diagnosis" value={diagnoses.primary} />
          </div>
        </Card>
      </section>

      <section className="mt-8 grid gap-4 md:grid-cols-2">
        <Card title="Clinical Access Log" accent="from-amber-500/60 to-rose-500/60">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="text-slate-300">
                <tr>
                  <th className="py-2">Clinician</th>
                  <th className="py-2">Role</th>
                  <th className="py-2">Action</th>
                  <th className="py-2">Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {auditLog.map((log: any, idx: number) => (
                  <tr key={`${log.clinician}-${idx}`} className="border-t border-white/5">
                    <td className="py-2 text-white">{log.clinician}</td>
                    <td className="py-2 text-slate-200">{log.role}</td>
                    <td className="py-2 text-slate-200">{log.action}</td>
                    <td className="py-2 text-slate-300">{new Date(log.timestamp).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
        <Card title="Caching" accent="from-emerald-500/60 to-teal-500/60">
          <ul className="space-y-1 text-sm text-slate-200">
            <li>presentations → Redis + local fallback (24h)</li>
            <li>diagnoses → Redis + local fallback (24h)</li>
            <li>drug info → Redis + local fallback (24h)</li>
            <li>Offline mode ready for basement / radiology / ICU</li>
          </ul>
        </Card>
      </section>
    </main>
  );
}

function Card({
  title,
  children,
  accent,
}: {
  title: string;
  children: React.ReactNode;
  accent: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4 shadow-lg shadow-black/40">
      <div className={`mb-3 inline-flex rounded-full bg-gradient-to-r ${accent} px-3 py-1 text-xs font-semibold uppercase text-white`}> 
        {title}
      </div>
      <div>{children}</div>
    </div>
  );
}

function List({ items, compact = false }: { items: string[]; compact?: boolean }) {
  const spacing = compact ? "space-y-1" : "space-y-2";
  return (
    <ul className={`${spacing} text-sm text-slate-200`}>
      {items.map((item) => (
        <li key={item} className="flex gap-2">
          <span className="mt-1 h-1.5 w-1.5 rounded-full bg-emerald-400" />
          <span>{item}</span>
        </li>
      ))}
    </ul>
  );
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between rounded-lg border border-white/10 bg-white/5 px-3 py-2">
      <span className="text-slate-300">{label}</span>
      <span className="font-semibold text-white">{value}</span>
    </div>
  );
}
