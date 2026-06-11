# AGENTS.md

## Project Layout

This repository now contains one desktop application:

```text
apps/
|-- electron/   # Electron main process and preload
|-- src/        # Vue renderer
|-- backend/    # Local Python HTTP backend and business logic
|-- scripts/    # Developer helper scripts
|-- dist/       # Vite build output
|-- package.json
|-- package-lock.json
`-- vite.config.js
```

The former `apps/pyside6` application line has been removed intentionally. Do not add new PySide6 application files unless the project is deliberately reintroducing that app.

The root directory is for repository-level files only. Keep application source, runtime files, and dependency files under `apps/`.

## Electron App

Location:

```text
apps
```

Important files:

- `package.json`, `package-lock.json`: Node dependency and script definitions.
- `node_modules/`: local installed Node dependencies. Keep this directory with the app when moving/copying it locally.
- `.npm-cache/`: local npm cache from this workspace.
- `electron/main.cjs`: Electron main process and Python backend launcher.
- `electron/preload.cjs`: renderer bridge.
- `src/`: Vue renderer.
- `backend/app/server.py`: local HTTP backend entry.
- `backend/app/bridge.py`: task bridge.
- `backend/classify_zipmod/`: Electron-owned Python business package.

Common commands:

```powershell
cd apps
npm run check:python
npm run dev
npm run build
npm run electron
```

Python backend development:

```powershell
cd apps
npm run python:dev
```

By default, the Electron main process starts the backend with `PYTHON_EXECUTABLE` if set. Otherwise it tries the local `mm_env` conda environment path first, then falls back to:

```powershell
conda run -n mm_env python backend/app/server.py
```

To force a specific Python interpreter:

```powershell
cd apps
$env:PYTHON_EXECUTABLE="D:\path\to\python.exe"
npm run dev
```

## Backend Boundary

Electron calls `backend/app/server.py`, which imports local modules from `backend/classify_zipmod/`.

Because `apps/pyside6` has been removed, the Electron app must not depend on any deleted PySide6 paths such as `apps/pyside6/script/app`. Shared or migrated behavior belongs inside `apps/backend/classify_zipmod/`.

## Maintenance Notes

- `Copy` is the safe default zipmod extraction mode.
- `Cut`/move modifies the game directory and should be treated as risky.
- Keep Electron, Vue, Python backend, dependency, and build files inside `apps/`.
- Do not add application source files directly to the repository root.
