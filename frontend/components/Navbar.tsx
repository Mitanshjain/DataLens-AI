"use client";

// ==========================================
// DATALENS AI - NAVBAR V5
// Midnight glass · brass hairline · hides on scroll down · shows on scroll up
// ==========================================

import { useEffect, useRef, useState } from "react";

const links = [
  { label: "Workspace", href: "#workspace" },
  { label: "Archive", href: "#archive" },
];

export default function Navbar() {
  const [hidden, setHidden] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [progress, setProgress] = useState(0);
  const [active, setActive] = useState<string | null>(null);

  const lastY = useRef(0);
  const ticking = useRef(false);

  useEffect(() => {
    function update() {
      const y = window.scrollY;
      const delta = y - lastY.current;
      const max =
        document.documentElement.scrollHeight - window.innerHeight;

      setScrolled(y > 12);
      setProgress(max > 0 ? Math.min(y / max, 1) : 0);

      if (y < 90) {
        setHidden(false); // always visible near the top
      } else if (delta > 6) {
        setHidden(true); // scrolling down
      } else if (delta < -6) {
        setHidden(false); // scrolling up
      }

      lastY.current = y;
      ticking.current = false;
    }

    function onScroll() {
      if (!ticking.current) {
        ticking.current = true;
        requestAnimationFrame(update);
      }
    }

    lastY.current = window.scrollY;
    update();

    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Highlight the link for the section currently on screen
  useEffect(() => {
    const targets = links
      .map((l) => document.querySelector(l.href))
      .filter((el): el is Element => el !== null);
    if (targets.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) setActive(`#${entry.target.id}`);
        });
      },
      { rootMargin: "-35% 0px -55% 0px" },
    );

    targets.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, []);

  return (
    <header
      onFocusCapture={() => setHidden(false)}
      className={`sticky top-0 z-50 border-b backdrop-blur-2xl backdrop-saturate-150 transition-[transform,background-color,border-color,box-shadow] duration-500 ease-[cubic-bezier(.2,.7,.2,1)] ${
        hidden ? "-translate-y-full" : "translate-y-0"
      } ${
        scrolled
          ? "border-white/10 bg-[#060a13]/85 shadow-[0_24px_60px_-24px_rgba(0,0,0,.75)]"
          : "border-white/[0.06] bg-[#060a13]/55"
      }`}
    >
      {/* brass hairline along the top edge */}
      <span
        aria-hidden
        className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/50 to-transparent"
      />

      {/* scroll progress */}
      <div
        aria-hidden
        className="absolute inset-x-0 bottom-[-1px] h-[2px] origin-left bg-gradient-to-r from-[#4d5b9e] via-[#a9bbd8] to-[#c9b98a] transition-opacity duration-300"
        style={{
          transform: `scaleX(${progress})`,
          opacity: scrolled ? 1 : 0,
        }}
      />

      <div className="mx-auto flex h-[72px] max-w-[1360px] items-center justify-between px-6 lg:px-10">
        {/* ==================================
            BRAND
        ================================== */}

        <a
          href="#"
          className="group flex items-center gap-3.5 rounded-xl focus:outline-none focus-visible:ring-2 focus-visible:ring-[#a9bbd8] focus-visible:ring-offset-2 focus-visible:ring-offset-[#060a13]"
        >
          <div className="relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-[#e4e9f5] to-[#a9bbd8] text-[13px] font-bold tracking-wide text-[#060a13] shadow-[0_10px_30px_-8px_rgba(105,122,196,.7)] ring-1 ring-white/30 transition-transform duration-300 group-hover:scale-105 group-hover:rotate-[-4deg]">
            DL
            <span
              aria-hidden
              className="absolute inset-x-2 top-0 h-px bg-gradient-to-r from-transparent via-white/90 to-transparent"
            />
          </div>

          <div className="leading-none">
            <span className="block text-[17px] font-semibold tracking-[-0.02em] text-white">
              DataLens AI
            </span>
            <span className="mt-1.5 hidden text-[11px] text-slate-500 sm:block">
              Intelligence workspace
            </span>
          </div>
        </a>

        {/* ==================================
            NAVIGATION (centered pill)
        ================================== */}

        <nav
          aria-label="Primary"
          className="absolute left-1/2 hidden -translate-x-1/2 items-center gap-1 rounded-full border border-white/10 bg-white/[0.04] p-1 shadow-[inset_0_1px_0_rgba(255,255,255,.06)] md:flex"
        >
          {links.map((link) => {
            const isActive = active === link.href;
            return (
              <a
                key={link.href}
                href={link.href}
                aria-current={isActive ? "location" : undefined}
                className={`rounded-full px-5 py-2 text-sm font-medium transition duration-300 hover:bg-white/[0.08] hover:text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-[#a9bbd8] ${
                  isActive
                    ? "bg-white/[0.1] text-white shadow-[inset_0_0_0_1px_rgba(255,255,255,.08)]"
                    : "text-slate-400"
                }`}
              >
                {link.label}
              </a>
            );
          })}
        </nav>

        {/* ==================================
            STATUS + ACTION
        ================================== */}

        <div className="flex items-center gap-3">
          <div className="hidden items-center gap-2.5 rounded-full border border-white/10 bg-white/[0.04] py-1.5 pl-3 pr-4 lg:flex">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-50" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
            </span>
            <span className="text-xs font-medium text-slate-300">
              System online
            </span>
          </div>

          <a
            href="#workspace"
            className="group inline-flex h-10 items-center gap-2 rounded-full bg-[#f5f4ef] px-5 text-sm font-semibold text-[#060a13] shadow-[0_10px_30px_-12px_rgba(169,187,216,.6)] transition duration-300 hover:-translate-y-px hover:bg-white hover:shadow-[0_14px_34px_-10px_rgba(169,187,216,.8)] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#a9bbd8] focus-visible:ring-offset-2 focus-visible:ring-offset-[#060a13]"
          >
            New analysis
            <span className="transition-transform group-hover:translate-x-0.5">
              →
            </span>
          </a>
        </div>
      </div>
    </header>
  );
}