export interface TranscriptSegment {
  id: string;
  speaker?: string;
  startSeconds?: number;
  endSeconds?: number;
  text: string;
  claimIds?: string[];
}

export interface TranscriptViewerProps {
  segments: TranscriptSegment[];
  activeSegmentId?: string;
  onSegmentClick?: (segmentId: string) => void;
}

/**
 * Displays transcript text with links back to the source claims. Segments are
 * shown as written; do not silently rewrite witness statements here.
 */
export function TranscriptViewer({ segments, activeSegmentId, onSegmentClick }: TranscriptViewerProps) {
  if (segments.length === 0) {
    return <p className="text-sm text-muted-foreground">No transcript available yet.</p>;
  }

  return (
    <section aria-label="Transcript" className="space-y-3">
      {segments.map((segment) => {
        const active = segment.id === activeSegmentId;
        return (
          <article
            key={segment.id}
            onClick={() => onSegmentClick?.(segment.id)}
            className={`transcript-segment rounded-md border p-3 ${active ? "is-active" : ""}`}
          >
            {segment.speaker ? (
              <header className="text-xs font-medium text-muted-foreground">{segment.speaker}</header>
            ) : null}
            <p className="mt-1 text-sm leading-relaxed">{segment.text}</p>
          </article>
        );
      })}
    </section>
  );
}
