#!/usr/bin/env python3
"""Fetch high-confidence M&A headlines and write browser-ready generated-deals.js.

The updater intentionally favors precision over volume. A story is accepted only when
its headline resembles an actual acquisition/merger announcement and passes noise filters.
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "generated-deals.js"

# Quoted/action-oriented phrases reduce generic stories returned by Google News.
QUERY = (
    '("to acquire" OR "agrees to acquire" OR acquires OR "to buy" OR '
    '"agrees to buy" OR "acquisition of" OR "merger with" OR '
    '"agree to merge" OR "takeover bid" OR "buyout of") when:7d'
)
DEFAULT_FEED = "https://news.google.com/rss/search?" + urllib.parse.urlencode(
    {"q": QUERY, "hl": "en-US", "gl": "US", "ceid": "US:en"}
)
FEED = os.environ.get("DEALSCOPE_FEED_URL", DEFAULT_FEED)

# Optional: set DEALSCOPE_ALLOWED_SOURCES="Reuters,Bloomberg,CNBC" in GitHub Actions.
ALLOWED_SOURCES = {
    value.strip().lower()
    for value in os.environ.get("DEALSCOPE_ALLOWED_SOURCES", "").split(",")
    if value.strip()
}

# A headline must match one of these transaction-shaped expressions.
TRANSACTION_PATTERNS = [
    re.compile(
        r"^(?P<a>.+?)\s+(?:agrees?|plans?|moves?|set|seeks?|expected)\s+to\s+"
        r"(?:acquire|buy|purchase|take over)\s+(?P<t>.+?)(?:\s+for\s+|\s+in\s+a\s+|$)",
        re.I,
    ),
    re.compile(
        r"^(?P<a>.+?)\s+(?:will\s+)?(?:acquires?|buys?|purchases?|takes over)\s+"
        r"(?P<t>.+?)(?:\s+for\s+|\s+in\s+a\s+|$)",
        re.I,
    ),
    re.compile(
        r"^(?P<a>.+?)\s+(?:completes?|closes?)\s+(?:the\s+)?acquisition\s+of\s+"
        r"(?P<t>.+?)(?:\s+for\s+|$)",
        re.I,
    ),
    re.compile(
        r"^(?P<a>.+?)\s+(?:announces?|confirms?)\s+(?:the\s+)?acquisition\s+of\s+"
        r"(?P<t>.+?)(?:\s+for\s+|$)",
        re.I,
    ),
    re.compile(
        r"^(?P<a>.+?)\s+(?:and|&)\s+(?P<t>.+?)\s+(?:agree|plan)\s+to\s+merge\b",
        re.I,
    ),
    re.compile(
        r"^(?P<a>.+?)\s+to\s+merge\s+with\s+(?P<t>.+?)(?:\s+in\s+a\s+|$)",
        re.I,
    ),
    re.compile(
        r"^(?P<a>.+?)\s+launches?\s+(?:a\s+)?(?:takeover\s+)?bid\s+for\s+(?P<t>.+?)(?:\s+worth\s+|$)",
        re.I,
    ),
    re.compile(
        r"^(?P<a>.+?)['’]s\s+(?:acquisition|buyout)\s+of\s+(?P<t>.+?)(?:\s+for\s+|$)",
        re.I,
    ),
]

# Strong noise categories that frequently contain acquisition-like language.
EXCLUDE = re.compile(
    r"\b("
    r"trade deal|peace deal|budget deal|debt deal|tax deal|labor deal|union deal|"
    r"sponsorship deal|broadcast deal|record deal|endorsement deal|licensing deal|"
    r"distribution deal|supply deal|contract deal|real estate deal|property deal|"
    r"arms deal|prisoner deal|plea deal|settlement deal|sports deal|transfer deal|"
    r"free agent|draft pick|player|coach|quarterback|striker|midfielder|pitcher|"
    r"job merger|data merge|merge request|traffic merger|lane merger|git merge|"
    r"partnership|partners with|collaboration|joint venture|funding round|raises?\s+\$|"
    r"investment in|minority stake|strategic investment|loan|bond offering|refinancing|"
    r"customer acquisition|user acquisition|talent acquisition|land acquisition|"
    r"acquisition cost|acquisition strategy|acquisition target(?:s)?|could acquire|"
    r"may acquire|might acquire|rumored to|reportedly considering|explores? acquisition"
    r")\b",
    re.I,
)

BAD_PARTY = re.compile(
    r"^(a|an|the|its|company|firm|business|stake|assets?|operations?|portfolio|"
    r"technology|platform|unit|division|shares?|remaining stake|majority stake|"
    r"minority stake|customers?|users?|talent|land|property)$",
    re.I,
)


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", " ", text or ""))).strip()


def split_source(title: str) -> tuple[str, str]:
    parts = title.rsplit(" - ", 1)
    return (parts[0].strip(), parts[1].strip()) if len(parts) == 2 else (title.strip(), "Google News")


def source_allowed(source_name: str) -> bool:
    if not ALLOWED_SOURCES:
        return True
    source = source_name.lower()
    return any(allowed in source for allowed in ALLOWED_SOURCES)


def trim_party(value: str) -> str:
    value = clean(value)
    # Remove common trailing transaction descriptors captured before a value phrase.
    value = re.sub(r"\s+(?:in|under)\s+(?:a|an|the)\s*$", "", value, flags=re.I)
    return value.strip(" ,:;-–—")[:100]


def infer_parties(headline: str) -> tuple[str, str] | None:
    for pattern in TRANSACTION_PATTERNS:
        match = pattern.search(headline)
        if not match:
            continue
        acquirer = trim_party(match.group("a"))
        target = trim_party(match.group("t"))
        if len(acquirer) < 2 or len(target) < 2:
            return None
        if BAD_PARTY.fullmatch(acquirer) or BAD_PARTY.fullmatch(target):
            return None
        # Reject overly sentence-like captures; company names are normally concise.
        if len(acquirer.split()) > 12 or len(target.split()) > 12:
            return None
        return acquirer, target
    return None


def is_high_confidence_ma(headline: str, source_name: str) -> tuple[str, str] | None:
    if not source_allowed(source_name):
        return None
    if EXCLUDE.search(headline):
        return None
    return infer_parties(headline)


def parse_value(text: str):
    match = re.search(
        r"(?:\$|US\$)\s*([0-9]+(?:\.[0-9]+)?)\s*(trillion|tn|billion|bn|million|m)\b",
        text,
        re.I,
    )
    if not match:
        return None
    value = float(match.group(1))
    unit = match.group(2).lower()
    if unit in ("trillion", "tn"):
        return round(value * 1000, 3)
    if unit in ("billion", "bn"):
        return round(value, 3)
    return round(value / 1000, 3)


def main() -> None:
    request = urllib.request.Request(FEED, headers={"User-Agent": "DealScope/2.0 (+GitHub Actions)"})
    with urllib.request.urlopen(request, timeout=30) as response:
        xml = response.read()

    root = ET.fromstring(xml)
    items = []
    seen = set()
    rejected = 0

    for item in root.findall("./channel/item"):
        raw_title = clean(item.findtext("title", ""))
        description = clean(item.findtext("description", ""))
        headline, source_name = split_source(raw_title)

        parties = is_high_confidence_ma(headline, source_name)
        if not parties:
            rejected += 1
            continue
        acquirer, target = parties

        normalized = re.sub(r"[^a-z0-9]+", " ", headline.lower()).strip()
        if normalized in seen:
            continue
        seen.add(normalized)

        link = clean(item.findtext("link", ""))
        pub_raw = clean(item.findtext("pubDate", ""))
        try:
            pub = parsedate_to_datetime(pub_raw).astimezone(timezone.utc)
        except Exception:
            pub = datetime.now(timezone.utc)

        digest = hashlib.sha256((headline + link).encode()).hexdigest()[:12]
        summary = description or (
            f"High-confidence M&A headline detected from {source_name}. "
            "Open the original article to verify transaction terms."
        )
        items.append(
            {
                "id": f"news-{digest}",
                "date": pub.strftime("%B %-d, %Y"),
                "publishedISO": pub.isoformat(),
                "acquirer": acquirer,
                "target": target,
                "headline": headline,
                "valueBillions": parse_value(headline + " " + description),
                "sector": "M&A news",
                "countries": ["To be confirmed"],
                "status": "News detected",
                "crossBorder": False,
                "automated": True,
                "sourceName": source_name,
                "summary": summary[:360],
                "intent": "Automatically detected from a transaction-shaped headline. Verify the original reporting before relying on the terms or rationale.",
                "longTermGoals": [
                    "Confirm transaction terms",
                    "Review management rationale",
                    "Track approvals and closing conditions",
                ],
                "culture": "Not yet researched. Compare leadership, operating models, incentives, and employee practices.",
                "geography": "Not yet researched. Confirm headquarters, operating regions, and regulatory jurisdictions.",
                "valuation": "Deal value is shown only when a clear U.S.-dollar amount appears in the headline or feed summary.",
                "shareholderValue": "Review offer premium, financing, dilution, debt, and the market reaction in the original reporting.",
                "scores": {"strategic": 5, "cultural": 5, "geographic": 5, "valuation": 5},
                "source": link,
                "regulatoryTimeline": [
                    {"stage": "News detected", "status": "complete", "date": pub.strftime("%b %-d, %Y")},
                    {"stage": "Terms verified", "status": "current", "date": "Manual review needed"},
                    {"stage": "Regulatory review", "status": "upcoming", "date": "To be confirmed"},
                    {"stage": "Closing", "status": "upcoming", "date": "To be confirmed"},
                ],
                "integrationTimeline": [
                    {"stage": "Integration planning", "status": "upcoming"},
                    {"stage": "Leadership alignment", "status": "upcoming"},
                    {"stage": "Systems and operations", "status": "upcoming"},
                    {"stage": "Synergy tracking", "status": "upcoming"},
                ],
            }
        )
        if len(items) >= 30:
            break

    items.sort(key=lambda value: value["publishedISO"], reverse=True)
    payload = (
        "// Generated automatically. Do not edit by hand.\n"
        "window.generatedDeals = "
        + json.dumps(items, ensure_ascii=False, indent=2)
        + ";\n"
    )
    OUTPUT.write_text(payload.replace("</", "<\\/"), encoding="utf-8")
    print(f"Accepted {len(items)} high-confidence M&A records; rejected {rejected} feed items.")
    print(f"Wrote results to {OUTPUT}")


if __name__ == "__main__":
    main()
