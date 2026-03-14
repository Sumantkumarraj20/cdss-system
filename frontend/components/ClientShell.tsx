"use client";

import React from "react";
import Header from "@/components/Header";
import ReactQueryProvider from "@/lib/react-query-provider";
import SyncBootstrap from "@/components/SyncBootstrap";

export default function ClientShell({ children }: { children: React.ReactNode }) {
  return (
    <ReactQueryProvider>
      <SyncBootstrap>
        <div className="min-h-screen flex flex-col">
          <Header />
          <main className="flex-1">{children}</main>
        </div>
      </SyncBootstrap>
    </ReactQueryProvider>
  );
}
