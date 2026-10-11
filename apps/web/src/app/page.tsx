import Link from "next/link";

const sections = [
  { href: "/cases", title: "Cases", body: "Open and manage authorized case records." },
  { href: "/review", title: "Review", body: "Confirm, edit, or flag model-extracted claims." },
  { href: "/civic-guidance", title: "Civic guidance", body: "Consult official procedural sources." },
  { href: "/reports", title: "Reports", body: "Preview and export source-linked reports." },
];

export default function HomePage() {
  return (
    <main className="mx-auto max-w-3xl px-6 py-16">
      <h1 className="text-3xl font-semibold">N-ATLAS Civic Evidence</h1>
      <p className="mt-3 text-sm text-muted-foreground">
        Organize interview testimony and civic incident reports into reviewable,
        source-linked records. Extracted claims stay attributed and unverified
        until a human reviewer confirms them.
      </p>
      <ul className="mt-10 grid gap-4 sm:grid-cols-2">
        {sections.map((section) => (
          <li key={section.href} className="rounded-lg border p-4">
            <Link href={section.href} className="font-medium underline-offset-2 hover:underline">
              {section.title}
            </Link>
            <p className="mt-1 text-sm text-muted-foreground">{section.body}</p>
          </li>
        ))}
      </ul>
    </main>
  );
}
