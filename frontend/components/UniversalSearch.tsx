"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { Search, ArrowRight, Loader2, Pill, Stethoscope, BookOpen } from "lucide-react";

import { api } from "@/lib/api";
import { useDebouncedValue } from "@/lib/hooks/useDebouncedValue";
import { SearchResult } from "@/lib/types";

const MIN_QUERY = 1;

async function fetchSearch(q: string) {
  const res = await api.get<SearchResult[]>("/clinical/search", { params: { q } });
  return res.data;
}

export default function UniversalSearch() {
  const [query, setQuery] = useState("");
  const debounced = useDebouncedValue(query, 160); // keep latency low but avoid request spam

  const { data, isFetching } = useQuery({
    queryKey: ["universal-search", debounced],
    queryFn: () => fetchSearch(debounced),
    enabled: debounced.trim().length >= MIN_QUERY,
    staleTime: 1000 * 60, // cache responses for 1 min to keep sub-20ms on repeat
    gcTime: 1000 * 60 * 5,
    placeholderData: (prev) => prev,
  });

  const grouped = useMemo(() => {
    const rows = data ?? [];
    return {
      presentations: rows.filter((r) => r.type === "presentation").slice(0, 4),
      diagnoses: rows.filter((r) => r.type === "diagnosis").slice(0, 4),
      symptoms: rows.filter((r) => r.type === "symptom").slice(0, 4),
      drugs: rows.filter((r) => r.type === "drug").slice(0, 4),
    };
  }, [data]);

  return (
    <div className="space-y-3">
      <div className="relative">
        <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
          <Search className="text-slate-400 dark:text-slate-500" size={18} />
        </div>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          type="text"
          placeholder="Search presentations, diagnoses, symptoms, drugs"
          className="w-full pl-12 pr-4 py-4 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-slate-900 dark:text-slate-100 placeholder:text-slate-400"
        />
        {isFetching && (
          <div className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400">
            <Loader2 className="animate-spin" size={18} />
          </div>
        )}
      </div>

      {debounced && (
        <div className="grid md:grid-cols-2 gap-3">
          <ResultGroup
            title="Presentations"
            icon={<BookOpen size={16} />}
            items={grouped.presentations.map((p) => ({
              name: p.name,
              href: `/clinical/presentations/${encodeURIComponent(p.name)}`,
            }))}
          />
          <ResultGroup
            title="Diagnoses / Symptoms"
            icon={<Stethoscope size={16} />}
            items={[...grouped.diagnoses, ...grouped.symptoms].map((p) => ({
              name: p.name,
              href: "/clinical",
            }))}
          />
          <ResultGroup
            title="Drugs"
            icon={<Pill size={16} />}
            items={grouped.drugs.map((p) => ({
              name: p.name,
              href: `/drugs?q=${encodeURIComponent(p.name)}`,
            }))}
          />
        </div>
      )}
    </div>
  );
}

function ResultGroup({
  title,
  icon,
  items,
}: {
  title: string;
  icon: React.ReactNode;
  items: { name: string; href: string }[];
}) {
  return (
    <div className="border border-slate-200 dark:border-slate-800 rounded-xl p-3 bg-white/70 dark:bg-slate-900/70">
      <div className="flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-200 mb-2">
        {icon} {title}
      </div>
      {items.length === 0 ? (
        <p className="text-sm text-slate-500">No matches</p>
      ) : (
        <ul className="space-y-1 text-sm">
          {items.map((item) => (
            <li key={item.href}>
              <Link
                href={item.href}
                className="flex items-center justify-between rounded-md px-3 py-2 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              >
                <span>{item.name}</span>
                <ArrowRight size={14} className="text-slate-400" />
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
