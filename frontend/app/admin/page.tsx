"use client";

import Link from "next/link";

export default function AdminHome() {
  return (
    <div className="space-y-10">
      {/* Page Header */}
      <section>
        <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
          Admin Console
        </h1>

        <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
          Manage clinical knowledge resources used by the CDSS engine.
        </p>
      </section>

      {/* Admin Status Card */}
      <section className="max-w-xl bg-white dark:bg-slate-900 border dark:border-slate-800 rounded-lg p-5 space-y-3">
        <h2 className="text-sm font-medium text-slate-800 dark:text-slate-200">
          Authentication
        </h2>

        <p className="text-xs text-green-600">
          You are authenticated as an administrator.
        </p>

        <p className="text-xs text-slate-500">
          Editing features are enabled for clinical knowledge modules.
        </p>
      </section>

      {/* Knowledge Management */}
      <section className="space-y-3">
        <h2 className="text-sm font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">
          Knowledge Modules
        </h2>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <Link
            href="/admin/drugs"
            className="border dark:border-slate-800 bg-white dark:bg-slate-900 rounded-lg p-5 hover:border-blue-500 transition"
          >
            <h3 className="font-medium text-slate-900 dark:text-slate-100">
              Drugs
            </h3>

            <p className="text-xs text-slate-500 mt-1">
              Manage medication database used by CDSS.
            </p>
          </Link>

          <Link
            href="/admin/diagnoses"
            className="border dark:border-slate-800 bg-white dark:bg-slate-900 rounded-lg p-5 hover:border-blue-500 transition"
          >
            <h3 className="font-medium text-slate-900 dark:text-slate-100">
              Diagnoses
            </h3>

            <p className="text-xs text-slate-500 mt-1">
              Maintain disease and condition knowledge base.
            </p>
          </Link>

          <Link
            href="/admin/presentations"
            className="border dark:border-slate-800 bg-white dark:bg-slate-900 rounded-lg p-5 hover:border-blue-500 transition"
          >
            <h3 className="font-medium text-slate-900 dark:text-slate-100">
              Presentations
            </h3>

            <p className="text-xs text-slate-500 mt-1">
              Manage symptom and presentation logic.
            </p>
          </Link>
        </div>
      </section>
    </div>
  );
}
