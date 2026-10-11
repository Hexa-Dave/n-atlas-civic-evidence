# Guards against silent output regressions across model versions.
import pytest


@pytest.mark.skip(reason="Requires a configured N-ATLAS endpoint and recorded fixtures.")
def test_claim_extraction_regression():
    raise AssertionError("Replace with a golden-output comparison once fixtures exist.")
