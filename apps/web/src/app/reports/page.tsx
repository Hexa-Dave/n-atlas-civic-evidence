import Link from "next/link";

import { ReportPreview } from "@/components/report-preview";
import { demoReport } from "@/lib/demo-data";

export default function ReportsPage() {
  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-wide text-muted-foreground">Reports</p>
          <h1 className="text-3xl font-semibold">Generated output</h1>
        </div>
        <Link href="/" className="rounded border px-3 py-2 text-sm hover:bg-muted">
          Home
        </Link>
      </div>

      <ReportPreview
        title={demoReport.title}
        status={demoReport.status}
        sections={demoReport.sections.map((section) => ({
          heading: section.heading,
          body: section.body,
          citations: section.citations,
        }))}
      />
    </main>
  );
}
