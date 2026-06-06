// Q-Verse VS Code Client V10.1+
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
