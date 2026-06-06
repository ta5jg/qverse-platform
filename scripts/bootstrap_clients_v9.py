
#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API_BASE_URL = "https://api.q-verse.io"
CHAT_ENDPOINT = f"{API_BASE_URL}/agents/chat"

FILES = {
    "clients/README.md": '''# Q-Verse Clients V10.1+

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
''',

    "clients/config/qverse-client-config.json": json.dumps({
        "version": "V10.1",
        "api_base_url": API_BASE_URL,
        "chat_endpoint": CHAT_ENDPOINT,
        "standard_body_fields": ["message", "source", "user_id", "username", "context"],
        "clients": ["cli", "cursor", "vscode", "web", "github", "n8n", "mcp"]
    }, indent=2) + "\n",

    "clients/cli/qverse.py": '''#!/usr/bin/env python3
import argparse
import json
import os
import sys
from typing import Any, Dict

try:
    import requests
except ImportError:
    print("Missing dependency: requests. Install with: pip install requests", file=sys.stderr)
    raise

DEFAULT_ENDPOINT = os.getenv("QVERSE_API_URL", "https://api.q-verse.io/agents/chat")


def build_payload(args: argparse.Namespace) -> Dict[str, Any]:
    context = {}
    if args.context:
        try:
            context = json.loads(args.context)
        except json.JSONDecodeError:
            context = {"raw_context": args.context}
    return {
        "message": args.message,
        "source": args.source,
        "user_id": args.user_id,
        "username": args.username,
        "context": context,
    }


def main():
    parser = argparse.ArgumentParser(description="Q-Verse CLI Client V10.1+")
    parser.add_argument("message", help="Message to send to Q-Verse Agent")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="Q-Verse chat endpoint")
    parser.add_argument("--source", default="cli", help="Client source name")
    parser.add_argument("--user-id", default=os.getenv("USER", "local-user"), help="User id")
    parser.add_argument("--username", default=os.getenv("USER", "local-user"), help="Username")
    parser.add_argument("--context", default="{}", help="JSON context")
    parser.add_argument("--json", action="store_true", help="Print full JSON response")
    args = parser.parse_args()

    payload = build_payload(args)
    try:
        response = requests.post(args.endpoint, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        if args.json:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(data.get("reply") or data.get("message") or json.dumps(data, ensure_ascii=False))
    except Exception as exc:
        print(f"Q-Verse request failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
''',

    "clients/cursor/qverse-client.js": '''// Q-Verse Cursor Client V10.1+
const DEFAULT_ENDPOINT = process.env.QVERSE_API_URL || 'https://api.q-verse.io/agents/chat';

async function askQVerse(message, options = {}) {
  const payload = {
    message,
    source: options.source || 'cursor',
    user_id: options.user_id || process.env.USER || 'cursor-user',
    username: options.username || process.env.USER || 'cursor-user',
    context: options.context || {}
  };

  const response = await fetch(options.endpoint || DEFAULT_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`Q-Verse API error: ${response.status} ${response.statusText}`);
  }

  return await response.json();
}

module.exports = { askQVerse };
''',

    "clients/vscode/package.json": json.dumps({
        "name": "qverse-vscode-client",
        "displayName": "Q-Verse Agent Client",
        "description": "Connect VS Code to Q-Verse Agent API",
        "version": "10.1.0",
        "engines": {"vscode": "^1.85.0"},
        "activationEvents": ["onCommand:qverse.askAgent", "onCommand:qverse.explainSelection"],
        "main": "./extension.js",
        "contributes": {
            "commands": [
                {"command": "qverse.askAgent", "title": "Q-Verse: Ask Agent"},
                {"command": "qverse.explainSelection", "title": "Q-Verse: Explain Selection"}
            ],
            "configuration": {
                "title": "Q-Verse",
                "properties": {
                    "qverse.apiUrl": {
                        "type": "string",
                        "default": CHAT_ENDPOINT,
                        "description": "Q-Verse Agent chat endpoint"
                    }
                }
            }
        }
    }, indent=2) + "\n",

    "clients/vscode/extension.js": '''// Q-Verse VS Code Client V10.1+
const vscode = require('vscode');

async function callQVerse(message, context = {}) {
  const config = vscode.workspace.getConfiguration('qverse');
  const endpoint = config.get('apiUrl') || 'https://api.q-verse.io/agents/chat';
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      source: 'vscode',
      user_id: process.env.USER || 'vscode-user',
      username: process.env.USER || 'vscode-user',
      context
    })
  });
  if (!response.ok) {
    throw new Error(`Q-Verse API error: ${response.status} ${response.statusText}`);
  }
  return await response.json();
}

function activate(context) {
  context.subscriptions.push(vscode.commands.registerCommand('qverse.askAgent', async () => {
    const message = await vscode.window.showInputBox({ prompt: 'Ask Q-Verse Agent...' });
    if (!message) return;
    try {
      const data = await callQVerse(message);
      vscode.window.showInformationMessage(data.reply || 'Q-Verse responded.');
    } catch (error) {
      vscode.window.showErrorMessage(String(error));
    }
  }));

  context.subscriptions.push(vscode.commands.registerCommand('qverse.explainSelection', async () => {
    const editor = vscode.window.activeTextEditor;
    const selected = editor ? editor.document.getText(editor.selection) : '';
    if (!selected) {
      vscode.window.showWarningMessage('No text selected.');
      return;
    }
    try {
      const data = await callQVerse('Explain this code selection.', { selected_text: selected });
      vscode.window.showInformationMessage(data.reply || 'Q-Verse responded.');
    } catch (error) {
      vscode.window.showErrorMessage(String(error));
    }
  }));
}

function deactivate() {}

module.exports = { activate, deactivate };
''',

    "clients/web/QVerseConsole.jsx": '''// Q-Verse Web Console V10.1+
import React, { useState } from "react";

const ENDPOINT = "https://api.q-verse.io/agents/chat";

export default function QVerseConsole() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");
  const [raw, setRaw] = useState(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    setLoading(true);
    setReply("");
    setRaw(null);
    try {
      const response = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          source: "web-console",
          user_id: "web-user",
          username: "web-user",
          context: { ui: "QVerseConsole" }
        })
      });
      const data = await response.json();
      setRaw(data);
      setReply(data.reply || JSON.stringify(data));
    } catch (error) {
      setReply(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section style={{ padding: 16, maxWidth: 900, margin: "0 auto" }}>
      <h2>Q-Verse Agent Console</h2>
      <textarea
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        placeholder="Ask Q-Verse Agent..."
        rows={6}
        style={{ width: "100%", padding: 12 }}
      />
      <button onClick={sendMessage} disabled={loading || !message.trim()} style={{ marginTop: 12 }}>
        {loading ? "Sending..." : "Send to Q-Verse"}
      </button>
      <div style={{ marginTop: 16 }}>
        <strong>Reply</strong>
        <pre style={{ whiteSpace: "pre-wrap" }}>{reply}</pre>
      </div>
      {raw && (
        <details>
          <summary>Raw Response</summary>
          <pre>{JSON.stringify(raw, null, 2)}</pre>
        </details>
      )}
    </section>
  );
}
''',

    "clients/github/qverse-action.yml": '''name: Q-Verse Agent Chat

on:
  workflow_dispatch:
    inputs:
      message:
        description: Message to send to Q-Verse Agent
        required: true
        default: Hello, Q-Verse!

jobs:
  qverse:
    runs-on: ubuntu-latest
    steps:
      - name: Send message to Q-Verse
        shell: bash
        run: |
          python3 - <<'PY'
          import json
          import os
          import urllib.request

          endpoint = "https://api.q-verse.io/agents/chat"
          payload = {
              "message": os.environ["QVERSE_MESSAGE"],
              "source": "github-actions",
              "user_id": os.environ.get("GITHUB_ACTOR", "github"),
              "username": os.environ.get("GITHUB_ACTOR", "github"),
              "context": {
                  "repository": os.environ.get("GITHUB_REPOSITORY", ""),
                  "run_id": os.environ.get("GITHUB_RUN_ID", "")
              }
          }
          request = urllib.request.Request(
              endpoint,
              data=json.dumps(payload).encode("utf-8"),
              headers={"Content-Type": "application/json"},
              method="POST",
          )
          with urllib.request.urlopen(request, timeout=60) as response:
              print(response.read().decode("utf-8"))
          PY
        env:
          QVERSE_MESSAGE: ${{ github.event.inputs.message }}
''',

    "clients/n8n/qverse-workflow-template.json": json.dumps({
        "name": "Q-Verse Agent API Template",
        "nodes": [
            {
                "parameters": {},
                "id": "manual-trigger",
                "name": "Manual Trigger",
                "type": "n8n-nodes-base.manualTrigger",
                "typeVersion": 1,
                "position": [250, 300]
            },
            {
                "parameters": {
                    "requestMethod": "POST",
                    "url": CHAT_ENDPOINT,
                    "jsonParameters": True,
                    "options": {},
                    "bodyParametersJson": json.dumps({
                        "message": "Hello Q-Verse from n8n",
                        "source": "n8n",
                        "user_id": "n8n-user",
                        "username": "n8n-user",
                        "context": {"workflow": "Q-Verse Agent API Template"}
                    })
                },
                "id": "qverse-http-request",
                "name": "Q-Verse Agent Chat",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 1,
                "position": [500, 300]
            }
        ],
        "connections": {
            "Manual Trigger": {
                "main": [[{"node": "Q-Verse Agent Chat", "type": "main", "index": 0}]]
            }
        }
    }, indent=2) + "\n",

    "clients/mcp/qverse-mcp-server.py": '''#!/usr/bin/env python3
"""Q-Verse MCP bridge scaffold.

This file is a lightweight starting point for exposing Q-Verse Agent API
as a tool-compatible bridge for MCP-style clients.
"""
import json
import os
import sys
import urllib.request

ENDPOINT = os.getenv("QVERSE_API_URL", "https://api.q-verse.io/agents/chat")


def ask_qverse(message: str, context=None):
    payload = {
        "message": message,
        "source": "mcp",
        "user_id": os.getenv("USER", "mcp-user"),
        "username": os.getenv("USER", "mcp-user"),
        "context": context or {},
    }
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


if __name__ == "__main__":
    message = " ".join(sys.argv[1:]) or "Hello Q-Verse from MCP"
    print(json.dumps(ask_qverse(message), indent=2, ensure_ascii=False))
''',
}


def write_file(path: str, content: str, force: bool = False):
    file_path = ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if file_path.exists() and not force:
        print(f"[SKIP] {path} (already exists, use --force)")
        return False
    file_path.write_text(content, encoding="utf-8")
    print(f"[WRITE] {path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Q-Verse Client Bootstrap V10.1+")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    print("Q-Verse Client Bootstrap V10.1+ Started")
    count = 0
    for path, content in FILES.items():
        if write_file(path, content, force=args.force):
            count += 1
    print(f"[SUMMARY] Client assets generated: {count}")
    print("[CLIENTS] CLI, Cursor, VS Code, Web, GitHub, n8n and MCP integrations ready")
    print("Q-Verse Client Bootstrap V10.1+ Complete")


if __name__ == "__main__":
    main()