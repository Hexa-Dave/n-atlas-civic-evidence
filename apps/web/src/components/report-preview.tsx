export interface ReportSection {
  heading: string;
  body: string;
  citations?: string[];
}

export interface ReportPreviewProps {
  title: string;
  status: "draft" | "final";
  sections: ReportSection[];
}

/**
 * Read-only preview of an assembled report. Testimony and official civic
 * guidance must remain in clearly separated sections.
 */
export function ReportPreview({ title, status, sections }: ReportPreviewProps) {
  return (
    <article className="rounded-lg border p-6">
      <header className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">{title}</h2>
        <span className="rounded-full border px-2 py-0.5 text-xs uppercase">{status}</span>
      </header>
      {sections.map((section) => (
        <section key={section.heading} className="mt-5">
          <h3 className="text-sm font-semibold">{section.heading}</h3>
          <p className="mt-1 whitespace-pre-line text-sm leading-relaxed">{section.body}</p>
          {section.citations?.length ? (
            <ul className="mt-2 list-disc pl-5 text-xs text-muted-foreground">
              {section.citations.map((citation) => (
                <li key={citation}>{citation}</li>
              ))}
            </ul>
          ) : null}
        </section>
      ))}
    </article>
  );
}
