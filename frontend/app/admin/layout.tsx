"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { PropsWithChildren } from "react";

const nav = [
  { href: "/admin", label: "Overview" },
  { href: "/admin/drugs", label: "Drugs" },
  { href: "/admin/diagnoses", label: "Diagnoses" },
  { href: "/admin/presentations", label: "Presentations" },
];

export default function AdminLayout({ children }: PropsWithChildren) {
  const path = usePathname();

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      {/* Sub Navigation */}
      <div className="border-b bg-white/70 dark:bg-slate-900/70 backdrop-blur dark:border-slate-800">
        <div className="max-w-6xl mx-auto px-6 py-3 flex flex-wrap items-center gap-3">
          <span className="text-xs font-medium text-slate-500 uppercase tracking-wide">
            Admin
          </span>

          <nav className="flex flex-wrap gap-2 text-sm">
            {nav.map((item) => {
              const active = path === item.href;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`px-3 py-1.5 rounded-md transition
                  ${
                    active
                      ? "bg-slate-900 text-white"
                      : "text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Page Content */}
      <main className="max-w-6xl mx-auto px-6 py-8">{children}</main>
    </div>
  );
}
