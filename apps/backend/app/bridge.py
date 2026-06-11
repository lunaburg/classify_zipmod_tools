from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock, Thread
from time import time
from uuid import uuid4

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from star_manager.core.config import ConfigDataList
from star_manager.core.zipmod_utils import is_hs2_game_dir
from star_manager.services.mod_workflow import ExtractOptions, WorkflowReporter, extract_mods, search_ais_cards, sort_mods


@dataclass
class TaskState:
    id: str
    task_type: str
    status: str = "queued"
    progress: int = 0
    title: str = "Waiting"
    messages: list[str] = field(default_factory=list)
    error: str = ""
    data: dict = field(default_factory=dict)
    created_at: float = field(default_factory=time)
    updated_at: float = field(default_factory=time)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "task_type": self.task_type,
            "status": self.status,
            "progress": self.progress,
            "title": self.title,
            "messages": list(self.messages),
            "error": self.error,
            "data": self.data,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class TaskStore:
    def __init__(self) -> None:
        self._tasks: dict[str, TaskState] = {}
        self._lock = Lock()

    def create_task(self, task_type: str, payload: dict | None = None) -> TaskState:
        task = TaskState(
            id=uuid4().hex,
            task_type=task_type,
            title=task_type or "Unnamed task",
            messages=[f"Task submitted: {task_type}"],
        )
        with self._lock:
            self._tasks[task.id] = task
        Thread(target=run_task, args=(task, payload or {}), daemon=True).start()
        return task

    def get_task(self, task_id: str) -> TaskState | None:
        with self._lock:
            return self._tasks.get(task_id)

    def list_tasks(self) -> list[dict]:
        with self._lock:
            return [task.to_dict() for task in self._tasks.values()]


task_store = TaskStore()


def create_health_payload() -> dict:
    return {
        "ok": True,
        "message": "Python backend is ready.",
        "service": "Star_Manager",
        "transport": "http-api",
    }


def build_reporter(task: TaskState) -> WorkflowReporter:
    def set_progress(value):
        task.progress = int(value)
        task.updated_at = time()

    def add_message(text):
        task.messages.append(text)
        task.updated_at = time()

    def set_title(text):
        task.title = text
        task.updated_at = time()

    return WorkflowReporter(
        on_progress=set_progress,
        on_message=add_message,
        on_title=set_title,
        on_result=add_message,
    )


def run_task(task: TaskState, payload: dict) -> None:
    reporter = build_reporter(task)
    task.status = "running"
    task.updated_at = time()

    try:
        if task.task_type == "check_game_dir":
            game_dir = str(payload.get("game_dir") or "")
            task.title = "Check game directory"
            task.data = {"is_valid": is_hs2_game_dir(game_dir), "game_dir": game_dir}
        elif task.task_type == "search_cards":
            input_dir = str(payload.get("input_dir") or "")
            card_paths = search_ais_cards(input_dir, reporter)
            task.data = {"card_paths": sorted(card_paths), "card_count": len(card_paths)}
        elif task.task_type == "extract_mods":
            result = extract_mods(
                ExtractOptions(
                    game_dir=str(payload.get("game_dir") or ""),
                    input_dir=str(payload.get("input_dir") or ""),
                    output_dir=str(payload.get("output_dir") or ""),
                    card_paths=set(payload.get("card_paths") or []),
                    zipmod_extract_mode=str(payload.get("zipmod_extract_mode") or ConfigDataList.ZIPMOD_MODE_COPY),
                ),
                reporter,
            )
            task.data = {
                "output_dir": result.output_dir,
                "card_paths": sorted(result.card_paths),
                "required_guid_count": len(result.required_guids),
                "matched_mod_count": len(result.matched_mod_paths),
                "missing_mods": sorted(result.missing_mods),
                "missing_abdata": sorted(result.missing_abdata),
            }
        elif task.task_type == "sort_mods":
            result = sort_mods(
                str(payload.get("input_dir") or ""),
                output_dir=str(payload.get("output_dir") or "") or None,
                delete_empty=bool(payload.get("delete_empty")),
                reporter=reporter,
            )
            task.data = {"output_dir": result.output_dir, "processed_count": result.processed_count}
        else:
            raise ValueError(f"Unknown task type: {task.task_type}")

        task.progress = 100
        task.status = "completed"
    except Exception as error:
        task.error = str(error)
        task.status = "failed"
        task.messages.append(f"[Error] {error}")
    finally:
        task.updated_at = time()
