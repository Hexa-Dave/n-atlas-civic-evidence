/**
 * Client-side session helpers. Authentication is ultimately enforced by the
 * backend; these utilities only gate what the UI renders.
 */

export interface SessionUser {
  id: string;
  name: string;
  roles: string[];
}

export async function getSession(): Promise<SessionUser | null> {
  if (typeof window === "undefined") {
    return null;
  }

  const stored = window.localStorage.getItem("civic_evidence_session");
  if (stored) {
    try {
      const parsed = JSON.parse(stored) as SessionUser;
      if (parsed?.id) {
        return parsed;
      }
    } catch {
      return null;
    }
  }

  return {
    id: "local-dev-user",
    name: "Local reviewer",
    roles: ["reviewer", "admin"],
  };
}

export function canReview(user: SessionUser | null): boolean {
  return Boolean(user?.roles.includes("reviewer") || user?.roles.includes("admin"));
}
