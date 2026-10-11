"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { backendApi, GuidanceResponse } from "@/lib/api-client";
import { demoGuidance } from "@/lib/demo-data";

export default function CivicGuidancePage() {
  const [sources, setSources] = useState<GuidanceResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    async function loadGuidance() {
      try {
        const result = await backendApi.searchGuidance("registration deadline identification");
        if (active) {
          setSources(result);
        }
      } catch {
        if (active) {
          setSources(
            demoGuidance.map((item) => ({
              source_id: item.id,
              source_title: item.title,
              title: item.title,
              section: item.section,
              excerpt: item.excerpt,
              url: item.url,
              jurisdiction: item.jurisdiction,
            })),
          );
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadGuidance();
    return () => {
      active = false;
    };
  }, []);

  const displaySources = sources.length > 0 ? sources : demoGuidance.map((item) => ({
    source_id: item.id,
    source_title: item.title,
    title: item.title,
    section: item.section,
    excerpt: item.excerpt,
    url: item.url,
    jurisdiction: item.jurisdiction,
  }));

  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-wide text-muted-foreground">Civic guidance</p>
          <h1 className="text-3xl font-semibold">Official procedures and citations</h1>
        </div>
        <Link href="/" className="rounded border px-3 py-2 text-sm hover:bg-muted">
          Home
        </Link>
      </div>

      {loading ? <p className="text-sm text-muted-foreground">Loading guidance…</p> : null}

      <div className="space-y-4">
        {displaySources.map((source) => (
          <article key={source.source_id} className="rounded-lg border p-5">
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-lg font-semibold">{source.title}</h2>
              <span className="text-xs uppercase tracking-wide text-muted-foreground">{source.jurisdiction}</span>
            </div>
            <p className="mt-2 text-sm font-medium text-muted-foreground">{source.section}</p>
            <p className="mt-3 text-sm leading-relaxed">{source.excerpt}</p>
            <a href={source.url} target="_blank" rel="noreferrer" className="mt-3 inline-flex text-sm underline-offset-2 hover:underline">
              Open source
            </a>
          </article>
        ))}
      </div>
    </main>
  );
}
