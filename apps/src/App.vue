<script setup>
import { onMounted, reactive, ref } from "vue";

const t = {
  noTask: "\u65e0\u4efb\u52a1",
  pauseNotReady: "\u6682\u505c\u672a\u63a5\u5165",
  pauseMessage: "\u6682\u505c\u529f\u80fd\u5c1a\u672a\u63a5\u5165\u3002",
  brandSubtitle: "HS2 \u4eba\u7269\u5361\u4f9d\u8d56\u63d0\u53d6\u4e0e\u8d44\u6e90\u8865\u9f50",
  logTitle: "\u8fd0\u884c\u65e5\u5fd7",
  clearLog: "\u6e05\u7a7a\u65e5\u5fd7",
  previewTitle: "\u63d0\u53d6\u9884\u89c8",
  chooseInputHint: "\u9009\u62e9\u8f93\u5165\u76ee\u5f55\u540e\u663e\u793a\u8bc6\u522b\u7ed3\u679c",
  cards: "\u5361\u7247",
  missingAbdata: "\u7f3a\u5931 abdata",
  gamePath: "\u6e38\u620f\u8def\u5f84",
  inputDir: "\u8f93\u5165\u76ee\u5f55",
  outputDir: "\u8f93\u51fa\u76ee\u5f55",
  sortPath: "\u6574\u7406\u8def\u5f84",
  chooseGamePath: "\u9009\u62e9\u6e38\u620f\u8def\u5f84",
  chooseInputDir: "\u9009\u62e9\u8f93\u5165\u76ee\u5f55",
  chooseOutputDir: "\u9009\u62e9\u8f93\u51fa\u76ee\u5f55",
  chooseSortPath: "\u9009\u62e9\u6574\u7406\u8def\u5f84",
  inputPlaceholder: "\u9009\u62e9\u5305\u542b PNG \u4eba\u7269\u5361\u7684\u76ee\u5f55",
  outputPlaceholder: "\u672a\u9009\u62e9\u65f6\u9ed8\u8ba4\u4f7f\u7528 input/output",
  sortPlaceholder: "\u9009\u62e9\u9700\u8981\u6574\u7406 zipmod \u7684\u76ee\u5f55",
  gameDirStatus: "\u6e38\u620f\u76ee\u5f55",
  recognizedCards: "\u5df2\u8bc6\u522b\u5361\u7247",
  unchecked: "\u672a\u6821\u9a8c",
  valid: "\u6709\u6548",
  invalid: "\u65e0\u6548",
  extract: "\u63d0\u53d6",
  pause: "\u6682\u505c",
  search: "\u641c\u7d22",
  sort: "\u6574\u7406",
  startSort: "\u5f00\u59cb\u6574\u7406",
  cancel: "\u53d6\u6d88",
  task: "\u4efb\u52a1",
  buttonPressed: "\u6309\u94ae\u5df2\u6309\u4e0b",
  sortDialogTitle: "\u6574\u7406 zipmod",
  sortDialogHint: "\u9009\u62e9\u4e00\u4e2a\u76ee\u5f55\uff0c\u70b9\u51fb\u5f00\u59cb\u540e\u4f1a\u5728\u8be5\u76ee\u5f55\u4e0b\u6267\u884c\u6574\u7406\u4efb\u52a1\u3002",
  sortPathRequired: "\u8bf7\u5148\u9009\u62e9\u6574\u7406\u8def\u5f84\u3002"
};

const paths = reactive({
  gameDir: "",
  inputDir: "",
  outputDir: ""
});

const stats = reactive({
  cards: 0,
  zipmods: 0,
  abdata: 0
});

const logs = ref(["Ready.", "[Mode] zipmod extract mode: Copy"]);
const taskName = ref(t.noTask);
const progress = ref(0);
const mode = ref("copy");
const backendStatus = ref("checking");
const gameDirStatus = ref(t.unchecked);
const cardPaths = ref([]);
const activeButton = ref("");
const isBusy = ref(false);
const showSortDialog = ref(false);
const sortPath = ref("");
const lastMessageCountByTask = reactive({});

const actionButtons = [
  { type: "extract_mods", label: t.extract, primary: true },
  { type: "pause", label: t.pause },
  { type: "search_cards", label: t.search },
  { type: "sort_dialog", label: t.sort }
];

async function selectPath(key, title) {
  const selected = await window.desktopApi.selectDirectory(title);
  if (!selected) {
    return;
  }

  paths[key] = selected;
  logs.value.push(`[Path] ${title}: ${selected}`);

  if (key === "gameDir") {
    await submitTask("check_game_dir");
  }

  if (key === "inputDir") {
    await submitTask("search_cards");
  }
}

async function selectSortPath() {
  const selected = await window.desktopApi.selectDirectory(t.chooseSortPath);
  if (!selected) {
    return;
  }

  sortPath.value = selected;
  logs.value.push(`[Path] ${t.chooseSortPath}: ${selected}`);
}

async function pingBackend() {
  try {
    const result = await window.desktopApi.backendRequest("/health");
    backendStatus.value = result.ok ? "ready" : "error";
    logs.value.push(`[Backend] ${result.message}`);
  } catch (error) {
    backendStatus.value = "error";
    logs.value.push(`[Backend Error] ${error.message}`);
  }
}

function buildPayload(overrides = {}) {
  return {
    game_dir: String(paths.gameDir || ""),
    input_dir: String(paths.inputDir || ""),
    output_dir: String(paths.outputDir || ""),
    card_paths: Array.from(cardPaths.value || []),
    zipmod_extract_mode: String(mode.value || "copy"),
    ...overrides
  };
}

function appendTaskLogs(task) {
  const messages = task.messages || [];
  const previousCount = lastMessageCountByTask[task.id] || 0;
  for (const message of messages.slice(previousCount)) {
    logs.value.push(`[Task] ${message}`);
  }
  lastMessageCountByTask[task.id] = messages.length;

  if (task.error && task.status === "failed") {
    const marker = `${task.id}:error`;
    if (!lastMessageCountByTask[marker]) {
      logs.value.push(`[Task Error] ${task.error}`);
      lastMessageCountByTask[marker] = 1;
    }
  }
}

function applyTaskResult(task) {
  taskName.value = task.title || task.task_type || t.task;
  progress.value = Number(task.progress || 0);
  appendTaskLogs(task);

  if (task.task_type === "check_game_dir") {
    gameDirStatus.value = task.data?.is_valid ? t.valid : t.invalid;
  }

  if (task.task_type === "search_cards") {
    cardPaths.value = task.data?.card_paths || cardPaths.value;
    stats.cards = task.data?.card_count ?? stats.cards;
  }

  if (task.task_type === "extract_mods") {
    if (task.data?.output_dir) {
      paths.outputDir = task.data.output_dir;
    }
    cardPaths.value = task.data?.card_paths || cardPaths.value;
    stats.cards = cardPaths.value.length;
    stats.zipmods = task.data?.matched_mod_count ?? stats.zipmods;
    stats.abdata = task.data?.missing_abdata?.length ?? stats.abdata;
  }

  if (task.task_type === "sort_mods") {
    stats.zipmods = task.data?.processed_count ?? stats.zipmods;
  }
}

async function pollTask(taskId, buttonType) {
  for (;;) {
    const result = await window.desktopApi.backendRequest(`/tasks/${taskId}`);
    if (!result.ok) {
      logs.value.push(`[Task Error] ${result.error || "unknown error"}`);
      break;
    }

    applyTaskResult(result.task);

    if (result.task.status === "completed" || result.task.status === "failed") {
      break;
    }

    await new Promise((resolve) => window.setTimeout(resolve, 300));
  }

  finishButtonFeedback(buttonType);
}

function finishButtonFeedback(type) {
  window.setTimeout(() => {
    if (activeButton.value === type) {
      activeButton.value = "";
    }
    isBusy.value = false;
  }, 240);
}

function openSortDialog() {
  activeButton.value = "sort_dialog";
  logs.value.push(`[UI] ${t.sort} ${t.buttonPressed}`);
  if (!sortPath.value) {
    sortPath.value = paths.inputDir || "";
  }
  showSortDialog.value = true;
  finishButtonFeedback("sort_dialog");
}

async function startSortTask() {
  if (!sortPath.value) {
    logs.value.push(`[Task Error] ${t.sortPathRequired}`);
    return;
  }

  showSortDialog.value = false;
  await submitTask("sort_mods", {
    input_dir: String(sortPath.value),
    output_dir: String(sortPath.value)
  });
}

async function submitTask(type, payloadOverrides = {}) {
  if (type === "sort_dialog") {
    openSortDialog();
    return;
  }

  activeButton.value = type;
  isBusy.value = true;
  logs.value.push(`[UI] ${buttonLabel(type)} ${t.buttonPressed}`);

  if (type === "pause") {
    logs.value.push(`[Task] ${t.pauseMessage}`);
    taskName.value = t.pauseNotReady;
    progress.value = 0;
    finishButtonFeedback(type);
    return;
  }

  try {
    const result = await window.desktopApi.backendRequest("/tasks", {
      method: "POST",
      body: { task_type: type, payload: buildPayload(payloadOverrides) }
    });

    if (!result.ok) {
      logs.value.push(`[Task Error] ${result.error || "unknown error"}`);
      finishButtonFeedback(type);
      return;
    }

    lastMessageCountByTask[result.task.id] = 0;
    applyTaskResult(result.task);
    await pollTask(result.task.id, type);
  } catch (error) {
    logs.value.push(`[Task Error] ${error.message}`);
    finishButtonFeedback(type);
  }
}

function buttonLabel(type) {
  if (type === "sort_mods") {
    return t.sort;
  }
  return actionButtons.find((button) => button.type === type)?.label || type;
}

function clearLogs() {
  logs.value = [];
}

onMounted(() => {
  pingBackend();
});
</script>

<template>
  <main class="shell">
    <header class="topbar">
      <div class="brand">
        <div class="mark">Z</div>
        <div>
          <strong>Star_Manager</strong>
          <span>{{ t.brandSubtitle }}</span>
        </div>
      </div>
      <div class="chip" :class="backendStatus">Python backend: {{ backendStatus }}</div>
    </header>

    <section class="main-grid">
      <section class="panel log-panel">
        <div class="panel-head">
          <h2>{{ t.logTitle }}</h2>
          <button class="icon-button" :title="t.clearLog" @click="clearLogs">x</button>
        </div>
        <pre class="terminal">{{ logs.join("\n") }}</pre>
      </section>

      <aside class="panel preview-panel">
        <div class="preview-title">
          <h2>{{ t.previewTitle }}</h2>
          <span>Card / zipmod / abdata</span>
        </div>
        <div class="card-drop">
          <strong>HS2 Card</strong>
          <span>{{ t.chooseInputHint }}</span>
        </div>
        <div class="stats">
          <div><b>{{ stats.cards }}</b><span>{{ t.cards }}</span></div>
          <div><b>{{ stats.zipmods }}</b><span>zipmod</span></div>
          <div><b>{{ stats.abdata }}</b><span>{{ t.missingAbdata }}</span></div>
        </div>
        <code class="tree">output/
|- mods/
`- UserData/chara/female/</code>
      </aside>
    </section>

    <section class="bottom-grid">
      <section class="panel path-panel">
        <label>
          <span>{{ t.gamePath }}</span>
          <input :value="paths.gameDir" readonly placeholder="D:\\HoneySelect2" />
          <button @click="selectPath('gameDir', t.chooseGamePath)">...</button>
        </label>
        <label>
          <span>{{ t.inputDir }}</span>
          <input :value="paths.inputDir" readonly :placeholder="t.inputPlaceholder" />
          <button @click="selectPath('inputDir', t.chooseInputDir)">...</button>
        </label>
        <label>
          <span>{{ t.outputDir }}</span>
          <input :value="paths.outputDir" readonly :placeholder="t.outputPlaceholder" />
          <button @click="selectPath('outputDir', t.chooseOutputDir)">...</button>
        </label>
        <p class="path-hint">{{ t.gameDirStatus }}: {{ gameDirStatus }} · {{ t.recognizedCards }}: {{ cardPaths.length }}</p>
      </section>

      <section class="panel action-panel">
        <div class="button-strip">
          <button
            v-for="button in actionButtons"
            :key="button.type"
            :class="{
              primary: button.primary,
              active: activeButton === button.type,
              busy: isBusy && activeButton === button.type
            }"
            @click="submitTask(button.type)"
          >
            {{ button.label }}
          </button>
        </div>
        <div class="status-row">
          <div class="task-name">{{ taskName }}</div>
          <progress :value="progress" max="100"></progress>
          <select v-model="mode">
            <option value="copy">Copy</option>
            <option value="move">Cut</option>
          </select>
        </div>
      </section>
    </section>

    <div v-if="showSortDialog" class="modal-backdrop" @click.self="showSortDialog = false">
      <section class="sort-dialog" role="dialog" aria-modal="true" :aria-label="t.sortDialogTitle">
        <header class="sort-dialog-head">
          <h2>{{ t.sortDialogTitle }}</h2>
          <button class="dialog-close" @click="showSortDialog = false">x</button>
        </header>
        <p class="dialog-hint">{{ t.sortDialogHint }}</p>
        <label class="sort-path-row">
          <span>{{ t.sortPath }}</span>
          <input :value="sortPath" readonly :placeholder="t.sortPlaceholder" />
          <button @click="selectSortPath">...</button>
        </label>
        <footer class="dialog-actions">
          <button class="secondary-action" @click="showSortDialog = false">{{ t.cancel }}</button>
          <button class="primary-action" @click="startSortTask">{{ t.startSort }}</button>
        </footer>
      </section>
    </div>
  </main>
</template>
