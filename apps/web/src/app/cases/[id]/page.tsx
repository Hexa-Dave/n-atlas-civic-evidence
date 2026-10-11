"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { AudioPlayer } from "@/components/audio-player";
import { ClaimCard } from "@/components/claim-card";
import { EvidenceTimeline } from "@/components/evidence-timeline";
import { TranscriptViewer } from "@/components/transcript-viewer";
import { backendApi, CaseResponse, ClaimResponse } from "@/lib/api-client";
import { demoCases, demoClaims } from "@/lib/demo-data";

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

export default function CaseDetailPage() {
  const params = useParams<{ id: string }>();
  const caseId = Array.isArray(params?.id) ? params.id[0] : params?.id;
  const [caseRecord, setCaseRecord] = useState<CaseResponse | null>(demoCases[0] as unknown as CaseResponse);
  const [claims, setClaims] = useState<ClaimResponse[]>([]);

  useEffect(() => {
    if (!caseId) return;

    async function loadCase() {
      try {
        const result = await backendApi.getCase(caseId);
        setCaseRecord(result);
      } catch {
        setCaseRecord(demoCases[0] as unknown as CaseResponse);
      }

      try {
        const result = await backendApi.listClaims(caseId);
        setClaims(result);
      } catch {
        setClaims(
          demoClaims.map((claim) => ({
            id: claim.id,
            case_id: caseId,
            text: claim.text,
            status: claim.status,
            source_segment_id: claim.sourceSegmentId,
            confidence: claim.confidence,
          })),
        );
      }
    }

    loadCase();
  }, [caseId]);

  const displayClaims = claims.length > 0 ? claims : demoClaims.map((claim) => ({
    id: claim.id,
    case_id: caseId ?? "demo-case",
    text: claim.text,
    status: claim.status,
    source_segment_id: claim.sourceSegmentId,
    confidence: claim.confidence,
  }));

  return (
    <main className="mx-auto max-w-6xl px-6 py-12">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-wide text-muted-foreground">Case detail</p>
          <h1 className="text-3xl font-semibold">{caseRecord?.title ?? "Case"}</h1>
        </div>
        <Link href="/cases" className="rounded border px-3 py-2 text-sm hover:bg-muted">
          Back to cases
        </Link>
      </div>

      <p className="mb-6 max-w-2xl text-sm text-muted-foreground">{caseRecord?.description ?? "No description provided."}</p>

      <div className="content-grid">
        <section className="content-stack">
          <AudioPlayer
            segments={[
              { id: "segment-02", startSeconds: 18, endSeconds: 32 },
              { id: "segment-04", startSeconds: 42, endSeconds: 54 },
            ]}
          />
          <TranscriptViewer segments={transcriptSegments} />
          <EvidenceTimeline events={timelineEvents} />
        </section>

        <div className="claim-list">
          {displayClaims.map((claim) => (
            <ClaimCard
              key={claim.id}
              id={claim.id}
              text={claim.text}
              status={claim.status as any}
              sourceSegmentId={claim.source_segment_id ?? undefined}
            />
          ))}
        </div>
      </div>
    </main>
  );
}
