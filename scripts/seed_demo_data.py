# Loads synthetic demo data. Never use real interview or incident data here.
from __future__ import annotations

import argparse

from civic_evidence.dependencies import initialize_database
from civic_evidence.schemas.case import CaseCreate
from civic_evidence.services.case_service import CaseService


DEMO_CASES = [
    {
        "title": "Demo interview",
        "description": "Synthetic intake describing a reporting delay and documentation requirement.",
        "consent_recorded": True,
    },
    {
        "title": "Demo incident report",
        "description": "Synthetic incident summary requiring review and civic guidance.",
        "consent_recorded": True,
    },
]


def main(confirm: bool, actor_id: str = "seed-script") -> list[str]:
    if not confirm:
        print("Refusing to seed without --confirm (this writes to the local database).")
        return []

    initialize_database()
    from civic_evidence.dependencies import _SessionLocal

    if _SessionLocal is None:
        raise RuntimeError("Database session factory was not initialized")

    created: list[str] = []
    with _SessionLocal() as db:
        service = CaseService(db)
        for payload in DEMO_CASES:
            case = service.create_case(CaseCreate(**payload), actor_id=actor_id)
            created.append(case.id)
            print(f"Created case {case.id}: {case.title}")
    return created


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed synthetic demo data.")
    parser.add_argument("--confirm", action="store_true", help="Confirm writing demo data")
    parser.add_argument("--actor-id", default="seed-script", help="Actor to attribute to the seeded cases")
    args = parser.parse_args()
    main(args.confirm, actor_id=args.actor_id)
