"use client";

import Header from "./Header";
import ReactQueryProvider from "@/lib/react-query-provider";


export default function ClientShell({
  children,
  authenticated,
}: {
  children: React.ReactNode;
  authenticated: boolean;
}) {
  return (
    <ReactQueryProvider>
      <Header authenticated={authenticated} />
      <main>{children}</main>
    </ReactQueryProvider>
  );
}
