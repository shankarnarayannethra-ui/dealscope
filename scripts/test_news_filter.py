#!/usr/bin/env python3
"""Small regression test for M&A headline precision."""
from update_news import is_high_confidence_ma

SHOULD_ACCEPT = [
    "Oracle agrees to acquire Acme Cloud for $4.2 billion",
    "Alpha Corp acquires Beta Systems",
    "Northstar and BluePeak agree to merge",
    "Atlas to merge with Horizon in a $9 billion transaction",
    "MegaBank launches takeover bid for Regional Bank",
    "Vertex completes acquisition of Signal Labs",
]

SHOULD_REJECT = [
    "Senate leaders reach budget deal",
    "Yankees sign player to record deal",
    "Company announces partnership with cloud provider",
    "Five acquisition targets investors should watch",
    "Marketing team lowers customer acquisition cost",
    "Developer fixes Git merge request",
    "Fund makes strategic investment in startup",
    "Company may acquire rival next year",
]

for headline in SHOULD_ACCEPT:
    assert is_high_confidence_ma(headline, "Reuters"), f"Should accept: {headline}"

for headline in SHOULD_REJECT:
    assert not is_high_confidence_ma(headline, "Reuters"), f"Should reject: {headline}"

print("All news filter tests passed.")
