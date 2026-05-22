// DOM
const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);

const keySection = $("#key-section");
const uploadSection = $("#upload-section");
const progressSection = $("#progress-section");
const resultSection = $("#result-section");
const errorSection = $("#error-section");

const apiKeyInput = $("#api-key");
const proxyUrlInput = $("#proxy-url");
const btnNext = $("#btn-next");
const btnEye = $("#btn-eye");
const keyError = $("#key-error");

const dropZone = $("#drop-zone");
const fileInput = $("#file-input");
const fileInfo = $("#file-info");
const fileNameEl = $("#file-name");
const btnRemove = $("#btn-remove");
const btnStart = $("#btn-start");
const btnBack = $("#btn-back");
const uploadError = $("#upload-error");

const progressFill = $("#progress-fill");
const progressMsg = $("#progress-msg");
const progressPct = $("#progress-pct");

const btnDownload = $("#btn-download");
const btnNew = $("#btn-new");
const btnRetry = $("#btn-retry");
const errorMsg = $("#error-msg");

let apiKey = "";
let proxyUrl = "";
let selectedFile = null;
let results = null;

// ===== Step 1: API Key =====
apiKeyInput.addEventListener("input", () => {
    btnNext.disabled = apiKeyInput.value.trim().length < 10;
    hide(keyError);
});

apiKeyInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !btnNext.disabled) btnNext.click();
});

btnEye.addEventListener("click", () => {
    apiKeyInput.type = apiKeyInput.type === "password" ? "text" : "password";
});

btnNext.addEventListener("click", () => {
    const val = apiKeyInput.value.trim();
    if (!val.startsWith("sk-") || val.length < 20) {
        showErr(keyError, "API Key 格式不正确，应以 sk- 开头");
        return;
    }
    apiKey = val;
    proxyUrl = proxyUrlInput.value.trim();
    show("upload");
});

// ===== Step 2: Upload =====
btnBack.addEventListener("click", () => show("key"));

dropZone.addEventListener("click", () => fileInput.click());
dropZone.addEventListener("dragover", (e) => { e.preventDefault(); dropZone.classList.add("over"); });
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("over"));
dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("over");
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener("change", () => { if (fileInput.files.length) handleFile(fileInput.files[0]); });

function handleFile(file) {
    const ext = file.name.split(".").pop().toLowerCase();
    if (!["tex", "md", "txt"].includes(ext)) {
        showErr(uploadError, "请上传 .tex / .md / .txt 文件");
        return;
    }
    selectedFile = file;
    fileNameEl.textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    fileInfo.classList.remove("hidden");
    dropZone.classList.add("hidden");
    btnStart.disabled = false;
    hide(uploadError);
}

btnRemove.addEventListener("click", () => {
    selectedFile = null;
    fileInput.value = "";
    fileInfo.classList.add("hidden");
    dropZone.classList.remove("hidden");
    btnStart.disabled = true;
});

btnStart.addEventListener("click", async () => {
    if (!selectedFile) return;
    btnStart.disabled = true;
    btnStart.textContent = "读取文件...";

    try {
        const text = await selectedFile.text();
        if (text.trim().length < 100) {
            showErr(uploadError, "论文内容过短，请上传完整论文");
            btnStart.disabled = false;
            btnStart.innerHTML = '开始优化 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>';
            return;
        }

        const discipline = $("#discipline").value;
        const citation = $("#citation").value;

        show("progress");
        results = await runPipeline(text, apiKey, proxyUrl, discipline, citation, onProgress);
        displayResults(results);
        show("result");
    } catch (err) {
        showError(err.message);
    } finally {
        btnStart.disabled = false;
        btnStart.innerHTML = '开始优化 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>';
    }
});

// ===== Progress =====
function onProgress(stage, pct, msg) {
    progressFill.style.width = `${pct}%`;
    progressMsg.textContent = msg;
    progressPct.textContent = `${pct}%`;

    const order = ["analyze", "reduce_ai", "reduce_plagiarism", "polish", "check_format", "evaluate"];
    const idx = order.indexOf(stage);
    $$(".stage").forEach((el, i) => {
        el.classList.remove("active", "done");
        if (i < idx) el.classList.add("done");
        else if (i === idx) el.classList.add("active");
    });
}

// ===== Results =====
function displayResults(r) {
    $("#panel-evaluation").textContent = r.evaluation || "暂无";
    $("#panel-analysis").textContent = r.analysis || "暂无";
    $("#panel-format").textContent = r.format_report || "暂无";

    let logs = "";
    if (r.revision_logs && r.revision_logs.length) {
        for (const [stage, log] of r.revision_logs) {
            logs += `=== ${stage} ===\n\n${log}\n\n`;
        }
    }
    $("#panel-logs").textContent = logs || "暂无修订日志";
}

// Tabs
$$(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
        $$(".tab").forEach((t) => t.classList.remove("active"));
        $$(".panel").forEach((p) => p.classList.remove("active"));
        tab.classList.add("active");
        $(`#panel-${tab.dataset.t}`).classList.add("active");
    });
});

// Download
btnDownload.addEventListener("click", () => {
    if (!results || !results.polished) return;
    const blob = new Blob([results.polished], { type: "text/markdown;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "optimized_thesis.md";
    a.click();
    URL.revokeObjectURL(a.href);
});

// New / Retry
btnNew.addEventListener("click", reset);
btnRetry.addEventListener("click", reset);

function reset() {
    selectedFile = null;
    results = null;
    fileInput.value = "";
    fileInfo.classList.add("hidden");
    dropZone.classList.remove("hidden");
    btnStart.disabled = true;
    progressFill.style.width = "0%";
    progressMsg.textContent = "准备中...";
    progressPct.textContent = "0%";
    $$(".stage").forEach((el) => el.classList.remove("active", "done"));
    $$(".tab").forEach((t, i) => t.classList.toggle("active", i === 0));
    $$(".panel").forEach((p, i) => p.classList.toggle("active", i === 0));
    hide(uploadError);
    show("upload");
}

// ===== Helpers =====
function show(name) {
    [keySection, uploadSection, progressSection, resultSection, errorSection].forEach((s) => s.classList.add("hidden"));
    const map = { key: keySection, upload: uploadSection, progress: progressSection, result: resultSection, error: errorSection };
    if (map[name]) map[name].classList.remove("hidden");
}

function showErr(el, msg) { el.textContent = msg; el.classList.remove("hidden"); }
function hide(el) { el.classList.add("hidden"); }
function showError(msg) { errorMsg.textContent = msg; show("error"); }
