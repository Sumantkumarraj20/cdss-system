"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { useSearchParams, useRouter } from "next/navigation";
import { Pill, Search } from "lucide-react";

import { api } from "@/lib/api";
import { useDebouncedValue } from "@/lib/hooks/useDebouncedValue";
import { useMedicalSearch } from "@/lib/hooks/useMedicalSearch";
import { DrugBase, DrugSearchResult } from "@/lib/types";

const PAGE_SIZE = 20;

async function searchDrugs(q: string, offset: number): Promise<DrugSearchResult> {
  const res = await api.get<DrugSearchResult>("/drugs/search", {
    params: { q, limit: PAGE_SIZE, offset },
  });
  return res.data;
}

export default function DrugSearchPage() {
  const params = useSearchParams();
  const router = useRouter();
  const initialQ = params.get("q") || "";
  const { setQuery: setLocalQuery, results, ready: localReady } = useMedicalSearch();

  const [q, setQ] = useState(initialQ);
  const [page, setPage] = useState(0);
  const debounced = useDebouncedValue(q, 400);

  const offset = page * PAGE_SIZE;

  useEffect(() => {
    const currentQ = params.get("q") || "";
    if (debounced === currentQ) return;
    const search = debounced ? `?q=${encodeURIComponent(debounced)}` : "";
    router.replace(search, { scroll: false });
  }, [debounced, params, router]);

  const { data, isFetching, isError } = useQuery({
    queryKey: ["drug-search", debounced, offset],
    queryFn: () => searchDrugs(debounced, offset),
    enabled: debounced.length >= 2 && !localReady, // prefer local cache when ready
    placeholderData: (prev) => prev,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
  });

  // Local-first: use Fuse results when ready to avoid network.
  const localItems = results.drugs;
  const items: DrugBase[] =
    localReady && debounced.length >= 2
      ? localItems
      : data?.items ?? [];
  const total =
    localReady && debounced.length >= 2 ? localItems.length : data?.total ?? 0;
  const canPrev = page > 0;
  const canNext = offset + PAGE_SIZE < total;

  const headline = useMemo(() => {
    if (!debounced) return "Search the formulary";
    if (isFetching) return "Searching…";
    return `${total} result${total === 1 ? "" : "s"}`;
  }, [debounced, isFetching, total]);

  return (
    <div className="bg-slate-50 dark:bg-slate-950 min-h-screen">
      <div className="max-w-6xl mx-auto px-4 py-10 space-y-6">
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm p-6 space-y-4">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div>
              <p className="text-xs uppercase tracking-wide text-blue-600 font-semibold">Drug explorer</p>
              <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-50">Search & review monographs</h1>
            </div>
            <Link href="/clinical" className="text-sm text-blue-600 hover:underline">Clinical workspace</Link>
          </div>

          <div className="relative">
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
              <Search size={18} />
            </div>
            <input
              value={q}
              onChange={(e) => {
                setPage(0);
                setQ(e.target.value);
                setLocalQuery(e.target.value);
              }}
              placeholder="Drug name or generic (min 2 chars)"
              className="w-full pl-10 pr-3 py-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <p className="text-sm text-slate-500">{headline}</p>
        </div>

        {isError && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            Failed to fetch drugs. Check API base URL.
          </div>
        )}

        <div className="grid gap-3">
          {items.map((drug: DrugBase) => (
            <Link
              key={drug.id}
              href={`/drugs/${drug.id}`}
              className="block bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 hover:border-blue-500 transition-colors"
            >
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-lg font-semibold text-slate-900 dark:text-slate-50">{drug.name}</p>
                  {drug.generic_name && <p className="text-sm text-slate-500">{drug.generic_name}</p>}
                </div>
                <Pill className="text-blue-500" />
              </div>
              <div className="flex flex-wrap gap-3 text-xs text-slate-600 dark:text-slate-400 mt-2">
                {drug.therapeutic_class && <span className="px-2 py-1 rounded bg-slate-100 dark:bg-slate-800">{drug.therapeutic_class}</span>}
                {drug.chemical_class && <span className="px-2 py-1 rounded bg-slate-100 dark:bg-slate-800">{drug.chemical_class}</span>}
                {drug.habit_forming && <span className="px-2 py-1 rounded bg-amber-100 text-amber-700">Habit forming</span>}
              </div>
            </Link>
          ))}

          {debounced.length >= 2 && items.length === 0 && !isFetching && (
            <div className="p-6 text-center text-slate-500 border border-dashed border-slate-300 rounded-xl">
              No drugs matched that query.
            </div>
          )}
        </div>

        {total > PAGE_SIZE && (
          <div className="flex items-center justify-between bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4">
            <button
              onClick={() => setPage((p) => Math.max(0, p - 1))}
              disabled={!canPrev}
              className={`px-4 py-2 rounded-md border ${
                canPrev ? "border-slate-300 hover:border-blue-500" : "border-slate-200 text-slate-400 cursor-not-allowed"
              }`}
            >
              Previous
            </button>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Page {page + 1} • showing {items.length} of {total}
            </p>
            <button
              onClick={() => setPage((p) => p + 1)}
              disabled={!canNext}
              className={`px-4 py-2 rounded-md border ${
                canNext ? "border-slate-300 hover:border-blue-500" : "border-slate-200 text-slate-400 cursor-not-allowed"
              }`}
            >
              Next
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
