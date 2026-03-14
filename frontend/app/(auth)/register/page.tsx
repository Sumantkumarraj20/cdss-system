"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

export default function RegisterPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [token, setToken] = useState("");
  const [status, setStatus] = useState<"idle" | "ok" | "error">("idle");

  const submit = async () => {
    try {
      // Placeholder: call login with token; real registration would hit an auth service.
      await api.post("/auth/login", { token });
      setStatus("ok");
      router.push("/login");
    } catch {
      setStatus("error");
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <div className="bg-white rounded-xl shadow p-6 w-full max-w-md space-y-4">
        <h1 className="text-xl font-semibold">Register (placeholder)</h1>
        <input
          className="border rounded px-3 py-2 w-full"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="border rounded px-3 py-2 w-full"
          placeholder="Invite token"
          value={token}
          onChange={(e) => setToken(e.target.value)}
        />
        <button onClick={submit} className="bg-slate-900 text-white px-4 py-2 rounded w-full">
          Continue
        </button>
        {status === "ok" && <p className="text-green-600 text-sm">Registered (stub).</p>}
        {status === "error" && <p className="text-red-600 text-sm">Failed.</p>}
      </div>
    </main>
  );
}
