#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEAL Flask backend: upload IR image, enhance, return result."""

from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, redirect, request, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

from inference import enhance, init_model, is_model_loaded

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BACKEND_DIR / "uploads"
RESULT_FOLDER = BACKEND_DIR / "results"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
CORS(app)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _frontend_dist_dir() -> Path | None:
    dist = PROJECT_ROOT / "frontend" / "dist"
    if dist.is_dir() and (dist / "index.html").is_file():
        return dist
    return None


def _register_bundled_frontend(dist: Path) -> None:
    @app.route("/")
    def _root_redirect():
        return redirect("/DEAL/")

    @app.route("/DEAL/", defaults={"path": ""})
    @app.route("/DEAL/<path:path>")
    def _serve_frontend(path: str):
        if path:
            try:
                candidate = (dist / path).resolve()
                dist_r = dist.resolve()
                if candidate.is_file() and candidate.is_relative_to(dist_r):
                    return send_from_directory(dist, path)
            except (ValueError, OSError):
                pass
        return send_from_directory(dist, "index.html")


def _maybe_register_bundled_frontend() -> None:
    dist = _frontend_dist_dir()
    if dist and os.environ.get("DEAL_SERVE_FRONTEND") == "1":
        _register_bundled_frontend(dist)
        logger.info("Serving frontend from %s at /DEAL/", dist)


_maybe_register_bundled_frontend()


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify(
        {
            "status": "healthy",
            "model_loaded": is_model_loaded(),
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/api/upload", methods=["POST"])
def upload_file():
    try:
        if "ir_image" not in request.files:
            return jsonify({"success": False, "error": "请上传红外图像 (ir_image)"}), 400

        ir_file = request.files["ir_image"]
        if not ir_file.filename:
            return jsonify({"success": False, "error": "文件名不能为空"}), 400

        filename = secure_filename(ir_file.filename)
        if not allowed_file(filename):
            return jsonify(
                {
                    "success": False,
                    "error": "不支持的文件格式，请上传 PNG、JPG 或 BMP",
                }
            ), 400

        session_id = str(uuid.uuid4())
        ext = filename.rsplit(".", 1)[1].lower()
        ir_filename = f"{session_id}_ir.{ext}"
        ir_path = UPLOAD_FOLDER / ir_filename
        ir_file.save(str(ir_path))

        logger.info("Uploaded %s", ir_filename)
        return jsonify(
            {
                "success": True,
                "session_id": session_id,
                "ir_filename": ir_filename,
                "message": "文件上传成功",
            }
        )
    except Exception as exc:
        logger.exception("Upload failed")
        return jsonify({"success": False, "error": f"文件上传失败: {exc}"}), 500


@app.route("/api/process", methods=["POST"])
def process_image():
    try:
        data = request.get_json(silent=True) or {}
        session_id = data.get("session_id")
        if not session_id:
            return jsonify({"success": False, "error": "缺少 session_id 参数"}), 400

        ir_files = list(UPLOAD_FOLDER.glob(f"{session_id}_ir.*"))
        if not ir_files:
            return jsonify({"success": False, "error": "找不到上传的红外图像"}), 404

        if not is_model_loaded():
            return jsonify({"success": False, "error": "DEAL 模型未加载"}), 500

        ir_path = ir_files[0]
        result_filename = f"{session_id}_enhanced.png"
        result_path = RESULT_FOLDER / result_filename

        enhance(ir_path, result_path)
        logger.info("Enhanced %s -> %s", ir_path.name, result_filename)

        return jsonify(
            {
                "success": True,
                "result_filename": result_filename,
                "message": "红外图像增强完成",
            }
        )
    except Exception as exc:
        logger.exception("Process failed")
        return jsonify({"success": False, "error": f"图像处理失败: {exc}"}), 500


@app.route("/api/result/<filename>", methods=["GET"])
def get_result(filename: str):
    try:
        safe_name = secure_filename(filename)
        if safe_name != filename:
            return jsonify({"success": False, "error": "非法文件名"}), 400

        result_path = RESULT_FOLDER / safe_name
        if not result_path.is_file():
            return jsonify({"success": False, "error": "结果文件不存在"}), 404

        response = send_file(str(result_path), mimetype="image/png")
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    except Exception as exc:
        logger.exception("Get result failed")
        return jsonify({"success": False, "error": f"获取结果失败: {exc}"}), 500


@app.route("/api/cleanup/<session_id>", methods=["DELETE"])
def cleanup_session(session_id: str):
    try:
        patterns = [
            f"{session_id}_ir.*",
            f"{session_id}_enhanced.*",
        ]
        removed = 0
        for folder in (UPLOAD_FOLDER, RESULT_FOLDER):
            for pattern in patterns:
                for path in folder.glob(pattern):
                    path.unlink(missing_ok=True)
                    removed += 1
        return jsonify({"success": True, "removed": removed})
    except Exception as exc:
        logger.exception("Cleanup failed")
        return jsonify({"success": False, "error": str(exc)}), 500


def main() -> None:
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))

    logger.info("Project root: %s", PROJECT_ROOT)
    logger.info("Upload dir: %s", UPLOAD_FOLDER)
    logger.info("Result dir: %s", RESULT_FOLDER)

    try:
        init_model()
        logger.info("DEAL model loaded successfully.")
    except Exception as exc:
        logger.error("DEAL model failed to load: %s", exc)

    app.run(host=host, port=port, debug=False, threaded=True)


if __name__ == "__main__":
    main()
