# MCP Tool Result Pagination Demo

Minimal XBSTACK fixture for application-level pagination of large MCP-style tool results.

This repository does **not** claim that MCP defines a universal 64 KB tool-result limit. The MCP specification does not define such a limit. Real truncation can come from a client, SDK implementation, context budget, proxy/message-size boundary, or timeout. The fixture demonstrates a safer application-level response contract for large results: bounded page size, `total`, `has_more`, and an opaque continuation cursor.

## Run

```bash
python3 verify.py
python3 -m unittest -v
```

Expected result:

```text
PASS
```

The verification reconstructs all 503 rows across cursor pages and checks that no row is silently dropped.

## Related XBSTACK guide

[MCP Tool Call Result Truncated: pagination, cursor, and result-size troubleshooting](https://www.xbstack.com/ai/mcp-tool-call-truncated-fix/?utm_source=github&utm_medium=referral&utm_campaign=mcp_tool_result_truncated&utm_content=repository_readme)

Related reading:

- [MCP -32700 Parse Error troubleshooting](https://www.xbstack.com/ai/mcp-json-rpc-parse-error/?utm_source=github&utm_medium=referral&utm_campaign=mcp_tool_result_truncated&utm_content=related_1)
- [MCP Streamable HTTP deployment](https://www.xbstack.com/ai/mcp-streamable-http-deployment/?utm_source=github&utm_medium=referral&utm_campaign=mcp_tool_result_truncated&utm_content=related_2)
- [MCP OAuth authentication](https://www.xbstack.com/ai/mcp-oauth-authentication/?utm_source=github&utm_medium=referral&utm_campaign=mcp_tool_result_truncated&utm_content=related_3)
