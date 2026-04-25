#!/usr/bin/env python3
"""
Dedupe new feature recommendations against the history file.

Usage:
    python dedupe_features.py --new shortlist.json --history seen-features.jsonl

The script does conservative string-based matching to surface candidate matches.
The skill's caller (Claude) makes the final semantic call — "dark mode" and
"dark theme support" are the same idea even though only some words overlap.

Input formats:

shortlist.json (the new run's shortlisted features):
[
    {"name": "Bulk CSV import", "description": "..."},
    {"name": "Dark mode", "description": "..."},
    ...
]

seen-features.jsonl (one JSON object per line):
{"date": "2026-04-17", "name": "...", "description": "...", "scores": {...}}
{"date": "2026-04-17", "name": "...", "description": "...", "scores": {...}}
...

Output: prints to stdout a list of likely matches, one per line:

    [LIKELY MATCH]   new: "Dark mode"  ⟷  history: "Dark theme" (2026-04-10)
    [POSSIBLE MATCH] new: "CSV import" ⟷  history: "Bulk import" (2026-04-03)
    [NEW]            "Workflow automation"

Exit code is always 0. The skill caller is expected to read this output
and make a final semantic decision per match.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from difflib import SequenceMatcher

# Words that are too generic to count as evidence of a match
STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "in", "on", "for", "to", "with",
    "support", "feature", "ability", "functionality", "system", "tool",
    "based", "new", "advanced", "basic", "simple", "full", "custom",
}


def normalize(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def keywords(text: str) -> set:
    """Extract content words from a feature name/description."""
    return {w for w in normalize(text).split() if w not in STOPWORDS and len(w) > 2}


def similarity(a_name: str, a_desc: str, b_name: str, b_desc: str) -> float:
    """Combined similarity score for two (name, description) pairs.

    We weight name overlap more than description overlap, because product
    feature names tend to be more diagnostic of identity ("dark mode" is the
    feature, "toggle for dark UI theme" is just one way to describe it).
    """
    # Name similarity: blend of string and keyword overlap
    name_str_sim = SequenceMatcher(None, normalize(a_name), normalize(b_name)).ratio()
    name_kw_a, name_kw_b = keywords(a_name), keywords(b_name)
    if name_kw_a and name_kw_b:
        name_kw_sim = len(name_kw_a & name_kw_b) / len(name_kw_a | name_kw_b)
    else:
        name_kw_sim = 0.0
    name_sim = 0.5 * name_str_sim + 0.5 * name_kw_sim

    # Combined keyword overlap across name + description (catches paraphrases)
    full_kw_a = keywords(f"{a_name} {a_desc}")
    full_kw_b = keywords(f"{b_name} {b_desc}")
    if full_kw_a and full_kw_b:
        full_kw_sim = len(full_kw_a & full_kw_b) / len(full_kw_a | full_kw_b)
    else:
        full_kw_sim = 0.0

    # Weight name similarity higher because it's more diagnostic
    return 0.65 * name_sim + 0.35 * full_kw_sim


def load_jsonl(path: Path) -> list:
    """Load a JSONL file. Returns empty list if missing."""
    if not path.exists():
        return []
    entries = []
    for line_num, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"warning: skipping malformed JSONL on line {line_num}: {e}",
                  file=sys.stderr)
    return entries


def load_json(path: Path) -> list:
    """Load a JSON file. Errors loudly if missing."""
    if not path.exists():
        print(f"error: {path} not found", file=sys.stderr)
        sys.exit(1)
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--new", required=True,
                        help="JSON file with new shortlisted features")
    parser.add_argument("--history", required=True,
                        help="JSONL file with previously suggested features")
    parser.add_argument("--likely-threshold", type=float, default=0.55,
                        help="Similarity above this is flagged [LIKELY MATCH] (default: 0.55)")
    parser.add_argument("--possible-threshold", type=float, default=0.30,
                        help="Similarity above this is flagged [POSSIBLE MATCH] (default: 0.30)")
    args = parser.parse_args()

    new_features = load_json(Path(args.new))
    history = load_jsonl(Path(args.history))

    if not history:
        print(f"# History file is empty or missing — all {len(new_features)} features are NEW.\n")
        for feat in new_features:
            print(f'[NEW]            "{feat["name"]}"')
        return

    print(f"# Comparing {len(new_features)} new features against {len(history)} historical entries.\n")

    for new_feat in new_features:
        best_match = None
        best_score = 0.0
        for hist_feat in history:
            score = similarity(
                new_feat["name"], new_feat.get("description", ""),
                hist_feat["name"], hist_feat.get("description", ""),
            )
            if score > best_score:
                best_score = score
                best_match = hist_feat

        if best_score >= args.likely_threshold:
            print(f'[LIKELY MATCH]   new: "{new_feat["name"]}"  '
                  f'⟷  history: "{best_match["name"]}" '
                  f'({best_match.get("date", "unknown date")}) '
                  f'[score={best_score:.2f}]')
        elif best_score >= args.possible_threshold:
            print(f'[POSSIBLE MATCH] new: "{new_feat["name"]}"  '
                  f'⟷  history: "{best_match["name"]}" '
                  f'({best_match.get("date", "unknown date")}) '
                  f'[score={best_score:.2f}]')
        else:
            print(f'[NEW]            "{new_feat["name"]}"')

    print("\n# Notes:")
    print("# - LIKELY MATCH and POSSIBLE MATCH need a final semantic call from you.")
    print("# - 'Dark mode' vs 'Dark theme support' = same idea (tag as RECURRING).")
    print("# - 'Real-time sync' vs 'Real-time collaboration' = different ideas (keep as NEW).")


if __name__ == "__main__":
    main()
