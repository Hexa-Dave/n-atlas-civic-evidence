import pytest


@pytest.mark.skip(reason="Requires a built civic index.")
def test_every_guidance_statement_has_a_citation():
    raise AssertionError("Replace with a grounding check over recorded guidance fixtures.")


def test_search_requires_built_index(tmp_path):
    from civic_knowledge.retrieval.search import search

    with pytest.raises(RuntimeError):
        search("q", index_dir=str(tmp_path / "missing"))
