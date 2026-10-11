import Link from "next/link";

const sections = [
  { href: "/cases", icon: "▤", title: "Case files", body: "Open and manage authorized case records.", count: "01" },
  { href: "/review", icon: "✓", title: "Review claims", body: "Confirm, edit, or flag model-extracted claims.", count: "02" },
  { href: "/civic-guidance", icon: "⌕", title: "Civic guidance", body: "Consult official procedural sources.", count: "03" },
  { href: "/reports", icon: "▧", title: "Reports", body: "Preview and export source-linked reports.", count: "04" },
];

export default function HomePage() {
  return (
    <main className="home-page">
      <section className="home-hero">
        <div className="hero-copy">
          <p className="hero-eyebrow"><span /> Evidence workspace</p>
          <h1>Clarity for complex civic stories.</h1>
          <p className="hero-description">
            Organize testimony and incident reports into careful, source-linked records.
            Keep every claim reviewable, attributed, and in human hands.
          </p>
          <div className="hero-actions">
            <Link href="/cases">Explore case files <span aria-hidden="true">→</span></Link>
            <Link href="/review" className="secondary">Open review queue</Link>
          </div>
        </div>
        <aside className="hero-aside">
          <span className="hero-aside-label">A principle we work by</span>
          <strong>Evidence is not a verdict.</strong>
          <p>Model-extracted statements remain unverified until an authorized person reviews them.</p>
        </aside>
      </section>

      <div className="home-stats" aria-label="Workspace principles">
        <div className="stat-card">
          <span className="stat-icon" aria-hidden="true">⌁</span>
          <div><strong>Traceable</strong><span>Every claim links to its source</span></div>
        </div>
        <div className="stat-card">
          <span className="stat-icon" aria-hidden="true">◎</span>
          <div><strong>Human-led</strong><span>Review before report finalization</span></div>
        </div>
        <div className="stat-card">
          <span className="stat-icon" aria-hidden="true">≋</span>
          <div><strong>Clearly separated</strong><span>Guidance stays distinct from testimony</span></div>
        </div>
      </div>

      <div className="section-heading">
        <div><p>Workspace</p><h2>Continue with a workflow</h2></div>
        <Link href="/cases">View all areas <span aria-hidden="true">→</span></Link>
      </div>

      <div className="workflow-grid">
        {sections.map((section) => (
          <Link href={section.href} key={section.href} className="workflow-card">
            <div className="workflow-card-icon" aria-hidden="true">{section.icon}</div>
            <h3>{section.title}<span className="workflow-number">{section.count}</span></h3>
            <p>{section.body}</p>
          </Link>
        ))}
      </div>

      <div className="home-footnote">
        <span aria-hidden="true">✳</span>
        <span><strong>Responsible by design.</strong> This workspace supports documentation; it does not determine whether an allegation is true.</span>
      </div>
    </main>
  );
}
