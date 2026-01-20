"use client";

import Link from "next/link";

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <Link href="/" className="flex items-center space-x-2">
          <span className="font-bold text-xl">Fitter</span>
        </Link>
        <nav className="ml-auto flex items-center space-x-4">
          <Link
            href="/fitting"
            className="text-sm font-medium transition-colors hover:text-primary"
          >
            AI 피팅룸
          </Link>
        </nav>
      </div>
    </header>
  );
}
