# Arc Audit

**Digital Arc Audit** — a deterministic report engine that turns a digital footprint
into a structured trajectory report, with a matching free 60-second web self-audit.

The **Arc Singularity** digital arc concept is distributed through the GitHub repo
`arc-self-audit`. This is the paid report engine: you feed it a digital footprint and it
emits a structured verdict, a per-category `{t, v, r}` section set, and a headline summary.

## What's in the repo

| Artifact | What it is |
|---|---|
| `arc_audit/product.py` | Paid $9/mo report engine. Deterministic, stdlib-only, shareable by URL fragment. |
| `digital-arc-self-audit.html` | Free 60-second web self-audit tool (no backend, shareable by URL fragment). |
| `index.html` | The public promise page for the Arc Singularity concept. |
| `brand.md` | The brand concept doc. |
| `.github/workflows/self-test.yml` | CI workflow. |
| `.gitignore` | Dotfile ignores. |
| `README.md` | This doc. |

## Free web self-audit

```sh
# Open in a browser
https://arc-self-audit.pages.dev/digital-arc-self-audit
```

No backend, no signup. Six questions, one verdict, one shareable URL fragment.
Runs entirely in your browser — nothing leaves your machine.

## Paid Arc Audit report

`arc_audit/product.py` is the deterministic report engine. It turns a digital footprint
into a structured trajectory report. Run from the command line:

```sh
python3 arc_audit/product.py \
  --footprint assets --cadence quarterly --interest trajectory \
  --legibility clear --focus plan
```

Or feed JSON / flags / stdin. Use the report builder directly:

```python
from arc_audit.product import build_report

report = build_report(
    inputs={
        "footprint": ["data"],
        "cadence": "quarterly",
        "interest": "trajectory",
        "legibility": "clear",
        "focus": "plan",
    }
)
print(report["verdict"])
print(report["summary"])
```

## How it maps to the promise page

| Product surface | Role |
|---|---|
| `digital-arc-self-audit.html` | Free 60-second web self-audit (the top-of-funnel capture) |
| `arc_audit/product.py` | Paid $9/mo report engine (the paid deliverable) |
| `index.html` | Public promise page on the Arc Singularity concept |
| `brand.md` | Brand concept and positioning |
| `.github/workflows/self-test.yml` | CI workflow |
| `.gitignore` | Dotfile ignores |

## Method (transparent)

Every Arc Audit report is deterministic and reproducible. The report is a `{t, v, r}` section
set over five inputs: footprint, cadence, interest, legibility, focus. The verdict is the
`·`-joined list of themes, plus a single highest-priority first move. All output is deterministic
and reproducible — same input, same report, every time.

## License

MIT — see `LICENSE`.
