"use client";

import { useRef } from "react";

export interface AudioSegment {
  id: string;
  startSeconds: number;
  endSeconds: number;
}

export interface AudioPlayerProps {
  src: string;
  segments?: AudioSegment[];
  onSegmentSelect?: (segmentId: string) => void;
}

function formatTime(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = Math.floor(totalSeconds % 60);
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
}

/**
 * Plays permitted case audio and lists time-aligned segments. The backend
 * remains the source of truth for who may access the underlying audio.
 */
export function AudioPlayer({ src, segments = [], onSegmentSelect }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null);

  return (
    <section aria-label="Case audio" className="rounded-lg border p-4">
      <audio ref={audioRef} controls preload="metadata" src={src} className="w-full" />
      {segments.length > 0 ? (
        <ul className="mt-3 space-y-1 text-sm">
          {segments.map((segment) => (
            <li key={segment.id}>
              <button
                type="button"
                className="underline-offset-2 hover:underline"
                onClick={() => onSegmentSelect?.(segment.id)}
              >
                {formatTime(segment.startSeconds)} - {formatTime(segment.endSeconds)}
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-3 text-sm text-muted-foreground">No time-aligned segments available.</p>
      )}
    </section>
  );
}
