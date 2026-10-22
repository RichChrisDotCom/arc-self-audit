# Arc Audit

Zero-dependency CLI + self-audit of the **Arc Singularity** digital arc concept.

Run a 60-second self-audit: what your footprint is made of, how often you review it,
what matters most, and how legible it is right now.

## Install

No third-party packages required. The script is executable on its own:

```sh
chmod +x arc_audit.py
./arc_audit.py --footprint assets --cadence quarterly --interest trajectory --legibility partial --focus plan
```

Or install the console entry point (`arc-audit`) for editable use:

```sh
pip install -e .
arc-audit --footprint assets --cadence quarterly --interest trajectory --legibility partial --focus plan
```

## Usage

```
--footprint    assets|identity|network|data        (what your footprint is made of)
--cadence      never|yearly|quarterly|monthly       (how often you review it)
--interest     legibility|risk|trajectory|network   (what matters most)
--legibility   clear|partial|fog                    (how legible your footprint is)
--focus        list|defend|plan|publish             (the one thing to fix)
```

Each flag is optional. Feed inputs as flags, `--json`, or on stdin.

```sh
echo '{"footprint":"network","cadence":"never"}' | arc-audit
```

## Output

The verdict is the ` · `-joined list of themes (e.g. `data · cadence · risk · fog · defend`),
plus the single highest-priority "first move".

## Self-test

```sh
python3 arc_audit.py --selftest
```

## As a GitHub distribution asset

- `arc-self-audit.pages.dev/digital-arc-self-audit` — the static web tool (no backend, shareable by URL fragment).
- This CLI — a zero-dependency companion for scripting and embedding.
