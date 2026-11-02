# Portal submission - Dataset Card Conformance Gate

## Category

Developer -> Intelligent Contract

## Contribution date

2026-11-02

## Description (987/1000)

Dataset Card Conformance Gate is a reusable GenLayer primitive for evidence-backed dataset procurement. A provider registers a dataset card, a datasheet URL, a buyer policy, a risk-tier ceiling, and a required disclosure set. Anyone can trigger an assessment. Validators independently fetch all three sources; an LLM extracts only the risk tier, disclosure mask, source consistency, and a summary. Deterministic contract code applies a fixed policy: conflicting or insufficient evidence is rejected, a risk tier above the buyer ceiling is rejected, a missing required disclosure is conditional, and a complete submission is approved. The custom validator re-fetches the evidence and compares the decision-bearing fields, so the model cannot approve a dataset by formatting a friendly response. Other contracts can consume is_conformant(dataset_id). The repository includes source, tests, deployment instructions, and a clear state model for data marketplaces, agent registries, and DAOs.

## Deployed evidence

- Public source repository: https://github.com/Fan-Yu0/genlayer-dataset-card-gate
- Contract: `0xa5E1f8665F732edF2781D35F61E44a7Fd5753f45`
- Explorer: https://explorer-studio.genlayer.com/address/0xa5E1f8665F732edF2781D35F61E44a7Fd5753f45
- Deployment transaction: `0xf3bccaaf664be796d1c09062e40965c9e104dd2c128142302f0ad8d161bcaaf8`
- Successful assessment transaction: `0xc0b6c6d14ceb87ce1f1e61b19770e0603af4169a15b7877a230cca4b7bb3fa22`
- Registration transaction: `0x4faebb7af66c8eace65e31acb30d8a584ba544f5c4d2353428401f78c926e891`
- Result: APPROVED (decision = 1), risk tier minimal, required_tier 3, disclosure_mask 7, missing_mask 0, source_consistency consistent, round 1

## First live example

- dataset_id: squad
- dataset_card_url: https://huggingface.co/datasets/rajpurkar/squad
- datasheet_url: https://arxiv.org/abs/1606.05250
- policy_url: https://www.nist.gov/itl/ai-risk-management-framework
- required_tier: 3
- required_mask: 7 (intended_use | provenance | license)
