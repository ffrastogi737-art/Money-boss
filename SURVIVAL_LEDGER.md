# SURVIVAL LEDGER (append-only; ISO-8601 UTC timestamps)

START_DATE: 2026-11-18T11:09:00Z
14_DAY_REVIEW_DATE: 2026-12-02T11:09:00Z
30_DAY_SCALE_DATE: 2026-12-18T11:09:00Z
TOTAL_GROSS_REVENUE: $0.00
TOTAL_NET_REVENUE: $0.00
TOTAL_VERIFIED_PAYOUT: $0.00

## Pipeline
PROSPECTS -> QUALIFIED_LEADS -> VERIFIED_SALE -> PAYOUT_PENDING -> VERIFIED_PAYOUT
0 -> 0 -> 0 -> 0 -> 0   [VERIFIED: nothing yet]

## Active Bets
| Bet | Role | Distribution channel (first 100 visits) | Monetization path | Status | Net revenue | Claude efficiency |
|---|---|---|---|---|---|---|
| salary-calculator-india | PRIMARY | Reddit r/IndiaInvestments & r/personalfinanceindia answers, Quora, X; SEO long-tail "old vs new regime" | Affiliate (needs owner link in config.js) | TRACTION_UNKNOWN | $0.00 | 1 run |
| gst-invoice-generator | SECONDARY | Freelancer communities (Reddit r/IndiaFreelancers-type subs, LinkedIn); SEO "GST invoice generator" | Affiliate accounting-software referral (needs owner link) | TRACTION_UNKNOWN | $0.00 | 1 run |
| hra-exemption-calculator | SECONDARY-2 | Same threads as salary tool (HRA/rent questions on Reddit/Quora); SEO "HRA exemption calculator" | Same affiliate offers (pending owner links) | TRACTION_UNKNOWN | $0.00 | 1 run |

## Live URLs
(audit.py reads lines of the form `- URL: <url> | <status>`)
- URL: https://ffrastogi737-art.github.io/Money-boss/ | [VERIFIED live 2026-11-18T11:18:28Z, HTTP 200 via watchdog] hub
- URL: https://ffrastogi737-art.github.io/Money-boss/salary-calculator-india/ | [VERIFIED live 2026-11-18T11:18:28Z, HTTP 200 via watchdog]
- URL: https://ffrastogi737-art.github.io/Money-boss/gst-invoice-generator/ | [VERIFIED live 2026-11-18T11:18:28Z, HTTP 200 via watchdog]
- URL: https://ffrastogi737-art.github.io/Money-boss/hra-exemption-calculator/ | [EXECUTED - PAGES_BUILDING]

## Bet scoring (0-5; [ESTIMATED], web research not yet run — demand is a prior, validate with real analytics)
| Candidate | Demand | Monetize | Distribution | Build speed | Total |
|---|---|---|---|---|---|
| In-hand salary calculator (India) | 5 | 3 | 4 | 5 | 17 |
| GST invoice generator | 4 | 3 | 3 | 5 | 15 |
| Image compressor | 4 | 1 | 2 | 4 | 11 |

## Log
- 2026-11-18T11:09:00Z [EXECUTED] Cycle 1: infra built, 2 MVPs written (not yet confirmed live).

- 2026-11-18T11:25:00Z [EXECUTED] Pages live (watchdog 200s). Salary FAQ + distribution drafts (projects/distribution/posts.md) pushed. Affiliate/GoatCounter blocked on owner accounts.
- 2026-11-18T12:00:00Z [EXECUTED] Added hra-exemption-calculator (3rd bet), linked from hub + salary tool. Owner declined scheduled daily run; runs are manual.

## VERIFIED_PAYOUT:
(none)
