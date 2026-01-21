"use client";

import Link from "next/link";

export function FittingFloatingCTA() {
  return (
    <Link
      href="/fitting"
      aria-label="AI 피팅룸으로 이동"
      className="fixed right-4 top-1/2 -translate-y-1/2 z-50
                 bg-neutral-900 text-white
                 px-4 py-3
                 rounded-sm
                 text-sm font-semibold
                 shadow-lg
                 transition hover:bg-neutral-800
                 flex flex-col items-center gap-1"
    >
      <span>AI</span>
      <span className="text-xs">피팅룸</span>
    </Link>
  );
}
