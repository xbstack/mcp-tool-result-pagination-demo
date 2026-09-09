import json
from pathlib import Path
from pagination_demo import paginate, read_all

items = [f"row-{i:04d}" for i in range(503)]
first = paginate(items, limit=100)
second = paginate(items, cursor=first.next_cursor, limit=100)
all_items = read_all(items, limit=100)

checks = {
    "first_page_count": len(first.items) == 100,
    "first_has_more": first.has_more is True,
    "cursor_advances": second.items[0] == "row-0100",
    "total_preserved": first.total == 503 and second.total == 503,
    "complete_reconstruction": all_items == items,
    "last_item_preserved": all_items[-1] == "row-0502",
}
result = {
    "result": "PASS" if all(checks.values()) else "FAIL",
    "checks": checks,
    "example_first_result": first.to_tool_result(),
}
Path("results").mkdir(exist_ok=True)
Path("results/verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps({"result": result["result"], "checks": checks}, indent=2))
