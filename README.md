# local-tools

Small Python CLI tools built by Everest, made to run on your Mac in the
VS Code terminal. No servers, no accounts — just scripts.

## Setup (once)

Open a terminal in VS Code and run:

```bash
git clone https://github.com/everestmuse-orig/local-tools.git
cd local-tools
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

(Keep that terminal open, or re-run `source .venv/bin/activate` each
time you come back.)

## Tools

| Tool | What it does | Example |
|------|--------------|---------|
| `albumcount` | Count an artist's studio albums (iTunes API, no key needed) | `python -m tools.albumcount "ABBA"` |

Every tool supports `--help`, and most support `--json` for
machine-readable output:

```bash
python -m tools.albumcount "Taylor Swift" --json
```

## Adding a new tool

Copy the template and make it yours:

```bash
cp templates/new_tool.py tools/mytool.py
# edit tools/mytool.py, then:
python -m tools.mytool --help
```

Conventions are in the template header (argparse, friendly errors,
`--json`, no hardcoded secrets). If a tool needs a third-party
package, add it to `requirements.txt`.

## Updating

```bash
git pull
```
