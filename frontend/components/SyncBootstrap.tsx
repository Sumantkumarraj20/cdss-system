"use client";

import { useEffect, useRef, useState } from "react";
import { startReplications, getDb } from "@/lib/db";

/**
 * Bootstraps local RxDB and starts live replication exactly once per session.
 * Shows a tiny hidden status (for debugging) without affecting layout.
 */
export default function SyncBootstrap({ children }: { children: React.ReactNode }) {
  const started = useRef(false);
  const [status, setStatus] = useState<"idle" | "ok" | "error">("idle");

  useEffect(() => {
    if (started.current) return;
    started.current = true;
    (async () => {
      try {
        await getDb(); // ensure collections exist
        await startReplications(); // live pull/push with checkpoints
        setStatus("ok");
      } catch (err) {
        console.warn("Sync bootstrap failed", err);
        setStatus("error");
      }
    })();
  }, []);

  return (
    <>
      {children}
      <span aria-hidden className="sr-only">
        sync:{status}
      </span>
    </>
  );
}
