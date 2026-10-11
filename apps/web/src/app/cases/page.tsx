import Link from "next/link";

// Placeholder list. Replace with a server-side fetch through lib/api-client
// once the backend cases endpoint is implemented.
const demoCases = [
  { id: "case-demo-001", title: "Demo interview", status: "in_review" },
  { id: "case-demo-002", title: "Demo incident report", status: "draft" },
];

export default function CasesPage() {
  return (
    <main className="mx-auto max-w-3xl px-6 py-12">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Cases</h1>
        <Link href="/cases/new" className="rounded bg-primary px-3 py-2 text-sm text-primary-foreground">
          New case
        </Link>
      </div>
      <table className="mt-6 w-full text-left text-sm">
        <thead>
          <tr className="border-b">
            <th className="py-2">Title</th>
            <th className="py-2">Status</th>
          </tr>
        </thead>
        <tbody>
          {demoCases.map((c) => (
            <tr key={c.id} className="border-b">
              <td className="py-2">
                <Link href={`/cases/${c.id}`} className="underline-offset-2 hover:underline">
                  {c.title}
                </Link>
              </td>
              <td className="py-2">{c.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
