"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { backendApi, CaseResponse } from "@/lib/api-client";
import { demoCases } from "@/lib/demo-data";

export default function CasesPage() {
  const [cases, setCases] = useState<CaseResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    async function loadCases() {
      try {
        const result = await backendApi.listCases();
        if (active) {
          setCases(result);
        }
      } catch {
        if (active) {
          setCases(demoCases as unknown as CaseResponse[]);
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadCases();
    return () => {
      active = false;
    };
  }, []);

  const displayCases = cases.length > 0 ? cases : (demoCases as unknown as CaseResponse[]);

  return (
    <main className="mx-auto max-w-3xl px-6 py-12">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-wide text-muted-foreground">Cases</p>
          <h1 className="text-2xl font-semibold">Authorized case records</h1>
        </div>
        <Link href="/cases/new" className="rounded bg-primary px-3 py-2 text-sm text-primary-foreground">
          New case
        </Link>
      </div>
      {loading ? <p className="mt-6 text-sm text-muted-foreground">Loading cases…</p> : null}
      <table className="mt-6 w-full text-left text-sm">
        <thead>
          <tr className="border-b">
            <th className="py-2">Title</th>
            <th className="py-2">Status</th>
            <th className="py-2">Description</th>
          </tr>
        </thead>
        <tbody>
          {displayCases.map((caseRecord) => (
            <tr key={caseRecord.id} className="border-b align-top">
              <td className="py-3">
                <Link href={`/cases/${caseRecord.id}`} className="font-medium underline-offset-2 hover:underline">
                  {caseRecord.title}
                </Link>
              </td>
              <td className="py-3">{caseRecord.status}</td>
              <td className="py-3 text-muted-foreground">{caseRecord.description ?? "No description provided."}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
