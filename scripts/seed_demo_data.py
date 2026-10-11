# Loads synthetic demo data. Never use real interview or incident data here.
import argparse


DEMO_CASES = [
    {"id": "case-demo-001", "title": "Demo interview", "status": "in_review"},
    {"id": "case-demo-002", "title": "Demo incident report", "status": "draft"},
]


def main(confirm: bool) -> None:
    if not confirm:
        print("Refusing to seed without --confirm (this writes to the local database).")
        return
    raise NotImplementedError("Insert DEMO_CASES through the case service with synthetic content.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed synthetic demo data.")
    parser.add_argument("--confirm", action="store_true", help="Confirm writing demo data")
    args = parser.parse_args()
    main(args.confirm)
