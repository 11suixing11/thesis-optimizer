"""FastAPI 主应用 — 论文优化 Web 服务"""

import asyncio
import json
import uuid
import zipfile
import io
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from core.optimizer import run_pipeline

app = FastAPI(title="论文优化系统", version="1.0.0")

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# 任务状态存储（内存）
tasks: dict[str, dict] = {}
# WebSocket 连接管理
_ws_connections: dict[str, list[WebSocket]] = {}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/api/upload")
async def upload_thesis(
    file: UploadFile = File(...),
    api_key: str = Form(...),
    discipline: str = Form("general"),
    citation_format: str = Form("gb/t 7714"),
):
    """上传论文并启动优化任务"""
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    if len(text.strip()) < 100:
        return JSONResponse(
            status_code=400,
            content={"error": "论文内容过短，请上传完整的论文文件"},
        )

    # 简单验证 API key 格式
    if not api_key.startswith("sk-") or len(api_key) < 20:
        return JSONResponse(
            status_code=400,
            content={"error": "API Key 格式不正确"},
        )

    task_id = str(uuid.uuid4())[:8]
    tasks[task_id] = {
        "status": "running",
        "stage": "init",
        "progress": 0,
        "message": "正在初始化...",
        "filename": file.filename,
        "discipline": discipline,
        "citation_format": citation_format,
        "text_length": len(text),
        "results": None,
        "error": None,
        "created_at": datetime.now().isoformat(),
    }

    asyncio.create_task(
        _run_optimization(task_id, text, api_key, discipline, citation_format)
    )
    return {"task_id": task_id}


async def _run_optimization(
    task_id: str, text: str, api_key: str, discipline: str, citation_format: str
):
    """后台执行优化流水线"""
    try:
        async def on_progress(stage: str, pct: int, msg: str):
            tasks[task_id]["stage"] = stage
            tasks[task_id]["progress"] = pct
            tasks[task_id]["message"] = msg
            if task_id in _ws_connections:
                payload = json.dumps(
                    {"stage": stage, "progress": pct, "message": msg},
                    ensure_ascii=False,
                )
                for ws in _ws_connections[task_id]:
                    try:
                        await ws.send_text(payload)
                    except Exception:
                        pass

        results = await run_pipeline(
            text, api_key, discipline, citation_format, on_progress
        )
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["results"] = results
        tasks[task_id]["progress"] = 100
        tasks[task_id]["message"] = "优化完成！"
        _save_results(task_id, results, text)

        if task_id in _ws_connections:
            for ws in _ws_connections[task_id]:
                try:
                    await ws.send_text(
                        json.dumps({"status": "completed"}, ensure_ascii=False)
                    )
                except Exception:
                    pass

    except Exception as e:
        tasks[task_id]["status"] = "error"
        tasks[task_id]["error"] = str(e)
        tasks[task_id]["message"] = f"出错了: {e}"
        if task_id in _ws_connections:
            for ws in _ws_connections[task_id]:
                try:
                    await ws.send_text(
                        json.dumps({"error": str(e)}, ensure_ascii=False)
                    )
                except Exception:
                    pass


def _save_results(task_id: str, results: dict, original_text: str):
    """将结果保存到 uploads/ 目录"""
    task_dir = UPLOAD_DIR / task_id
    task_dir.mkdir(exist_ok=True)

    (task_dir / "optimized_thesis.md").write_text(
        results.get("polished", ""), encoding="utf-8"
    )
    (task_dir / "evaluation.md").write_text(
        results.get("evaluation", ""), encoding="utf-8"
    )
    (task_dir / "analysis.md").write_text(
        results.get("analysis", ""), encoding="utf-8"
    )
    logs_text = ""
    for stage, log in results.get("revision_logs", []):
        logs_text += f"# {stage}\n\n{log}\n\n---\n\n"
    (task_dir / "revision_logs.md").write_text(logs_text, encoding="utf-8")
    (task_dir / "original.md").write_text(original_text, encoding="utf-8")
    (task_dir / "format_report.md").write_text(
        results.get("format_report", ""), encoding="utf-8"
    )


@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()
    _ws_connections.setdefault(task_id, []).append(websocket)
    try:
        if task_id in tasks:
            t = tasks[task_id]
            await websocket.send_text(
                json.dumps(
                    {
                        "stage": t["stage"],
                        "progress": t["progress"],
                        "message": t["message"],
                    },
                    ensure_ascii=False,
                )
            )
            if t["status"] in ("completed", "error"):
                await websocket.send_text(
                    json.dumps(
                        {"status": t["status"], "error": t.get("error")},
                        ensure_ascii=False,
                    )
                )
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        if task_id in _ws_connections and websocket in _ws_connections[task_id]:
            _ws_connections[task_id].remove(websocket)


@app.get("/api/task/{task_id}")
async def get_task(task_id: str):
    """查询任务状态"""
    if task_id not in tasks:
        return JSONResponse(status_code=404, content={"error": "任务不存在"})
    t = tasks[task_id]
    return {
        "task_id": task_id,
        "status": t["status"],
        "stage": t["stage"],
        "progress": t["progress"],
        "message": t["message"],
        "filename": t["filename"],
        "error": t.get("error"),
    }


@app.get("/api/task/{task_id}/result")
async def get_task_result(task_id: str):
    """获取任务结果"""
    if task_id not in tasks:
        return JSONResponse(status_code=404, content={"error": "任务不存在"})
    t = tasks[task_id]
    if t["status"] != "completed":
        return JSONResponse(status_code=400, content={"error": "任务尚未完成"})
    return {
        "analysis": t["results"]["analysis"],
        "evaluation": t["results"]["evaluation"],
        "format_report": t["results"]["format_report"],
        "revision_logs": t["results"]["revision_logs"],
    }


@app.get("/api/download/{task_id}")
async def download_result(task_id: str):
    """下载优化结果 ZIP 包"""
    task_dir = UPLOAD_DIR / task_id
    if not task_dir.exists():
        return JSONResponse(status_code=404, content={"error": "结果文件不存在"})

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in task_dir.iterdir():
            zf.write(f, f.name)
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="thesis_optimized_{task_id}.zip"'
        },
    )


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
