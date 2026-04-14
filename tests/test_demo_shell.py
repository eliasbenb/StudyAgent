import pytest

from study_agent_acp.demo_shell import (
    _extract_keeper_row,
    _infer_phenotype_name,
    _slugify,
    _split_csv,
    _split_query_text,
)


def test_slugify_normalizes_text() -> None:
    assert _slugify("Acute Gastrointestinal Bleeding") == "acute-gastrointestinal-bleeding"
    assert _slugify("   ") == "result"


def test_split_csv_trims_empty_values() -> None:
    assert _split_csv("Condition, Observation , , Procedure") == ["Condition", "Observation", "Procedure"]


def test_split_query_text_uses_semicolons() -> None:
    assert _split_query_text("GI bleed; abdominal pain ; melena") == ["GI bleed", "abdominal pain", "melena"]


def test_extract_keeper_row_from_rows_payload() -> None:
    payload = {
        "rows": [
            {"generatedId": "1", "presentation": "A"},
            {"generatedId": "2", "presentation": "B"},
        ]
    }
    assert _extract_keeper_row(payload, 1)["generatedId"] == "2"


def test_extract_keeper_row_from_nested_full_result() -> None:
    payload = {
        "full_result": {
            "rows": [
                {"generatedId": "1", "visitContext": "Inpatient Visit"},
            ]
        }
    }
    assert _extract_keeper_row(payload, 0)["visitContext"] == "Inpatient Visit"


def test_extract_keeper_row_accepts_direct_keeper_row() -> None:
    payload = {"keeper_row": {"generatedId": "5", "presentation": "GI hemorrhage"}}
    assert _extract_keeper_row(payload, 0)["generatedId"] == "5"


def test_extract_keeper_row_rejects_missing_rows() -> None:
    with pytest.raises(ValueError, match="could not locate a keeper row"):
        _extract_keeper_row({"concept_sets": []}, 0)


def test_extract_keeper_row_checks_row_index() -> None:
    with pytest.raises(ValueError, match="out of range"):
        _extract_keeper_row({"rows": [{"generatedId": "1"}]}, 2)


def test_infer_phenotype_name_prefers_top_level() -> None:
    assert _infer_phenotype_name({"phenotype": "GI bleed"}) == "GI bleed"


def test_infer_phenotype_name_uses_nested_full_result() -> None:
    payload = {"full_result": {"phenotype_name": "Intracranial bleeding"}}
    assert _infer_phenotype_name(payload) == "Intracranial bleeding"
