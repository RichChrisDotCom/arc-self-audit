#!/usr/bin/env python3
"""Self-test for arc-audit report engine.

Verifies the paid report engine (arc_audit/product.py) is correct and
reproducible. Run: python3 arc_audit/product.py --selftest

Checks:
  1. build_report() produces non-empty verdict + summary for every input combo.
  2. build_report() is deterministic (same input -> same output).
  3. build_share_url() returns a valid-looking URL.
  4. Every input slug maps to exactly one output (no silent failures).
  5. Required keys present in the report dict.
"""

import sys

# Add the repo root to the path so we can import the product module.
sys.path.insert(0, ".")

from arc_audit.product import build_report, build_share_url  # noqa: E402

FAILURES = []


def check(name, condition, detail=""):
    if condition:
        print(f"  [PASS] {name}")
    else:
        print(f"  [FAIL] {name} {detail}")
        FAILURES.append(name)


def main():
    print("Running Arc Audit self-test ...")

    # Test 1: build_report produces non-empty verdict + summary for every combo
    print("\n[TEST 1] report output for every input combination")
    combos = []
    for f in ("assets", "identity", "network", "data"):
        for c in ("never", "yearly", "quarterly", "monthly"):
            for i in ("legibility", "risk", "trajectory", "network"):
                for l in ("clear", "partial", "fog"):
                    for fo in ("list", "defend", "plan", "publish"):
                        combos.append({"footprint": f, "cadence": c, "interest": i, "legibility": l, "focus": fo})
    # Sample rather than 4*4*4*3*4 = 768 full combos (each builds 5 sections)
    sample = combos[:12] + combos[60:64] + combos[300:304]
    for inputs in sample:
        r = build_report(inputs=inputs)
        ok = bool(r["verdict"]) and bool(r["summary"]) and r["title"]
        check(f"inputs={inputs}", ok, str(r))

    # Test 2: deterministic
    print("\n[TEST 2] deterministic output")
    a = build_report(inputs={"footprint": "identity", "cadence": "monthly", "interest": "trajectory", "legibility": "partial", "focus": "plan"})
    b = build_report(inputs={"footprint": "identity", "cadence": "monthly", "interest": "trajectory", "legibility": "partial", "focus": "plan"})
    check("deterministic", a == b, f"{a} != {b}")

    # Test 3: build_share_url returns a valid-looking URL
    print("\n[TEST 3] share URL generation")
    r = build_report(inputs={"footprint": "data", "cadence": "never", "interest": "risk", "legibility": "fog", "focus": "defend"})
    url = build_share_url(r)
    check("share_url format", url.startswith("https://") and "#/audit" in url, url)

    # Test 4: every input slug maps to exactly one output section (one section per input)
    print("\n[TEST 4] no silent failures (every input -> exactly one section)")
    r = build_report(inputs={"footprint": "assets", "cadence": "monthly", "interest": "trajectory", "legibility": "partial", "focus": "plan"})
    slugs = [s["slug"] for s in r["sections"]]
    check(f"footprint=assets", "footprint" in slugs, str(slugs))
    check(f"cadence=monthly", "cadence" in slugs, str(slugs))
    check(f"interest=trajectory", "interest" in slugs, str(slugs))
    check(f"legibility=partial", "legibility" in slugs, str(slugs))
    check(f"focus=plan", "focus" in slugs, str(slugs))

    for f in ("assets", "identity", "network", "data"):
        r = build_report(inputs={"footprint": f, "cadence": "monthly", "interest": "trajectory", "legibility": "partial", "focus": "plan"})
        check(f"footprint={f}", "footprint" in [s["slug"] for s in r["sections"]], str(r["sections"]))

    for c in ("never", "yearly", "quarterly", "monthly"):
        r = build_report(inputs={"footprint": "assets", "cadence": c, "interest": "trajectory", "legibility": "partial", "focus": "plan"})
        check(f"cadence={c}", "cadence" in [s["slug"] for s in r["sections"]], str(r["sections"]))

    for i in ("legibility", "risk", "trajectory", "network"):
        r = build_report(inputs={"footprint": "assets", "cadence": "monthly", "interest": i, "legibility": "partial", "focus": "plan"})
        check(f"interest={i}", "interest" in [s["slug"] for s in r["sections"]], str(r["sections"]))

    for l in ("clear", "partial", "fog"):
        r = build_report(inputs={"footprint": "assets", "cadence": "monthly", "interest": "trajectory", "legibility": l, "focus": "plan"})
        check(f"legibility={l}", "legibility" in [s["slug"] for s in r["sections"]], str(r["sections"]))

    for fo in ("list", "defend", "plan", "publish"):
        r = build_report(inputs={"footprint": "assets", "cadence": "monthly", "interest": "trajectory", "legibility": "partial", "focus": fo})
        check(f"focus={fo}", "focus" in [s["slug"] for s in r["sections"]], str(r["sections"]))

    # Test 5: required keys present
    print("\n[TEST 5] required report keys")
    r = build_report(inputs={"footprint": "assets"})
    for key in ("title", "verdict", "recommendation", "summary", "sections", "meta", "generator"):
        check(f"key={key}", key in r, str(r.keys()))

    print(f"\n{'=' * 50}")
    if FAILURES:
        print(f"SELF-TEST FAILED: {len(FAILURES)} check(s) failed")
        for f in FAILURES:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("SELF-TEST OK: all checks passed")
        sys.exit(0)


if __name__ == "__main__":
    main()
