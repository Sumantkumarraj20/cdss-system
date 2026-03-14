"use client";

import { useState, Suspense } from "react"; 
import { useRouter, useSearchParams } from "next/navigation";
import { api, setAuthToken } from "@/lib/api";

// 2. Move your logic into a sub-component
function LoginForm() {
  const [token, setToken] = useState("");
  const [status, setStatus] = useState<"idle" | "ok" | "error">("idle");
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirect = searchParams.get("redirect") || "/admin";

  const submit = async () => {
    try {
      const res = await api.post("/auth/login", { token });
      setAuthToken(res.data.access_token || token);
      setStatus("ok");
      router.push(redirect);
    } catch {
      setStatus("error");
    }
  };

  return (
    <div className="bg-white rounded-xl shadow p-6 w-full max-w-md space-y-4">
      <h1 className="text-xl font-semibold">Admin Login</h1>
      <p className="text-sm text-slate-600">
        Enter your admin token. Cookies will be set for cross-site requests.
      </p>
      <input
        className="border rounded px-3 py-2 w-full"
        placeholder="CDSS_API_TOKEN"
        value={token}
        onChange={(e) => setToken(e.target.value)}
      />
      <button
        onClick={submit}
        className="bg-slate-900 text-white px-4 py-2 rounded w-full"
      >
        Continue
      </button>
      {status === "ok" && <p className="text-green-600 text-sm">Logged in.</p>}
      {status === "error" && <p className="text-red-600 text-sm">Invalid token.</p>}
    </div>
  );
}

// 3. Export a default function that wraps the form in Suspense
export default function LoginPage() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <Suspense fallback={<div>Loading...</div>}>
        <LoginForm />
      </Suspense>
    </main>
  );
}