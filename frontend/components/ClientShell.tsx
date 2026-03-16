"use client";

import Header from "./Header";

export default function ClientShell({
  children,
  authenticated,
}: {
  children: React.ReactNode;
  authenticated: boolean;
}) {
  return (
    <>
      <Header authenticated={authenticated} />
      <main>{children}</main>
    </>
  );
}
