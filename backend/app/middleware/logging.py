import time
from typing import Callable
from starlette.types import ASGIApp, Receive, Scope, Send

class RequestLoggingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope.get("method")
        path = scope.get("path")
        start = time.time()
        status_code_container = {"code": None}

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code_container["code"] = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
            dur_ms = (time.time() - start) * 1000
            print(f"REQ {method} {path} -> {status_code_container['code']} in {dur_ms:.2f}ms")
        except Exception as e:
            dur_ms = (time.time() - start) * 1000
            print(f"ERR {method} {path} -> 500 in {dur_ms:.2f}ms :: {type(e).__name__}: {e}")
            raise
