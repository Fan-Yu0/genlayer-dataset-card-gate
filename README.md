# Dataset Card Conformance Gate

A standalone GenLayer Intelligent Contract primitive for evidence-based dataset
procurement and marketplace admission.

A dataset provider registers a dataset card, a datasheet/documentation URL, a
buyer policy, a risk-tier ceiling, and a required disclosure set. Anyone can then
trigger `assess(dataset_id)`.

GenLayer validators independently fetch the dataset card, the datasheet, and the
policy, and an LLM extracts only structured evidence: risk tier, disclosure
bitmask, source consistency, and a short summary. The contract computes the final
decision deterministically.

## Decision logic

| Condition | Decision |
| --- | --- |
| Sources conflict or are insufficient | REJECTED |
| Extracted risk tier exceeds the buyer ceiling | REJECTED |
| Required disclosure is missing | CONDITIONAL |
| All checks pass | APPROVED |

## Disclosure bits

| Bit | Field |
| --- | --- |
| 1 | intended use |
| 2 | provenance |
| 4 | license |
| 8 | PII handling |
| 16 | data quality |
| 32 | limitations |
| 64 | update cadence |
| 127 | all seven fields |

## Why it is a reusable primitive

- Useful without a frontend; any registry, DAO, or procurement contract can call
  `is_conformant(dataset_id)`.
- Policy is data, not hard-coded business logic.
- Evidence extraction and the deterministic policy engine are separated, and the
  custom validator independently re-fetches the same sources.
- Fork it for models, APIs, or agent manifests by changing the disclosure bits.

## Local verification

```shell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
genvm-lint check contracts/dataset_card_gate.py
pytest tests/direct/ -v
```

## Deploy

### Studio

1. Open <https://studio.genlayer.com/>.
2. Create a new contract, paste `contracts/dataset_card_gate.py`, deploy with no
   constructor arguments.
3. Call `register_dataset` with real public dataset sources.
4. Call `assess(dataset_id)`.
5. Save the contract address and the deployment/assessment transaction hashes.

## Security notes

- Only HTTPS evidence URLs are accepted.
- Conflicting or incomplete evidence fails closed.
- The final decision is deterministic; the LLM cannot approve a dataset by
  returning a friendly summary.
- This contract records a procurement signal, not a legal certification.


## Current deployment

- Contract: `0xa5E1f8665F732edF2781D35F61E44a7Fd5753f45`
- Network: GenLayer StudioNet (gasless)
- Explorer: https://explorer-studio.genlayer.com/address/0xa5E1f8665F732edF2781D35F61E44a7Fd5753f45
- Deployment transaction: `0xf3bccaaf664be796d1c09062e40965c9e104dd2c128142302f0ad8d161bcaaf8`
- Live example: `squad` -> https://huggingface.co/datasets/rajpurkar/squad
- Registration transaction: `0x4faebb7af66c8eace65e31acb30d8a584ba544f5c4d2353428401f78c926e891`
- Assessment transaction: `0xc0b6c6d14ceb87ce1f1e61b19770e0603af4169a15b7877a230cca4b7bb3fa22`
- Assessment result: APPROVED (decision = 1), risk tier minimal, required_tier 3,
  required_mask 7, disclosure_mask 7, missing_mask 0, source consistency consistent,
  round 1.
