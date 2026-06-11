from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from bridge import create_health_payload, task_store


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        route = urlparse(self.path).path
        if route == "/health":
            self.send_json(create_health_payload())
            return

        if route == "/tasks":
            self.send_json({"ok": True, "tasks": task_store.list_tasks()})
            return

        if route.startswith("/tasks/"):
            task_id = route.removeprefix("/tasks/")
            task = task_store.get_task(task_id)
            if task is None:
                self.send_json({"ok": False, "error": f"Task not found: {task_id}"}, status=404)
                return
            self.send_json({"ok": True, "task": task.to_dict()})
            return

        self.send_json({"ok": False, "error": f"Unknown route: {route}"}, status=404)

    def do_POST(self) -> None:
        route = urlparse(self.path).path
        body = self.read_json_body()

        if route == "/tasks":
            task_type = body.get("task_type", "")
            payload = body.get("payload") or {}
            task = task_store.create_task(task_type, payload)
            self.send_json({"ok": True, "task": task.to_dict()})
            return

        self.send_json({"ok": False, "error": f"Unknown route: {route}"}, status=404)

    def read_json_body(self) -> dict:
        length = int(self.headers.get("content-length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    port = int(os.environ.get("STAR_MANAGER_BACKEND_PORT", "8765"))
    server = ThreadingHTTPServer(("127.0.0.1", port), RequestHandler)
    print(f"Star_Manager backend listening on http://127.0.0.1:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
