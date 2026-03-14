"use client";

import React from "react";
import {
  Search,
  ShieldAlert,
  BookOpen,
  Activity,
  Zap,
  Smartphone,
} from "lucide-react";
import UniversalSearch from "@/components/UniversalSearch";

const LandingPage = () => {
  return (
    <div className="bg-slate-50 dark:bg-slate-950 min-h-full transition-colors duration-300">
      {/* Hero Section */}
      <section className="py-16 px-6 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 text-xs font-bold mb-6 tracking-wide uppercase">
            <Zap size={14} /> Built for Interns & Residents
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 dark:text-slate-50 tracking-tight mb-6">
            Clinical Confidence at the{" "}
            <span className="text-blue-600 dark:text-blue-500">
              Point of Care.
            </span>
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-400 mb-10 max-w-2xl mx-auto leading-relaxed">
            A high-yield decision support system for 300+ common clinical
            presentations. No walls of text—just actionable guides, red flags,
            and drug rationales.
          </p>

          {/* Quick Search - universal, powered by /clinical/search (Meili backend) */}
          <div className="max-w-2xl mx-auto mb-4">
            <UniversalSearch />
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="py-16 px-6 max-w-6xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Feature 1 */}
          <div className="bg-white dark:bg-slate-900 p-8 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-all">
            <div className="w-12 h-12 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg flex items-center justify-center mb-6">
              <ShieldAlert size={24} />
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-slate-50 mb-3">
              Safety First
            </h3>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed text-sm">
              Mandatory "Red Flag" prompts for every clinical encounter. Never
              miss a critical exclusion criterion again.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="bg-white dark:bg-slate-900 p-8 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-all">
            <div className="w-12 h-12 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-lg flex items-center justify-center mb-6">
              <Activity size={24} />
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-slate-50 mb-3">
              Modular Knowledge
            </h3>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed text-sm">
              High-yield pearls for USMLE/NEET-PG integrated directly into
              clinical workflows. Study while you work.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="bg-white dark:bg-slate-900 p-8 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-all">
            <div className="w-12 h-12 bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 rounded-lg flex items-center justify-center mb-6">
              <Smartphone size={24} />
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-slate-50 mb-3">
              Offline Capable
            </h3>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed text-sm">
              Designed for hospital wards with poor signal. Works fully offline
              via RxDB and local indexing.
            </p>
          </div>
        </div>
      </section>

      {/* Quick Access List */}
      <section className="pb-20 px-6 max-w-4xl mx-auto">
        <div className="bg-slate-900 dark:bg-blue-700 rounded-3xl p-8 md:p-12 text-white overflow-hidden relative shadow-xl">
          <div className="relative z-10 text-center md:text-left">
            <h2 className="text-2xl font-bold mb-4">Ready to start a round?</h2>
            <p className="text-slate-300 dark:text-blue-100 mb-8 max-w-md">
              Access 300+ modules categorized by system and emergency priority.
            </p>
            <button className="bg-blue-600 dark:bg-slate-900 hover:bg-blue-500 dark:hover:bg-slate-800 text-white px-8 py-3 rounded-lg font-semibold transition-all shadow-lg active:scale-95">
              Enter Clinical Dashboard
            </button>
          </div>
          <BookOpen className="absolute -right-10 -bottom-10 text-white/10 dark:text-white/5 w-64 h-64 rotate-12" />
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
