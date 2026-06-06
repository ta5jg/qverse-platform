# Q-Verse Clients V10.1+

Q-Verse clients connect external tools to the live Q-Verse Agent API.

Supported clients:

- CLI
- Cursor
- VS Code
- Web Console
- GitHub Actions
- n8n workflow template
- MCP bridge scaffold

Default endpoint:

```text
https://api.q-verse.io/agents/chat
```

Standard request body:

```json
{
  "message": "Hello Q-Verse",
  "source": "client-name",
  "user_id": "local-user",
  "username": "optional",
  "context": {}
}
```
