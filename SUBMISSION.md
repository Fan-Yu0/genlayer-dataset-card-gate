# Portal submission - Dataset Card Conformance Gate

## Category

Developer -> Intelligent Contract

## Contribution date

2026-11-02

## Description (987/1000)

Dataset Card Conformance Gate is a reusable GenLayer primitive for evidence-backed dataset procurement. A provider registers a dataset card, a datasheet URL, a buyer policy, a risk-tier ceiling, and a required disclosure set. Anyone can trigger an assessment. Validators independently fetch all three sources; an LLM extracts only the risk tier, disclosure mask, source consistency, and a summary. Deterministic contract code applies a fixed policy: conflicting or insufficient evidence is rejected, a risk tier above the buyer ceiling is rejected, a missing required disclosure is conditional, and a complete submission is approved. The custom validator re-fetches the evidence and compares the decision-bearing fields, so the model cannot approve a dataset by formatting a friendly response. Other contracts can consume is_conformant(dataset_id). The repository includes source, tests, deployment instructions, and a clear state model for data marketplaces, agent registries, and DAOs.

## Deployed evidence

- Public source repository: https://github.com/Fan-Yu0/genlayer-dataset-card-gate
- Contract: TBD
- Explorer: TBD
- Deployment transaction: TBD
- Successful assessment transaction: TBD

## First live example

- dataset_id: TBD
- dataset_card_url: TBD
- datasheet_url: TBD
- policy_url: https://www.nist.gov/itl/ai-risk-management-framework
- required_tier: 3
- required_mask: 7 (intended_use | provenance | license)
