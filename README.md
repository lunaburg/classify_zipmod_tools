# Star_Manager

Electron + Vue desktop app with a local Python HTTP backend for managing HS2 / AIS card dependencies and related zipmod resources.

## Project Context

Star_Manager is a mod manager designed for the HS2 game. Its main managed targets are `zipmod` and `png` files, and future versions may also handle `unity3d` files.

- `zipmod` files are compressed archives.
- A typical `zipmod` contains `unity3d` model files, CSV files that record model metadata such as model name and body part, and an XML file that records mod author information.
- `png` files are commonly used as character cards under the HS2 user data structure.

## Current Structure

The project currently has one maintained application under `apps/`.

```text
apps/
|-- electron/                 # Electron main process and preload
|-- src/                      # Vue renderer UI
|-- backend/app/              # Local Python HTTP service
|-- backend/star_manager/     # Python business logic
|-- scripts/                  # Developer helper scripts
|-- dist/                     # Vite build output
|-- node_modules/             # Installed Node dependencies
|-- .npm-cache/               # Local npm cache from this workspace
|-- package.json
|-- package-lock.json
`-- vite.config.js
```

Repository-level files such as this README and `AGENTS.md` stay at the root. Application files should stay inside `apps/`.

## Test Environment

The repository includes an HS2 test game environment under `test/hs2`. Future development and verification can use this test folder directly.

Important HS2 test directories and expected roles:

- `test/hs2/mods`: stores `zipmod` files.
- `test/hs2/abdata`: usually stores `unity3d` files.
- `test/hs2/UserData/char`: stores character cards, usually `png` files.

## Commands

Run all commands from `apps`:

```powershell
cd apps
```

Check the Python backend entry points:

```powershell
npm run check:python
```

Start the development app:

```powershell
npm run dev
```

Build the renderer:

```powershell
npm run build
```

Build and start Electron against the production renderer:

```powershell
npm run electron
```

Start only the Python backend:

```powershell
npm run python:dev
```

## Python Backend

The Electron main process starts `backend/app/server.py`. It uses `PYTHON_EXECUTABLE` when set; otherwise it tries the local `mm_env` conda environment path and then falls back to `conda run -n mm_env python`.

Example with an explicit interpreter:

```powershell
cd apps
$env:PYTHON_EXECUTABLE="D:\path\to\python.exe"
npm run dev
```

Important backend files:

- `backend/app/server.py`
- `backend/app/bridge.py`
- `backend/star_manager/services/mod_workflow.py`
- `backend/star_manager/core/card_parser.py`
- `backend/star_manager/core/zipmod_utils.py`
- `backend/star_manager/tools/mod_sorter.py`

## Notes

- The Electron app is self-contained under `apps/`.
- The removed PySide6 app should not be imported or referenced by new code.
- `Copy` is the safer zipmod extraction mode. `Cut`/move modifies the game directory and should be treated carefully.
