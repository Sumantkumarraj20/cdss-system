"use client";

import { useState } from "react";
import Link from "next/link";
import { Menu, X } from "lucide-react";

export default function Header() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur dark:border-slate-800">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link
          href="/"
          className="text-lg font-semibold tracking-tight text-slate-900 dark:text-slate-100"
        >
          CDSS<span className="text-blue-600">Ward</span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-700 dark:text-slate-300">
          <Link href="/" className="hover:text-blue-600 transition-colors">
            Home
          </Link>

          <Link
            href="/clinical"
            className="hover:text-blue-600 transition-colors"
          >
            Clinical
          </Link>

          <Link
            href="/drugs"
            className="hover:text-blue-600 transition-colors"
          >
            Drugs
          </Link>

          <Link href="/admin" className="hover:text-blue-600 transition-colors">
            Admin
          </Link>

          <Link
            href="/login"
            className="ml-2 px-4 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700 transition-colors"
          >
            Login
          </Link>
        </nav>

        {/* Mobile Menu Button */}
        <button
          aria-label="Toggle menu"
          className="md:hidden text-slate-700 dark:text-slate-200"
          onClick={() => setOpen(!open)}
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {/* Mobile Navigation */}
      {open && (
        <div className="md:hidden border-t dark:border-slate-800 bg-white dark:bg-slate-900">
          <nav className="flex flex-col px-4 py-3 text-sm font-medium text-slate-700 dark:text-slate-300">
            <Link
              href="/"
              className="py-2 hover:text-blue-600"
              onClick={() => setOpen(false)}
            >
              Home
            </Link>

            <Link
              href="/clinical"
              className="py-2 hover:text-blue-600"
              onClick={() => setOpen(false)}
            >
              Clinical
            </Link>

            <Link
              href="/drugs"
              className="py-2 hover:text-blue-600"
              onClick={() => setOpen(false)}
            >
              Drugs
            </Link>

            <Link
              href="/admin"
              className="py-2 hover:text-blue-600"
              onClick={() => setOpen(false)}
            >
              Admin
            </Link>

            <Link
              href="/login"
              className="mt-2 px-4 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700 text-center"
              onClick={() => setOpen(false)}
            >
              Login
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
}
