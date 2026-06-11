# Electron + Vue + Python

This directory contains the maintained `classify_zipmod_tools` desktop app.

## Structure

```text
apps/
|-- electron/                 # Electron main process and preload
|-- src/                      # Vue renderer UI
|-- backend/app/              # Local Python HTTP bridge service
|-- backend/classify_zipmod/  # Python business logic
|-- scripts/                  # Developer helper scripts
|-- dist/                     # Current Vite build output
|-- node_modules/             # Installed Node dependencies
|-- .npm-cache/               # Local npm cache from this workspace
|-- package.json
|-- package-lock.json
`-- vite.config.js
```

The former `apps/pyside6` app has been removed. This app should remain self-contained in `apps/`.

## Commands

```powershell
npm run dev
npm run build
npm run electron
```

Python backend checks:

```powershell
npm run check:python
npm run python:dev
```

By default the Electron main process starts the backend with `PYTHON_EXECUTABLE` if set, then falls back to the configured local `mm_env` conda environment.

```powershell
$env:PYTHON_EXECUTABLE="D:\path\to\python.exe"
npm run dev
```

## Backend Boundary

Electron calls `backend/app/server.py`, which imports local modules from `backend/classify_zipmod/`. It should not import from removed PySide6 paths. Shared behavior should be migrated deliberately into this backend package rather than reached through relative paths.

Important backend files:

- `backend/app/server.py`
- `backend/app/bridge.py`
- `backend/classify_zipmod/services/mod_workflow.py`
- `backend/classify_zipmod/core/card_parser.py`
- `backend/classify_zipmod/core/zipmod_utils.py`
- `backend/classify_zipmod/tools/mod_sorter.py`
