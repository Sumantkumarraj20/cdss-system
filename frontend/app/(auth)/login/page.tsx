"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const params = useSearchParams();

  const redirect = params.get("redirect") || "/admin";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();

    const res = await fetch("/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (res.ok) {
      router.push(redirect);
    } else {
      alert("Login failed");
    }
  }

  return (
    <div className="max-w-md mx-auto mt-20 space-y-6">
      {/* Title */}
      <div>
        <h1 className="text-2xl font-semibold">Admin Login</h1>
        <p className="text-sm text-slate-500">
          Sign in to manage CDSS clinical knowledge modules.
        </p>
      </div>

      {/* Form */}
      <form onSubmit={handleLogin} className="space-y-4">
        <input
          type="email"
          required
          className="border w-full p-2 rounded"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          required
          className="border w-full p-2 rounded"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="w-full bg-black text-white px-4 py-2 rounded hover:bg-slate-800">
          Login
        </button>
      </form>

      {/* Registration Navigation */}
      <div className="text-sm text-slate-600 text-center">
        No admin account?{" "}
        <Link
          href="/register"
          className="text-blue-600 hover:underline font-medium"
        >
          Create one
        </Link>
      </div>
    </div>
  );
}
