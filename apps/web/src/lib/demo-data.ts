export type ReviewStatus = "unverified" | "accepted" | "edited" | "rejected" | "flagged";

export interface CaseRecord {
  id: string;
  title: string;
  status: "draft" | "in_review" | "finalized";
  description: string;
}

export interface ClaimRecord {
  id: string;
  text: string;
  status: ReviewStatus;
  sourceSegmentId: string;
  confidence: number;
}

export interface SourceRecord {
  id: string;
  title: string;
  section: string;
  jurisdiction: string;
  excerpt: string;
  url: string;
}

export interface ReportRecord {
  title: string;
  status: "draft" | "final";
  sections: Array<{
    heading: string;
    body: string;
    citations: string[];
  }>;
}

export const demoCases: CaseRecord[] = [
  {
    id: "case-demo-001",
    title: "Demo interview",
    status: "in_review",
    description: "Witness account about polling access and procedural steps.",
  },
  {
    id: "case-demo-002",
    title: "Demo incident report",
    status: "draft",
    description: "Incident summary for civic guidance and review.",
  },
];

export const demoClaims: ClaimRecord[] = [
  {
    id: "claim-1",
    text: "The witness reported that he was told to wait an additional hour before receiving assistance.",
    status: "unverified",
    sourceSegmentId: "segment-02",
    confidence: 0.87,
  },
  {
    id: "claim-2",
    text: "The witness described a process requiring a photo ID to obtain the requested service.",
    status: "accepted",
    sourceSegmentId: "segment-04",
    confidence: 0.81,
  },
];

export const demoGuidance: SourceRecord[] = [
  {
    id: "src-1",
    title: "Voter registration procedure",
    section: "Registration requirements",
    jurisdiction: "US-XX",
    excerpt:
      "Eligible voters must register before the applicable deadline and provide required identification.",
    url: "https://example.gov/voter-registration",
  },
  {
    id: "src-2",
    title: "Public assistance access guidance",
    section: "Processing timelines",
    jurisdiction: "US-XX",
    excerpt:
      "Agencies must communicate the status of requests and the procedures for contesting a delay.",
    url: "https://example.gov/public-access-guidance",
  },
];

export const demoReport: ReportRecord = {
  title: "Case report",
  status: "final",
  sections: [
    {
      heading: "Testimony summary",
      body:
        "The witness reported a delay in receiving assistance and described a requirement to provide identification. These statements remain attributed to the witness and are marked as reviewed, not established fact.",
      citations: ["segment-02", "segment-04"],
    },
    {
      heading: "Official civic guidance",
      body:
        "Procedural guidance should be reviewed separately from witness statements and used to inform next steps, not to confirm facts.",
      citations: ["Voter registration procedure", "Public assistance access guidance"],
    },
  ],
};
