from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Page:
    items: list[str]
    total: int
    has_more: bool
    next_cursor: str | None

    def to_tool_result(self) -> dict:
        return {
            "content": self.items,
            "metadata": {
                "total": self.total,
                "has_more": self.has_more,
                "next_cursor": self.next_cursor,
            },
        }


def encode_cursor(offset: int) -> str:
    payload = json.dumps({"offset": offset}, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(payload).decode().rstrip("=")


def decode_cursor(cursor: str | None) -> int:
    if not cursor:
        return 0
    padding = "=" * (-len(cursor) % 4)
    decoded = base64.urlsafe_b64decode((cursor + padding).encode())
    payload = json.loads(decoded)
    offset = payload.get("offset")
    if not isinstance(offset, int) or offset < 0:
        raise ValueError("invalid cursor")
    return offset


def paginate(items: Iterable[str], *, cursor: str | None = None, limit: int = 50) -> Page:
    if limit < 1 or limit > 200:
        raise ValueError("limit must be between 1 and 200")
    values = list(items)
    offset = decode_cursor(cursor)
    page_items = values[offset : offset + limit]
    next_offset = offset + len(page_items)
    has_more = next_offset < len(values)
    return Page(
        items=page_items,
        total=len(values),
        has_more=has_more,
        next_cursor=encode_cursor(next_offset) if has_more else None,
    )


def read_all(items: Iterable[str], *, limit: int = 50) -> list[str]:
    values = list(items)
    cursor = None
    collected: list[str] = []
    while True:
        page = paginate(values, cursor=cursor, limit=limit)
        collected.extend(page.items)
        if not page.has_more:
            break
        cursor = page.next_cursor
    return collected
