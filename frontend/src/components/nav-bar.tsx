"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { getHealth } from "@/lib/api";
import { cn } from "@/lib/utils";

const NAV_LINKS = [
  { href: "/match", label: "Match" },
  { href: "/compare", label: "Compare" },
  { href: "/entities", label: "Entities" },
  { href: "/evaluation", label: "Evaluation" },
];

export function NavBar() {
  const pathname = usePathname();
  const [healthy, setHealthy] = useState<boolean | null>(null);

  useEffect(() => {
    getHealth()
      .then((h) => setHealthy(h.status === "healthy"))
      .catch(() => setHealthy(false));
  }, []);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 h-14 border-b border-zinc-800 bg-zinc-900/80 backdrop-blur-sm">
      <div className="max-w-[1200px] mx-auto px-4 h-full flex items-center justify-between">
        <Link
          href="/match"
          className="text-lg font-semibold tracking-tight text-zinc-100"
        >
          Resume2Job
        </Link>

        <div className="flex items-center gap-1">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "px-3 py-1.5 text-sm rounded-md transition-colors",
                pathname === link.href
                  ? "bg-zinc-800 text-zinc-100"
                  : "text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/50"
              )}
            >
              {link.label}
            </Link>
          ))}

          <div className="ml-3 flex items-center gap-1.5">
            <div
              className={cn(
                "w-2 h-2 rounded-full",
                healthy === null
                  ? "bg-zinc-600"
                  : healthy
                    ? "bg-green-500"
                    : "bg-red-500"
              )}
            />
            <span className="text-xs text-zinc-500">API</span>
          </div>
        </div>
      </div>
    </nav>
  );
}
