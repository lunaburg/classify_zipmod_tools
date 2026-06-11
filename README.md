# classify_zipmod_tools

Electron + Vue desktop app with a local Python HTTP backend for classifying HS2 / AIS card dependencies and related zipmod resources.

## Current Structure

The project currently has one maintained application under `apps/`. The former `apps/pyside6` app has been removed intentionally.

```text
apps/
|-- electron/                 # Electron main process and preload
|-- src/                      # Vue renderer UI
|-- backend/app/              # Local Python HTTP service
|-- backend/classify_zipmod/  # Python business logic
|-- scripts/                  # Developer helper scripts
|-- dist/                     # Vite build output
|-- node_modules/             # Installed Node dependencies
|-- .npm-cache/               # Local npm cache from this workspace
|-- package.json
|-- package-lock.json
`-- vite.config.js
```

Repository-level files such as this README and `AGENTS.md` stay at the root. Application files should stay inside `apps/`.

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
- `backend/classify_zipmod/services/mod_workflow.py`
- `backend/classify_zipmod/core/card_parser.py`
- `backend/classify_zipmod/core/zipmod_utils.py`
- `backend/classify_zipmod/tools/mod_sorter.py`

## Notes

- The Electron app is self-contained under `apps/`.
- The removed PySide6 app should not be imported or referenced by new code.
- `Copy` is the safer zipmod extraction mode. `Cut`/move modifies the game directory and should be treated carefully.
