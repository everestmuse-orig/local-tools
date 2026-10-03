#!/usr/bin/env python3
"""albumcount — how many studio albums does an artist have?

Uses Apple's iTunes Search API (no API key, no signup). Counts distinct
album titles credited to the artist, skipping singles/EPs best-effort.

Usage:
    python -m tools.albumcount "ABBA"
    python -m tools.albumcount "Taylor Swift" --json
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

API = "https://itunes.apple.com/search"


def fetch_albums(artist, limit=200):
    q = urllib.parse.urlencode({
        "term": artist,
        "entity": "album",
        "attribute": "artistTerm",
        "limit": str(limit),
    })
    req = urllib.request.Request(
        API + "?" + q,
        headers={"User-Agent": "local-tools/1.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8", "replace"))
    return data.get("results") or []


def _norm(s):
    return "".join(ch.lower() for ch in str(s or "") if ch.isalnum())


def studio_albums(artist):
    """Distinct studio-ish album titles for the artist.

    iTunes marks proper albums with collectionType == "Album". We dedupe
    on the normalized title and drop obvious non-studio editions
    (deluxe/remaster/live) best-effort — the count is approximate.
    """
    seen = {}
    want = _norm(artist)
    for r in fetch_albums(artist):
        if (r.get("collectionType") or "") != "Album":
            continue
        # the artistTerm search is loose (tributes, same-name artists) —
        # only count albums actually credited to the requested artist
        if _norm(r.get("artistName") or "") != want:
            continue
        # iTunes tags singles as collectionType "Album" — a real album
        # has a real tracklist
        try:
            if int(r.get("trackCount") or 0) < 7:
                continue
        except (TypeError, ValueError):
            continue
        title = (r.get("collectionName") or "").strip()
        if not title:
            continue
        # group editions under the base title ("1989 (Taylor's Version)"
        # -> "1989"); keep the shortest title per group
        base = title.lower().split(" (")[0].split(" - ")[0].strip()
        if base not in seen or len(title) < len(seen[base]):
            seen[base] = title
    titles = sorted(seen.values(), key=str.lower)
    # compilations are tagged collectionType "Album" by iTunes, so drop
    # them by title keywords best-effort
    titles = [t for t in titles
              if not any(w in t.lower() for w in (
                  "greatest hits", "best of", "the essential", "essential ",
                  "collection", "anthology", "the singles", "singles ",
                  "complete ", "ultimate ", "live at", "live in",
                  "gold", "exitos", "grandes exitos"))]
    return titles


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Count an artist's studio albums via the iTunes API.")
    ap.add_argument("artist", help="Artist name, e.g. \"ABBA\"")
    ap.add_argument("--json", action="store_true",
                    help="print machine-readable JSON")
    args = ap.parse_args(argv)

    try:
        albums = studio_albums(args.artist)
    except Exception as exc:  # noqa: BLE001 - friendly CLI error
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"artist": args.artist,
                          "studio_albums": len(albums),
                          "titles": albums}, indent=2))
    else:
        print(f"{args.artist}: {len(albums)} studio albums")
        for t in albums:
            print(f"  - {t}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
