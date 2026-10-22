#!/usr/bin/env python3
"""
arc_audit.py — Digital Arc Self-Audit. Zero-dependency CLI.

A 60-second self-audit of your digital footprint: what it's made of, how often
you review it, what matters most, and how legible it is right now. Prints the
verdict and your first move.

Usage:
    python arc_audit.py --footprint assets --cadence quarterly --interest trajectory --legibility partial --focus plan
    echo '{"footprint":"data"}' | python arc_audit.py            # JSON on stdin
    python arc_audit.py --selftest                              # run the built-in self-test

No third-party modules. Stdlib only (argparse, json, sys).
"""
import argparse
import json
import sys

__version__ = "1.0.0"

# Each input slug -> {t, v, r}. t = theme label, v = verdict sentence, r = first move.
VERDICT = {
    "assets":      {"t": "owned",     "v": "your footprint is a stack of things that deserve a single ledger", "r": "start by listing everything you own. inventory first, strategy second."},
    "identity":    {"t": "identity",  "v": "your name flows across the web without a single source of truth", "r": "pick one home for your name and make it yours before you build on top of it."},
    "network":     {"t": "network",   "v": "your reputation is carried by the people who cite or mirror you", "r": "stop building on borrowed surface. name your own home first."},
    "data":        {"t": "data",      "v": "the cost of your footprint hides in subscriptions you forgot", "r": "run a subscription + data sweep this week. kill what you forgot."},
    "clear":       {"t": "clear",     "v": "you already have a baseline", "r": "protect the baseline. drift will come, but you're ahead of it."},
    "partial":     {"t": "legibility","v": "you have a partial map but no single source of truth", "r": "consolidate into one list. clarity is the first deliverable, not the last."},
    "fog":         {"t": "fog",       "v": "you don't even know what you own", "r": "inventory first. a 60-second list beats a 60-hour strategy."},
    "never":       {"t": "cadence",   "v": "no recent map of where your digital self sits", "r": "run the audit now. the map is the deliverable, strategy is only the next step."},
    "yearly":      {"t": "cadence",   "v": "your map is 12 months stale", "r": "re-run this quarterly. drift compounds silently until it bites."},
    "quarterly":   {"t": "cadence",   "v": "your cadence is tight enough to course-correct", "r": "keep going quarterly. you're already on the right track."},
    "monthly":     {"t": "cadence",   "v": "you are already running the right cadence", "r": "protect that discipline. cadence is your edge."},
    "legibility":  {"t": "legibility","v": "knowing exactly what I own & where it lives", "r": "start with a single list. inventory is the deliverable."},
    "risk":        {"t": "risk",      "v": "the risk is the slow bleed of subscriptions and forgotten data", "r": "subscription + data sweep. kill what you forgot this week."},
    "trajectory":  {"t": "trajectory","v": "you care about the 3-5 year direction", "r": "write a plain-english 3-year plan. the arc is the point."},
    "plan":        {"t": "plan",      "v": "you already know the fix: a stated direction", "r": "write the plan down. a stated direction is the whole job."},
    "publish":     {"t": "publish",   "v": "you want your reputation to live somewhere, on purpose", "r": "name your own home first. the rest of the web is borrowed surface."},
    "list":  {"t": "list",   "v": "the missing piece is a single inventory", "r": "list everything you own this week. inventory is the deliverable."},
    "defend": {"t": "defend", "v": "the risk is the slow bleed of subscriptions and forgotten data", "r": "subscription + data sweep. kill what you forgot this week."},
}

# Cadence (frequency of review) -> (v, r)
CADENCE = {
    "never":     ("no recent map of where your digital self sits", "run the audit now. the map is the deliverable, strategy is only the next step."),
    "yearly":    ("your map is 12 months stale", "re-run this quarterly. drift compounds silently until it bites."),
    "quarterly": ("your cadence is tight enough to course-correct", "keep going quarterly. you're already on the right track."),
    "monthly":   ("you are already running the right cadence", "protect that discipline. cadence is your edge."),
}

# Interest -> (t, v, r)
INTEREST = {
    "legibility": ("legibility", "knowing exactly what I own & where it lives", "start with a single list. inventory is the deliverable."),
    "risk":       ("risk",       "the risk is the slow bleed of subscriptions and forgotten data", "subscription + data sweep. kill what you forgot this week."),
    "trajectory": ("trajectory", "you care about the 3-5 year direction", "write a plain-english 3-year plan. the arc is the point."),
    "network":    ("network",    "your reputation is carried by the people who cite or mirror you", "stop building on borrowed surface. name your own home first."),
}

# Legibility (how clear your footprint is) -> (v, r)
LEGIBILITY = {
    "clear":  ("you have a baseline", "protect the baseline. drift will come, but you're ahead of it."),
    "partial": ("you have a partial map but no single source of truth", "consolidate into one list. clarity is the first deliverable, not the last."),
    "fog":    ("you don't even know what you own", "inventory first. a 60-second list beats a 60-hour strategy."),
}

# Focus (the one thing to fix) -> (t, v, r)
FOCUS = {
    "list":   ("list",   "the missing piece is a single inventory", "list everything you own this week. inventory is the deliverable."),
    "defend": ("defend", "the risk is the slow bleed of subscriptions and forgotten data", "subscription + data sweep. kill what you forgot this week."),
    "plan":   ("plan",   "you already know the fix: a stated direction", "write the plan down. a stated direction is the whole job."),
    "publish":("publish","you want your reputation to live somewhere, on purpose", "name your own home first. the rest of the web is borrowed surface."),
}


def audit(inputs):
    """Pure verdict. `inputs` is a dict with any of footprint/cadence/interest/
    legibility/focus (all optional). Returns dict with verdict (the ; -separated
    theme list), recommend (bits[0].r), bits (raw rows), themes."""
    footprint = inputs.get("footprint")
    cadence = inputs.get("cadence")
    interest = inputs.get("interest")
    legibility = inputs.get("legibility")
    focus = inputs.get("focus")
    bits = []
    if footprint:
        v = VERDICT.get(footprint)
        bits.append({"t": v["t"] if v else "owned",
                     "v": v["v"] if v else "your footprint needs inventory",
                     "r": v["r"] if v else "start by inventorying what you own."})
    if cadence:
        v, r = CADENCE.get(cadence, ("unknown cadence", "pick a review cadence and run the audit."))
        bits.append({"t": "cadence", "v": v, "r": r})
    if interest:
        t, v, r = INTEREST.get(interest, (interest, interest, "state what actually matters and the audit will adapt."))
        bits.append({"t": t, "v": v, "r": r})
    if legibility:
        if legibility == "clear":
            t, v, r = "clear", LEGIBILITY["clear"][0], LEGIBILITY["clear"][1]
        elif legibility == "fog":
            t, v, r = "fog", LEGIBILITY["fog"][0], LEGIBILITY["fog"][1]
        else:
            t, v, r = "legibility", LEGIBILITY["partial"][0], LEGIBILITY["partial"][1]
        bits.append({"t": t, "v": v, "r": r})
    if focus:
        t, v, r = FOCUS.get(focus, (focus, focus, "keep this as your north star."))
        bits.append({"t": t, "v": v, "r": r})
    themes = [b["t"] for b in bits]
    return {
        "verdict": " · ".join(themes),
        "recommend": bits[0]["r"] if bits else "start by inventorying what you own.",
        "bits": bits,
        "themes": themes,
    }


def _build_parser():
    p = argparse.ArgumentParser(
        prog="arc_audit",
        description="Digital Arc Self-Audit: where your digital footprint is heading.",
    )
    p.add_argument("--footprint", choices=list(VERDICT),
                   help="what your footprint is mostly made of (assets/identity/network/data)")
    p.add_argument("--cadence", choices=list(CADENCE),
                   help="how often you review it (never/yearly/quarterly/monthly)")
    p.add_argument("--interest", choices=list(INTEREST),
                   help="what matters most (legibility/risk/trajectory/network)")
    p.add_argument("--legibility", choices=list(LEGIBILITY),
                   help="how legible your footprint is right now (clear/partial/fog)")
    p.add_argument("--focus", choices=list(FOCUS),
                   help="the one thing to fix (list/defend/plan/publish)")
    p.add_argument("--selftest", action="store_true",
                   help="run the built-in self-test and exit")
    p.add_argument("--json", help="single JSON object on the command line")
    return p


def _stdin_json():
    return json.load(sys.stdin)


def _run(inputs):
    out = audit(inputs)
    print("verdict:", out["verdict"])
    print("recommend:", out["recommend"])
    if "--verbose" in sys.argv:
        print("themes:", ", ".join(out["themes"]))
    return 0


def _selftest():
    failures = 0
    # (inputs, expected THEME list). Each entry is the exact list of bit "t"
    # values the audit() must produce -- the verdict string is the join of these.
    cases = [
        ({"footprint": "data", "cadence": "never", "interest": "risk", "legibility": "fog", "focus": "defend"},
         ["data", "cadence", "risk", "fog", "defend"]),
        ({"footprint": "identity", "cadence": "monthly", "legibility": "clear", "focus": "plan"},
         ["identity", "cadence", "clear", "plan"]),
        ({"footprint": "network", "cadence": "never"},
         ["network", "cadence"]),
        ({"footprint": "assets", "cadence": "quarterly", "focus": "list"},
         ["owned", "cadence", "list"]),
        ({"footprint": "unknown", "cadence": "yearly", "legibility": "fog"},
         ["owned", "cadence", "fog"]),
        ({"interest": "trajectory", "focus": "publish", "legibility": "partial"},
         ["trajectory", "legibility", "publish"]),
    ]
    for i, (inp, expected_themes) in enumerate(cases):
        out = audit(inp)
        if out["themes"] != expected_themes:
            failures += 1
            print("FAIL case %d: expected themes %r, got %r" % (i, expected_themes, out["themes"]))
        if out["verdict"] != " \u00b7 ".join(expected_themes):
            failures += 1
            print("FAIL case %d: verdict %r != %r" % (i, out["verdict"], " \u00b7 ".join(expected_themes)))
        for b in out["bits"]:
            if not all(k in b for k in ("t", "v", "r")):
                failures += 1
                print("FAIL case %d: bit missing field" % i)
    if failures:
        print("selftest FAILED: %d case(s)" % failures)
        return 1
    print("selftest OK: %d combinations verified" % len(cases))
    return 0


def main(argv=None):
    p = _build_parser()
    args = p.parse_args(argv)
    if args.selftest:
        return _selftest()
    inputs = {}
    if args.json:
        inputs = json.loads(args.json)
    if args.footprint:
        inputs["footprint"] = args.footprint
    if args.cadence:
        inputs["cadence"] = args.cadence
    if args.interest:
        inputs["interest"] = args.interest
    if args.legibility:
        inputs["legibility"] = args.legibility
    if args.focus:
        inputs["focus"] = args.focus
    if not inputs:
        try:
            inputs = _stdin_json()
        except Exception:
            sys.stderr.write("no inputs given (flags, --json, or stdin)\n")
            return 1
    if not inputs:
        p.print_help()
        return 0
    return _run(inputs)


if __name__ == "__main__":
    sys.exit(main())
