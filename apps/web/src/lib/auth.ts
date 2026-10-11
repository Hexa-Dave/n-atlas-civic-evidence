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
  // Replace with a call to the backend session endpoint once implemented.
  return null;
}

export function canReview(user: SessionUser | null): boolean {
  return Boolean(user?.roles.includes("reviewer") || user?.roles.includes("admin"));
}
