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
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    getHealth()
      .then((h) => setHealthy(h.status === "healthy"))
      .catch(() => setHealthy(false));
  }, []);

  return (
    <nav aria-label="Main navigation" className="fixed top-0 left-0 right-0 z-50 h-14 border-b border-zinc-800 bg-zinc-900/80 backdrop-blur-sm">
      <div className="max-w-[1200px] mx-auto px-4 h-full flex items-center justify-between">
        <Link
          href="/match"
          className="text-lg font-semibold tracking-tight text-zinc-100"
        >
          Resume2Job
        </Link>

        {/* Desktop nav links */}
        <div className="hidden md:flex items-center gap-1">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              aria-current={pathname === link.href ? "page" : undefined}
              className={cn(
                "px-3 py-2 min-h-[44px] flex items-center text-sm rounded-md transition-colors",
                pathname === link.href
                  ? "bg-zinc-800 text-zinc-100"
                  : "text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/50"
              )}
            >
              {link.label}
            </Link>
          ))}

          <HealthDot healthy={healthy} />
        </div>

        {/* Mobile: health dot + hamburger */}
        <div className="flex md:hidden items-center gap-2">
          <HealthDot healthy={healthy} />
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            aria-expanded={menuOpen}
            aria-label="Toggle navigation menu"
            className="p-2 min-w-[44px] min-h-[44px] flex items-center justify-center rounded-md text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/50"
          >
            {menuOpen ? (
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M5 5l10 10M15 5L5 15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
              </svg>
            ) : (
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M3 6h14M3 10h14M3 14h14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Mobile slide-out menu */}
      {menuOpen && (
        <div className="md:hidden border-b border-zinc-800 bg-zinc-900/95 backdrop-blur-sm">
          <div className="max-w-[1200px] mx-auto px-4 py-2 flex flex-col gap-1">
            {NAV_LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMenuOpen(false)}
                aria-current={pathname === link.href ? "page" : undefined}
                className={cn(
                  "px-3 py-3 min-h-[44px] flex items-center text-sm rounded-md transition-colors",
                  pathname === link.href
                    ? "bg-zinc-800 text-zinc-100"
                    : "text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/50"
                )}
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
}

function HealthDot({ healthy }: { healthy: boolean | null }) {
  return (
    <div className="ml-3 flex items-center gap-1.5" aria-hidden="true">
      <div
        className={cn(
          "w-2 h-2 rounded-full",
          healthy === null
            ? "bg-zinc-400 health-dot-loading"
            : healthy
              ? "bg-green-500"
              : "bg-red-500"
        )}
        title={
          healthy === null
            ? "Checking API..."
            : healthy
              ? "API healthy"
              : "API unreachable"
        }
      />
      <span className="text-xs text-zinc-500">API</span>
    </div>
  );
}
