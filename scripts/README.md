# Developer and verification scripts

This directory contains repeatable helper scripts for local setup, tests, demo data, and deployment verification.

Possible scripts include `setup_dev.sh`, `seed_demo_data.py`, `run_local.sh`, `run_tests.sh`, and `verify_deployment.py`.

Use explicit arguments and fail safely when configuration is missing. Scripts must not print secrets, silently overwrite private data, or upload user material without clear authorization. Document prerequisites and expected outputs in each script's help text or the root README.

Do not add scripts that depend on unimplemented commands and then present them as working. Test each script in a clean environment before marking it ready.
