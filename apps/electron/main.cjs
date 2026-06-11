const { app, BrowserWindow, Menu, dialog, ipcMain } = require("electron");
const { spawn } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const rendererUrl = process.env.ELECTRON_RENDERER_URL || "";
const isDev = Boolean(rendererUrl);
const backendPort = process.env.CLASSIFY_ZIPMOD_BACKEND_PORT || "8765";
let backendProcess = null;

function createWindow() {
  const window = new BrowserWindow({
    width: 980,
    height: 720,
    minWidth: 900,
    minHeight: 640,
    title: "classify_zipmod_tools",
    backgroundColor: "#f3efe4",
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  if (rendererUrl) {
    window.loadURL(rendererUrl);
  } else {
    window.loadFile(path.join(__dirname, "../dist/index.html"));
  }
}

function startPythonBackend() {
  const backendEntry = path.join(__dirname, "../backend/app/server.py");
  const backendRoot = path.join(__dirname, "../backend");
  const pythonExecutable = resolvePythonExecutable();
  const command = pythonExecutable || "conda";
  const args = pythonExecutable
    ? [backendEntry]
    : ["run", "-n", process.env.CLASSIFY_ZIPMOD_CONDA_ENV || "mm_env", "python", backendEntry];

  console.log(`[backend] starting: ${command} ${args.join(" ")}`);
  backendProcess = spawn(command, args, {
    cwd: backendRoot,
    env: {
      ...process.env,
      CLASSIFY_ZIPMOD_BACKEND_PORT: backendPort
    },
    stdio: "inherit",
    windowsHide: true
  });

  backendProcess.on("error", (error) => {
    console.error("[backend] failed to start:", error);
  });

  backendProcess.on("exit", (code, signal) => {
    console.error(`[backend] exited code=${code} signal=${signal}`);
  });
}

function resolvePythonExecutable() {
  const candidates = [
    process.env.PYTHON_EXECUTABLE,
    "D:\\desktop_app\\anaconda\\envs\\mm_env\\python.exe"
  ].filter(Boolean);

  return candidates.find((candidate) => fs.existsSync(candidate)) || "";
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function fetchBackend(route, options = {}) {
  const url = `http://127.0.0.1:${backendPort}${route}`;
  const fetchOptions = {
    method: options.method || "GET",
    headers: {
      "content-type": "application/json",
      ...(options.headers || {})
    },
    body: options.body ? JSON.stringify(options.body) : undefined
  };

  let lastError;
  for (let attempt = 0; attempt < 20; attempt += 1) {
    try {
      const response = await fetch(url, fetchOptions);
      return response.json();
    } catch (error) {
      lastError = error;
      await sleep(250);
    }
  }

  return {
    ok: false,
    error: `Python backend unavailable: ${lastError ? lastError.message : "unknown error"}`
  };
}

ipcMain.handle("dialog:selectDirectory", async (_event, title) => {
  const result = await dialog.showOpenDialog({
    title,
    properties: ["openDirectory"]
  });
  return result.canceled ? "" : result.filePaths[0];
});

ipcMain.handle("backend:request", async (_event, route, options = {}) => {
  return fetchBackend(route, options);
});

app.whenReady().then(() => {
  Menu.setApplicationMenu(null);
  startPythonBackend();
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("before-quit", () => {
  if (backendProcess && !backendProcess.killed) {
    backendProcess.kill();
  }
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
