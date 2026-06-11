# Electron + Vue + Python

This directory contains the maintained `Star_Manager` desktop app.

## Domain Notes

Star_Manager is an HS2 mod manager. The main managed file types are `zipmod` archives and `png` character cards, with possible future support for `unity3d` files. A typical `zipmod` archive may contain `unity3d` model files, CSV metadata files for model names and parts, and XML author metadata.

## Structure

```text
apps/
|-- electron/                 # Electron main process and preload
|-- src/                      # Vue renderer UI
|-- backend/app/              # Local Python HTTP bridge service
|-- backend/star_manager/     # Python business logic
|-- scripts/                  # Developer helper scripts
|-- dist/                     # Current Vite build output
|-- node_modules/             # Installed Node dependencies
|-- .npm-cache/               # Local npm cache from this workspace
|-- package.json
|-- package-lock.json
`-- vite.config.js
```

The former `apps/pyside6` app has been removed. This app should remain self-contained in `apps/`.

The repository-level `test/hs2` directory is the local HS2 test environment. In the expected HS2 layout, `mods` stores `zipmod` files, `abdata` stores `unity3d` files, and `UserData/char` stores character-card `png` files.

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

Electron calls `backend/app/server.py`, which imports local modules from `backend/star_manager/`. It should not import from removed PySide6 paths. Shared behavior should be migrated deliberately into this backend package rather than reached through relative paths.

Important backend files:

- `backend/app/server.py`
- `backend/app/bridge.py`
- `backend/star_manager/services/mod_workflow.py`
- `backend/star_manager/core/card_parser.py`
- `backend/star_manager/core/zipmod_utils.py`
- `backend/star_manager/tools/mod_sorter.py`
