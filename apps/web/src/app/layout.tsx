import Link from "next/link";

import "./globals.css";

export const metadata = {
  title: "N-ATLAS Civic Evidence",
  description: "A source-linked workspace for reviewing civic evidence.",
};

const navigation = [
  { href: "/", label: "Overview", icon: "◫" },
  { href: "/cases", label: "Case files", icon: "▤" },
  { href: "/review", label: "Review queue", icon: "✓" },
  { href: "/civic-guidance", label: "Civic guidance", icon: "⌕" },
  { href: "/reports", label: "Reports", icon: "▧" },
];

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div className="app-frame">
          <aside className="sidebar">
            <Link href="/" className="brand-lockup" aria-label="N-ATLAS home">
              <span className="brand-mark">N</span>
              <span className="brand-copy">
                <strong>N-ATLAS</strong>
                <small>CIVIC EVIDENCE</small>
              </span>
            </Link>

            <div className="workspace-label">WORKSPACE</div>
            <nav className="primary-nav" aria-label="Primary navigation">
              {navigation.map((item) => (
                <Link href={item.href} key={item.href} className="nav-link">
                  <span className="nav-icon" aria-hidden="true">{item.icon}</span>
                  <span>{item.label}</span>
                </Link>
              ))}
            </nav>

            <div className="sidebar-bottom">
              <div className="trust-note">
                <span className="trust-dot" />
                <div>
                  <strong>Evidence, not verdicts</strong>
                  <p>Every claim stays attributed and reviewable.</p>
                </div>
              </div>
              <div className="user-chip">
                <span className="avatar">R</span>
                <span><strong>Reviewer</strong><small>Local workspace</small></span>
                <span className="user-menu" aria-hidden="true">···</span>
              </div>
            </div>
          </aside>

          <div className="app-main">
            <header className="topbar">
              <div className="breadcrumb"><span>Workspace</span><span className="crumb-divider">/</span><strong>Civic evidence</strong></div>
              <div className="topbar-right">
                <span className="environment-badge"><span /> Demo environment</span>
                <span className="topbar-date">Private review workspace</span>
              </div>
            </header>
            <div className="page-content">{children}</div>
          </div>
        </div>
      </body>
    </html>
  );
}
