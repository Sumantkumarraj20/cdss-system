"use client";

import { useEffect } from "react";

export default function GlobalError({ error, reset }: { error: Error; reset: () => void }) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <html>
      <body className="min-h-screen bg-slate-50 text-slate-900">
        <div className="max-w-2xl mx-auto py-16 px-6 space-y-4">
          <h1 className="text-2xl font-bold text-red-700">Something went wrong</h1>
          <p className="text-sm text-slate-700 whitespace-pre-wrap bg-red-50 border border-red-200 rounded p-3">
            {error.message || "Unknown error"}
          </p>
          <button
            onClick={() => reset()}
            className="px-4 py-2 rounded bg-slate-900 text-white hover:bg-slate-800"
          >
            Reload page
          </button>
          <p className="text-xs text-slate-500">See console for full stack trace.</p>
        </div>
      </body>
    </html>
  );
}
