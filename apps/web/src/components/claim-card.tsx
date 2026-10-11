export type ReviewStatus = "unverified" | "accepted" | "edited" | "rejected" | "flagged";

export interface ClaimCardProps {
  id: string;
  text: string;
  status: ReviewStatus;
  sourceSegmentId?: string;
  onSelect?: (claimId: string) => void;
}

const STATUS_LABELS: Record<ReviewStatus, string> = {
  unverified: "Unverified",
  accepted: "Human-reviewed",
  edited: "Human-edited",
  rejected: "Rejected",
  flagged: "Flagged",
};

/**
 * Renders a single extracted claim with its review status. A model-extracted
 * claim is never shown as a confirmed fact.
 */
export function ClaimCard({ id, text, status, sourceSegmentId, onSelect }: ClaimCardProps) {
  return (
    <article
      className="cursor-pointer rounded-lg border p-4"
      onClick={() => onSelect?.(id)}
      aria-label={`Claim ${id}`}
    >
      <div className="flex items-center justify-between gap-3">
        <span className="text-xs uppercase tracking-wide text-muted-foreground">Model-extracted</span>
        <span className="rounded-full border px-2 py-0.5 text-xs">{STATUS_LABELS[status]}</span>
      </div>
      <p className="mt-2 text-sm leading-relaxed">{text}</p>
      {sourceSegmentId ? (
        <footer className="mt-2 text-xs text-muted-foreground">Source: {sourceSegmentId}</footer>
      ) : (
        <footer className="mt-2 text-xs text-destructive">No source segment linked.</footer>
      )}
    </article>
  );
}
