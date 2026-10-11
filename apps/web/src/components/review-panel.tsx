"use client";

import type { ReviewStatus } from "./claim-card";

export interface ReviewPanelProps {
  claimId: string;
  status: ReviewStatus;
  note: string;
  onNoteChange?: (value: string) => void;
  onDecision?: (status: ReviewStatus) => void;
  disabled?: boolean;
}

const DECISIONS: ReviewStatus[] = ["accepted", "edited", "rejected", "flagged"];

/**
 * Reviewer controls for a single claim. Only an authorized reviewer should see
 * this panel; the backend must re-check authorization on submit.
 */
export function ReviewPanel({ claimId, status, note, onNoteChange, onDecision, disabled }: ReviewPanelProps) {
  return (
    <aside aria-label="Review panel" className="rounded-lg border p-4">
      <h2 className="text-sm font-semibold">Review claim {claimId}</h2>
      <p className="mt-1 text-xs text-muted-foreground">Current status: {status}</p>
      <label className="mt-3 block text-sm">
        Reviewer note
        <textarea
          className="mt-1 w-full rounded border p-2 text-sm"
          rows={3}
          value={note}
          disabled={disabled}
          onChange={(event) => onNoteChange?.(event.target.value)}
        />
      </label>
      <div className="review-actions">
        {DECISIONS.map((decision) => (
          <button
            key={decision}
            type="button"
            disabled={disabled}
            className="rounded border px-3 py-1.5 text-sm disabled:opacity-50"
            onClick={() => onDecision?.(decision)}
          >
            {decision}
          </button>
        ))}
      </div>
      <p className="mt-3 text-xs text-muted-foreground">
        Finalizing a report requires at least one human review.
      </p>
    </aside>
  );
}
