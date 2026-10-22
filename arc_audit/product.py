"""Digital Arc Audit — the paid product behind Arc Singularity.

A deterministic "digital arc audit" engine that turns a digital footprint into a structured
trajectory report. This is the $9/mo paid deliverable behind the Arc Singularity promise page
(the free self-audit on the page is the free 60-second version of the same engine).

Shared vocabulary (maps 1:1 to the web tool's audit()):
- footprint: assets | identity | network | data          (what you own)
- cadence:   never | yearly | quarterly | monthly        (review frequency)
- interest:  legibility | risk | trajectory | network    (what matters most)
- legibility: clear | partial | fog                       (how legible your footprint is)
- focus:     list | defend | plan | publish               (the one thing to fix)
"""


# ---------------------------------------------------------------------------
# Lexicon: the vocabulary the audit speaks.
# ---------------------------------------------------------------------------
FRONTIER_VALUES = {
    "footprint": ("assets", "identity", "network", "data"),
    "cadence": ("never", "yearly", "quarterly", "monthly"),
    "interest": ("legibility", "risk", "trajectory", "network"),
    "legibility": ("clear", "partial", "fog"),
    "focus": ("list", "defend", "plan", "publish"),
}

FOCUS = {
    "list":   ("list",   "the missing piece is a single inventory", "list everything you own this week. inventory is the deliverable."),
    "defend": ("defend", "the risk is the slow bleed of subscriptions and forgotten data", "subscription + data sweep. kill what you forgot this week."),
    "plan":   ("plan",   "you already know the fix: a stated direction", "write the plan down. a stated direction is the whole job."),
    "publish":("publish","you want your reputation to live somewhere, on purpose", "name your own home first. the rest of the web is borrowed surface."),
}

CADENCE = {
    "never":     ("cadence", "no recent map of where your digital self sits", "run the audit now. the map is the deliverable, strategy is only the next step."),
    "yearly":    ("cadence", "your map is 12 months stale", "re-run this quarterly. drift compounds silently until it bites."),
    "quarterly": ("cadence", "your cadence is tight enough to course-correct", "keep going quarterly. you're already on the right track."),
    "monthly":   ("cadence", "you are already running the right cadence", "protect that discipline. cadence is your edge."),
}

INTEREST = {
    "legibility": ("legibility", "knowing exactly what I own & where it lives", "start with a single list. inventory is the deliverable."),
    "risk":       ("risk",       "the risk is the slow bleed of subscriptions and forgotten data", "subscription + data sweep. kill what you forgot this week."),
    "trajectory": ("trajectory", "you care about the 3-5 year direction", "write a plain-english 3-year plan. the arc is the point."),
    "network":    ("network",    "your reputation is carried by the people who cite or mirror you", "stop building on borrowed surface. name your own home first."),
}

LEGIBILITY = {
    "clear":  ("clear", "you have a baseline", "protect the baseline. drift will come, but you're ahead of it."),
    "partial":("legibility", "you have a partial map but no single source of truth", "consolidate into one list. clarity is the first deliverable, not the last."),
    "fog":    ("fog", "you don't even know what you own", "inventory first. a 60-second list beats a 60-hour strategy."),
}

FOOTPRINT = {
    "assets":     ("owned",     "your footprint is a stack of things that deserve a single ledger", "start by listing everything you own. inventory first, strategy second."),
    "identity":   ("identity",  "your name flows across the web without a single source of truth", "pick one home for your name and make it yours before you build on top of it."),
    "network":    ("network",   "your reputation is carried by the people who cite or mirror you", "stop building on borrowed surface. name your own home first."),
    "data":       ("data",      "the cost of your footprint hides in subscriptions you forgot", "run a subscription + data sweep this week. kill what you forgot."),
}


# ---------------------------------------------------------------------------
# Report model: the shape of a "digital arc audit" deliverable.
# ---------------------------------------------------------------------------
DEFAULT_REPORT = {
    "title": "Digital Arc Audit",
    "verdict": [],          # ordered list of theme slugs
    "recommendation": "",   # the single highest-priority first move
    "summary": "",          # one-line headline
    "sections": [],         # ordered list of {slug, heading, body, t, v, r}
    "meta": {"footprint": [], "cadence": [], "interest": [], "legibility": [], "focus": []},
    "share_url": "",
    "generator": "arc-audit.report",
}


def build_report(
    corpus: list[str] | None = None,
    inputs: dict | None = None,
    *,
    capacity: int | None = None,
) -> dict:
    """Deterministic. Same input -> byte-identical report."""
    corpus = corpus or []
    raw = dict(inputs or {})
    footprint = raw.get("footprint")
    fp = footprint if isinstance(footprint, list) else ([footprint] if footprint is not None else [])
    fp = list(dict.fromkeys(x for x in fp if x))

    cadence = raw.get("cadence")
    interest = raw.get("interest")
    legibility = raw.get("legibility")
    focus = raw.get("focus")

    sections: list[dict] = []
    verdict: list[str] = []

    ent = FOOTPRINT.get(footprint, FOOTPRINT["assets"]) if footprint else FOOTPRINT["assets"]
    if fp:
        verdict.append("footprint")
        sections.append(
            {
                "slug": "footprint",
                "heading": "Your footprint",
                "body": "You see this as: " + (", ".join(fp) if len(fp) <= 4 else fp[0] + " + " + str(len(fp) - 1) + " more"),
                "t": ent[0],
                "v": ent[1],
                "r": ent[2],
            }
        )

    if cadence:
        verdict.append("cadence")
        c = CADENCE.get(cadence, CADENCE["monthly"])
        sections.append({
            "slug": "cadence", "heading": "Review cadence", "body": "You ask me to check: " + cadence, "t": c[0], "v": c[1], "r": c[2],
        })
    if interest:
        verdict.append("interest")
        i = INTEREST.get(interest, INTEREST["trajectory"])
        sections.append({
            "slug": "interest", "heading": "What matters most", "body": "You're optimizing for: " + interest, "t": i[0], "v": i[1], "r": i[2],
        })
    if legibility:
        verdict.append("legibility")
        l = LEGIBILITY.get(legibility, LEGIBILITY["partial"])
        sections.append({
            "slug": "legibility", "heading": "How legible is your footprint", "body": "You characterize it as: " + legibility, "t": l[0], "v": l[1], "r": l[2],
        })
    if focus:
        verdict.append("focus")
        f = FOCUS.get(focus, FOCUS["list"])
        sections.append({
            "slug": "focus", "heading": "The one thing to fix", "body": "You've landed here to solve: " + focus, "t": f[0], "v": f[1], "r": f[2],
        })

    primary = sections[0] if sections else {}
    fp_str = ", ".join(fp) if fp else "none"
    recommendation = primary.get("r", "") if sections else "re-orient"
    summary = f"Digital arc audit: footprint={fp_str} | first move: {recommendation}"

    report = {
        "title": "Digital Arc Audit",
        "verdict": verdict,
        "recommendation": recommendation,
        "summary": summary,
        "sections": sections,
        "meta": {
            "footprint": fp,
            "cadence": [cadence] if cadence else [],
            "interest": [interest] if interest else [],
            "legibility": [legibility] if legibility else [],
            "focus": [focus] if focus else [],
        },
        "generator": "arc-audit.report",
    }
    return report


def build_share_url(report: dict, hostname: str = "arc-self-audit.pages.dev") -> str:
    import urllib.parse, json
    raw = {
        "footprint": report["meta"]["footprint"],
        "cadence": report["meta"]["cadence"],
        "interest": report["meta"]["interest"],
        "legibility": report["meta"]["legibility"],
        "focus": report["meta"]["focus"],
    }
    fragment = urllib.parse.quote(urllib.parse.quote(json.dumps(raw, sort_keys=True), safe="/~"), safe="/~")
    return f"https://{hostname}/?arc={fragment}#/audit"
