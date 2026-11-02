import json

from tests.direct.conftest import to_hex


DATASET_ID = "acme/vision-1-dataset"
DATASET_CARD = "https://docs.example.com/acme/vision-1/dataset-card"
DATASHEET = "https://docs.example.com/acme/vision-1/datasheet"
POLICY = "https://buyer.example.com/data-procurement-policy"


def _mock_evidence(vm, payload):
    vm.mock_web(
        r".*docs\.example\.com/acme/vision-1/dataset-card.*",
        {"status": 200, "body": "Intended use: classification. License: CC-BY-4.0."},
    )
    vm.mock_web(
        r".*docs\.example\.com/acme/vision-1/datasheet.*",
        {"status": 200, "body": "Provenance, PII handling, quality checks described."},
    )
    vm.mock_web(
        r".*buyer\.example\.com/data-procurement-policy.*",
        {"status": 200, "body": "High-sensitivity datasets require provenance."},
    )
    vm.mock_llm(r".*DATASET CARD AUDIT.*", json.dumps(payload))


def _register(contract, vm, provider, required_tier=3, required_mask=127):
    vm.sender = provider
    contract.register_dataset(
        DATASET_ID,
        DATASET_CARD,
        DATASHEET,
        POLICY,
        required_tier,
        required_mask,
    )


FULL = {
    "intended_use": True,
    "provenance": True,
    "license": True,
    "pii_handling": True,
    "data_quality": True,
    "limitations": True,
    "update_cadence": True,
}


def test_approves_when_all_required_disclosures_are_present(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/dataset_card_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(
        direct_vm,
        {"risk_tier": 2, "disclosures": FULL, "source_consistency": "consistent", "summary": "Complete."},
    )
    contract.assess(DATASET_ID)

    result = contract.get_assessment(DATASET_ID)
    assert result["state"] == 1
    assert result["decision"] == 1
    assert result["missing_mask"] == 0
    assert result["round"] == 1
    assert contract.is_conformant(DATASET_ID) is True


def test_marks_conditional_when_a_disclosure_is_missing(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/dataset_card_gate.py")
    _register(contract, direct_vm, direct_alice)
    payload = dict(FULL)
    payload["update_cadence"] = False
    _mock_evidence(
        direct_vm,
        {"risk_tier": 2, "disclosures": payload, "source_consistency": "consistent", "summary": "No update cadence."},
    )
    contract.assess(DATASET_ID)

    result = contract.get_assessment(DATASET_ID)
    assert result["decision"] == 2
    assert result["missing_mask"] == 64
    assert contract.is_conformant(DATASET_ID) is False


def test_rejects_when_sources_conflict(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/dataset_card_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(
        direct_vm,
        {"risk_tier": 2, "disclosures": FULL, "source_consistency": "conflicting", "summary": "Conflict."},
    )
    contract.assess(DATASET_ID)

    result = contract.get_assessment(DATASET_ID)
    assert result["decision"] == 3
    assert result["source_consistency"] == "conflicting"


def test_rejects_risk_above_the_buyer_ceiling(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/dataset_card_gate.py")
    _register(contract, direct_vm, direct_alice, required_tier=2)
    _mock_evidence(
        direct_vm,
        {"risk_tier": 4, "disclosures": FULL, "source_consistency": "consistent", "summary": "Too risky."},
    )
    contract.assess(DATASET_ID)

    result = contract.get_assessment(DATASET_ID)
    assert result["decision"] == 3


def test_validator_accepts_matching_evidence(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/dataset_card_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(
        direct_vm,
        {"risk_tier": 2, "disclosures": FULL, "source_consistency": "consistent", "summary": "Complete."},
    )
    contract.assess(DATASET_ID)
    assert direct_vm.run_validator() is True


def test_validator_rejects_changed_evidence(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/dataset_card_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(
        direct_vm,
        {"risk_tier": 2, "disclosures": FULL, "source_consistency": "consistent", "summary": "Leader."},
    )
    contract.assess(DATASET_ID)

    direct_vm.clear_mocks()
    _mock_evidence(
        direct_vm,
        {"risk_tier": 4, "disclosures": FULL, "source_consistency": "consistent", "summary": "Validator differs."},
    )
    assert direct_vm.run_validator() is False
