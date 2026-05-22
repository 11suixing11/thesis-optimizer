// DOM Elements
const keySection = document.getElementById("key-section");
const uploadSection = document.getElementById("upload-section");
const progressSection = document.getElementById("progress-section");
const resultSection = document.getElementById("result-section");
const errorSection = document.getElementById("error-section");

const apiKeyInput = document.getElementById("api-key");
const btnToggleKey = document.getElementById("btn-toggle-key");
const btnNext = document.getElementById("btn-next");
const keyError = document.getElementById("key-error");

const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const fileInfo = document.getElementById("file-info");
const fileName = document.getElementById("file-name");
const btnRemove = document.getElementById("btn-remove");
const btnUpload = document.getElementById("btn-upload");
const btnBack = document.getElementById("btn-back");
const uploadError = document.getElementById("upload-error");

const progressBar = document.getElementById("progress-bar");
const progressText = document.getElementById("progress-text");
const progressPercent = document.getElementById("progress-percent");

const btnDownload = document.getElementById("btn-download");
const btnNew = document.getElementById("btn-new");
const btnRetry = document.getElementById("btn-retry");
const errorMessage = document.getElementById("error-message");

const tabs = document.querySelectorAll(".tab");
const tabPanes = document.querySelectorAll(".tab-pane");

let apiKey = "";
let selectedFile = null;
let currentTaskId = null;
let ws = null;

// ===== Step 1: API Key =====

apiKeyInput.addEventListener("input", () => {
    const val = apiKeyInput.value.trim();
    btnNext.disabled = val.length < 10;
    hideError(keyError);
});

btnNext.addEventListener("click", () => {
    const val = apiKeyInput.value.trim();
    if (!val.startsWith("sk-") || val.length < 20) {
        showError(keyError, "API Key 格式不正确，应以 sk- 开头");
        return;
    }
    apiKey = val;
    showSection("upload");
});

btnToggleKey.addEventListener("click", () => {
    const isPassword = apiKeyInput.type === "password";
    apiKeyInput.type = isPassword ? "text" : "password";
});

// Enter key support
apiKeyInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !btnNext.disabled) {
        btnNext.click();
    }
});

// ===== Step 2: Upload =====

btnBack.addEventListener("click", () => {
    showSection("key");
});

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    if (e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]);
});

fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) handleFile(fileInput.files[0]);
});

function handleFile(file) {
    const ext = file.name.split(".").pop().toLowerCase();
    if (!["tex", "md", "txt"].includes(ext)) {
        showError(uploadError, "请上传 .tex / .md / .txt 文件");
        return;
    }
    selectedFile = file;
    fileName.textContent = file.name;
    fileInfo.classList.remove("hidden");
    dropZone.classList.add("hidden");
    btnUpload.disabled = false;
    hideError(uploadError);
}

btnRemove.addEventListener("click", () => {
    selectedFile = null;
    fileInput.value = "";
    fileInfo.classList.add("hidden");
    dropZone.classList.remove("hidden");
    btnUpload.disabled = true;
});

btnUpload.addEventListener("click", async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("api_key", apiKey);
    formData.append("discipline", document.getElementById("discipline").value);
    formData.append("citation_format", document.getElementById("citation").value);

    try {
        btnUpload.disabled = true;
        btnUpload.textContent = "上传中...";
        hideError(uploadError);

        const resp = await fetch("/api/upload", { method: "POST", body: formData });
        const data = await resp.json();

        if (!resp.ok) {
            showError(uploadError, data.error || "上传失败");
            btnUpload.disabled = false;
            btnUpload.innerHTML = '开始优化 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>';
            return;
        }

        currentTaskId = data.task_id;
        showSection("progress");
        connectWebSocket(currentTaskId);
    } catch (err) {
        showError(uploadError, "网络错误，请检查连接");
        btnUpload.disabled = false;
        btnUpload.innerHTML = '开始优化 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>';
    }
});

// ===== Step 3: Progress =====

function connectWebSocket(taskId) {
    const protocol = location.protocol === "https:" ? "wss:" : "ws:";
    ws = new WebSocket(`${protocol}//${location.host}/ws/${taskId}`);

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.error) {
            showErrorGlobal(data.error);
            return;
        }

        if (data.status === "completed") {
            loadResults(taskId);
            return;
        }

        updateProgress(data.stage, data.progress, data.message);
    };

    ws.onclose = () => {
        if (!progressSection.classList.contains("hidden")) {
            setTimeout(() => pollStatus(taskId), 2000);
        }
    };

    ws.onerror = () => {
        setTimeout(() => pollStatus(taskId), 2000);
    };
}

async function pollStatus(taskId) {
    try {
        const resp = await fetch(`/api/task/${taskId}`);
        const data = await resp.json();

        if (data.status === "completed") {
            loadResults(taskId);
        } else if (data.status === "error") {
            showErrorGlobal(data.error || "未知错误");
        } else {
            updateProgress(data.stage, data.progress, data.message);
            setTimeout(() => pollStatus(taskId), 3000);
        }
    } catch {
        setTimeout(() => pollStatus(taskId), 5000);
    }
}

function updateProgress(stage, progress, message) {
    progressBar.style.width = `${progress}%`;
    progressText.textContent = message;
    progressPercent.textContent = `${progress}%`;

    const stageOrder = [
        "analyze",
        "reduce_ai",
        "reduce_plagiarism",
        "polish",
        "check_format",
        "evaluate",
    ];
    const currentIdx = stageOrder.indexOf(stage);

    document.querySelectorAll(".stage").forEach((el, idx) => {
        el.classList.remove("active", "done");
        if (idx < currentIdx) el.classList.add("done");
        else if (idx === currentIdx) el.classList.add("active");
    });
}

// ===== Results =====

async function loadResults(taskId) {
    try {
        const resp = await fetch(`/api/task/${taskId}/result`);
        const data = await resp.json();

        if (!resp.ok) {
            showErrorGlobal(data.error || "获取结果失败");
            return;
        }

        document.getElementById("tab-evaluation").textContent =
            data.evaluation || "暂无评估报告";
        document.getElementById("tab-analysis").textContent =
            data.analysis || "暂无分析报告";
        document.getElementById("tab-format").textContent =
            data.format_report || "暂无格式报告";

        let logsText = "";
        if (data.revision_logs && data.revision_logs.length > 0) {
            for (const [stage, log] of data.revision_logs) {
                logsText += `=== ${stage} ===\n\n${log}\n\n`;
            }
        }
        document.getElementById("tab-logs").textContent = logsText || "暂无修订日志";

        showSection("result");
    } catch {
        showErrorGlobal("加载结果失败");
    }
}

// Tabs
tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
        tabs.forEach((t) => t.classList.remove("active"));
        tabPanes.forEach((p) => p.classList.remove("active"));
        tab.classList.add("active");
        document.getElementById(`tab-${tab.dataset.tab}`).classList.add("active");
    });
});

// Download
btnDownload.addEventListener("click", () => {
    if (currentTaskId) {
        window.location.href = `/api/download/${currentTaskId}`;
    }
});

// New Task
btnNew.addEventListener("click", () => resetToUpload());
btnRetry.addEventListener("click", () => resetToUpload());

// ===== Helpers =====

function showSection(name) {
    keySection.classList.add("hidden");
    uploadSection.classList.add("hidden");
    progressSection.classList.add("hidden");
    resultSection.classList.add("hidden");
    errorSection.classList.add("hidden");

    const map = {
        key: keySection,
        upload: uploadSection,
        progress: progressSection,
        result: resultSection,
        error: errorSection,
    };
    if (map[name]) map[name].classList.remove("hidden");
}

function showError(el, msg) {
    el.textContent = msg;
    el.classList.remove("hidden");
}

function hideError(el) {
    el.classList.add("hidden");
}

function showErrorGlobal(msg) {
    errorMessage.textContent = msg;
    showSection("error");
}

function resetToUpload() {
    currentTaskId = null;
    selectedFile = null;
    fileInput.value = "";
    fileInfo.classList.add("hidden");
    dropZone.classList.remove("hidden");
    btnUpload.disabled = true;
    btnUpload.innerHTML = '开始优化 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>';
    progressBar.style.width = "0%";
    progressText.textContent = "准备中...";
    progressPercent.textContent = "0%";
    document.querySelectorAll(".stage").forEach((el) => {
        el.classList.remove("active", "done");
    });
    hideError(uploadError);
    if (ws) {
        ws.close();
        ws = null;
    }
    showSection("upload");
}
