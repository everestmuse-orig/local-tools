# local-tools

Small Python CLI tools built by Everest, made to run on your PC in the
VS Code terminal. No servers, no accounts — just scripts. Everything
here is plain Python, so it runs the same on Windows, Mac, and Linux.

## Setup (once)

Open a terminal in VS Code and run:

```bash
git clone https://github.com/everestmuse-orig/local-tools.git
cd local-tools
```

Then create the virtual environment and install dependencies.

**Windows (PowerShell — the VS Code default on PC):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Windows (Command Prompt):**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

**Mac / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

(Keep that terminal open, or re-run the activate line each time you
come back. On Windows, if PowerShell blocks the activate script, run
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try
again.)

You need Python 3.10+ installed — grab it from
[python.org](https://www.python.org/downloads/) (on Windows, tick
"Add python.exe to PATH" during install).

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
