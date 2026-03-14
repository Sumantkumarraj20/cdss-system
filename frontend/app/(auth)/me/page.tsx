"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function MePage() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .get("/auth/me")
      .then((res) => setData(res.data))
      .catch((err) => setError(err?.response?.data?.detail || "Not authenticated"));
  }, []);

  return (
    <main className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <div className="bg-white rounded-xl shadow p-6 w-full max-w-md space-y-2">
        <h1 className="text-xl font-semibold">Me</h1>
        {error && <p className="text-red-600 text-sm">{error}</p>}
        {data && <pre className="text-xs bg-slate-100 p-3 rounded">{JSON.stringify(data, null, 2)}</pre>}
      </div>
    </main>
  );
}
