export interface TimelineEvent {
  id: string;
  occurredAt: string;
  label: string;
  claimId?: string;
  confidence?: number;
}

export interface EvidenceTimelineProps {
  events: TimelineEvent[];
  onEventSelect?: (eventId: string) => void;
}

/**
 * Orders claims and documented events by time. Dates taken from testimony are
 * unverified unless corroborated by an official source.
 */
export function EvidenceTimeline({ events, onEventSelect }: EvidenceTimelineProps) {
  const ordered = [...events].sort((a, b) => a.occurredAt.localeCompare(b.occurredAt));

  return (
    <section aria-label="Evidence timeline" className="timeline-list">
      {ordered.map((event) => (
        <div key={event.id} className="flex gap-3" onClick={() => onEventSelect?.(event.id)}>
          <time className="w-28 shrink-0 text-xs text-muted-foreground">{event.occurredAt}</time>
          <div className="border-l pl-3 text-sm">{event.label}</div>
        </div>
      ))}
    </section>
  );
}
