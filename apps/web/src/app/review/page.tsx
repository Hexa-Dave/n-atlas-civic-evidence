"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { AudioPlayer } from "@/components/audio-player";
import { ClaimCard } from "@/components/claim-card";
import { EvidenceTimeline } from "@/components/evidence-timeline";
import { ReviewPanel } from "@/components/review-panel";
import { TranscriptViewer } from "@/components/transcript-viewer";
import { backendApi, ClaimResponse } from "@/lib/api-client";
import { demoClaims } from "@/lib/demo-data";

const transcriptSegments = [
  {
    id: "segment-02",
    speaker: "Witness",
    text: "I was told I had to wait another hour before anyone could help me with my request.",
  },
  {
    id: "segment-04",
    speaker: "Witness",
    text: "The clerk said I needed to bring my photo ID before the process could continue.",
  },
];

const timelineEvents = [
  { id: "event-01", occurredAt: "2026-01-07", label: "Initial intake completed", claimId: "claim-1" },
  { id: "event-02", occurredAt: "2026-01-07", label: "Witness described document requirement", claimId: "claim-2" },
];

export default function ReviewPage() {
  const [claims, setClaims] = useState<ClaimResponse[]>([]);
  const [selectedClaimId, setSelectedClaimId] = useState(demoClaims[0].id);
  const [note, setNote] = useState("Needs confirmation against the official procedure and case record.");

  useEffect(() => {
    async function loadClaims() {
      try {
        const result = await backendApi.listClaims("case-demo-001");
        if (result.length > 0) {
          setClaims(result);
          setSelectedClaimId(result[0].id);
        }
      } catch {
        setClaims(
          demoClaims.map((claim) => ({
            id: claim.id,
            case_id: "case-demo-001",
            text: claim.text,
            status: claim.status,
            source_segment_id: claim.sourceSegmentId,
            confidence: claim.confidence,
          })),
        );
      }
    }

    loadClaims();
  }, []);

  const displayClaims = claims.length > 0 ? claims : demoClaims.map((claim) => ({
    id: claim.id,
    case_id: "case-demo-001",
    text: claim.text,
    status: claim.status,
    source_segment_id: claim.sourceSegmentId,
    confidence: claim.confidence,
  }));
  const selectedClaim = displayClaims.find((claim) => claim.id === selectedClaimId) ?? displayClaims[0];

  return (
    <main className="mx-auto max-w-6xl px-6 py-12">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-wide text-muted-foreground">Review</p>
          <h1 className="text-3xl font-semibold">Claim review workspace</h1>
        </div>
        <Link href="/cases" className="rounded border px-3 py-2 text-sm hover:bg-muted">
          Back to cases
        </Link>
      </div>

      <div className="content-grid">
        <section className="content-stack">
          <AudioPlayer
            segments={[
              { id: "segment-02", startSeconds: 18, endSeconds: 32 },
              { id: "segment-04", startSeconds: 42, endSeconds: 54 },
            ]}
            onSegmentSelect={setSelectedClaimId}
          />
          <TranscriptViewer
            segments={transcriptSegments}
            activeSegmentId={selectedClaim?.source_segment_id ?? undefined}
            onSegmentClick={setSelectedClaimId}
          />
          <EvidenceTimeline
            events={timelineEvents}
            onEventSelect={(eventId) => {
              const event = timelineEvents.find((item) => item.id === eventId);
              if (event?.claimId) {
                setSelectedClaimId(event.claimId);
              }
            }}
          />
        </section>

        <div className="claim-list">
          {displayClaims.map((claim) => (
            <ClaimCard
              key={claim.id}
              id={claim.id}
              text={claim.text}
              status={claim.status as any}
              sourceSegmentId={claim.source_segment_id ?? undefined}
              onSelect={setSelectedClaimId}
            />
          ))}
          {selectedClaim ? (
            <ReviewPanel
              claimId={selectedClaim.id}
              status={selectedClaim.status as any}
              note={note}
              onNoteChange={setNote}
              onDecision={(status) => {
                console.info(`Decision recorded for ${selectedClaim.id}: ${status}`);
              }}
            />
          ) : null}
        </div>
      </div>
    </main>
  );
}
