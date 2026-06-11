const { spawn } = require("node:child_process");
const path = require("node:path");

const mode = process.argv[2] || "check";
const root = path.join(__dirname, "..");
const pythonExecutable = process.env.PYTHON_EXECUTABLE;
const condaEnv = process.env.STAR_MANAGER_CONDA_ENV || "mm_env";

const pythonArgsByMode = {
  check: ["-m", "py_compile", "backend/app/server.py", "backend/app/bridge.py"],
  dev: ["backend/app/server.py"]
};

if (!pythonArgsByMode[mode]) {
  console.error(`Unknown python script mode: ${mode}`);
  process.exit(1);
}

const command = pythonExecutable || "conda";
const args = pythonExecutable
  ? pythonArgsByMode[mode]
  : ["run", "-n", condaEnv, "python", ...pythonArgsByMode[mode]];

const child = spawn(command, args, {
  cwd: root,
  stdio: "inherit",
  shell: false,
  windowsHide: true
});

child.on("exit", (code, signal) => {
  if (signal) {
    console.error(`Python process exited by signal ${signal}`);
    process.exit(1);
  }
  process.exit(code ?? 0);
});
