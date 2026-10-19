const vscode = require('vscode');
const http = require('http');

let aiHeatmapDecoration = null;
let securityDecoration = null;
let heatmapActive = true;

function activate(context) {
  // Create text decorations for line heatmap and security flags
  aiHeatmapDecoration = vscode.window.createTextEditorDecorationType({
    backgroundColor: 'rgba(168, 85, 247, 0.18)',
    isWholeLine: true,
    overviewRulerColor: 'rgba(168, 85, 247, 0.7)',
    overviewRulerLane: vscode.OverviewRulerLane.Right
  });

  securityDecoration = vscode.window.createTextEditorDecorationType({
    backgroundColor: 'rgba(239, 68, 68, 0.25)',
    isWholeLine: true,
    overviewRulerColor: 'rgba(239, 68, 68, 0.9)',
    overviewRulerLane: vscode.OverviewRulerLane.Right
  });

  // Diagnostic collection for VS Code Problems tab
  const diagnosticCollection = vscode.languages.createDiagnosticCollection('coderescue');
  context.subscriptions.push(diagnosticCollection);

  async function runAudit(editor) {
    if (!editor || editor.document.languageId !== 'python') return;

    const code = editor.document.getText();
    const config = vscode.workspace.getConfiguration('coderescue');
    const serverUrl = config.get('serverUrl') || 'http://localhost:5000';
    const threshold = config.get('aiThreshold') || 70;

    try {
      const data = await queryCodeRescue(serverUrl, code);
      if (!data || !data.aiAttribution) return;

      const aiDecorations = [];
      const secDecorations = [];
      const diagnostics = [];

      // 1. Process line heatmap
      if (heatmapActive && data.aiAttribution.lineHeatmap) {
        for (const item of data.aiAttribution.lineHeatmap) {
          if (item.probability >= threshold) {
            const line = Math.max(0, item.line - 1);
            const range = new vscode.Range(line, 0, line, 1000);
            aiDecorations.push({
              range,
              hoverMessage: `🤖 **CodeRescue AI Attribution**: ${item.probability}% AI probability\n\n*Factors*: ${item.factors.join(', ')}`
            });
          }
        }
      }

      // 2. Process security vulnerabilities & hallucinations
      if (data.aiAttribution.vulnerabilities) {
        for (const v of data.aiAttribution.vulnerabilities) {
          const line = Math.max(0, v.line - 1);
          const range = new vscode.Range(line, 0, line, 1000);
          secDecorations.push({
            range,
            hoverMessage: `🚨 **${v.title}** [${v.severity}]: ${v.message}\n\n*Fix*: \`${v.fix}\``
          });

          diagnostics.push(new vscode.Diagnostic(
            range,
            `[CodeRescue ${v.code}] ${v.title}: ${v.message}`,
            v.severity === 'CRITICAL' ? vscode.DiagnosticSeverity.Error : vscode.DiagnosticSeverity.Warning
          ));
        }
      }

      editor.setDecorations(aiHeatmapDecoration, aiDecorations);
      editor.setDecorations(securityDecoration, secDecorations);
      diagnosticCollection.set(editor.document.uri, diagnostics);

      vscode.window.setStatusBarMessage(
        `$(shield) CodeRescue AI: ${data.aiAttribution.overallProbability}% AI Boilerplate | ${data.aiAttribution.vulnerabilities.length} Security Risks`,
        5000
      );
    } catch (err) {
      vscode.window.showWarningMessage(`CodeRescue AI backend error: ${err.message}. Make sure server is running on localhost:5000.`);
    }
  }

  // Register commands
  context.subscriptions.push(
    vscode.commands.registerCommand('coderescue.auditFile', () => {
      runAudit(vscode.window.activeTextEditor);
    }),
    vscode.commands.registerCommand('coderescue.toggleHeatmap', () => {
      heatmapActive = !heatmapActive;
      vscode.window.showInformationMessage(`CodeRescue Heatmap ${heatmapActive ? 'Enabled' : 'Disabled'}`);
      runAudit(vscode.window.activeTextEditor);
    })
  );

  // Auto-run on save
  vscode.workspace.onDidSaveTextDocument(doc => {
    if (doc.languageId === 'python' && vscode.window.activeTextEditor) {
      runAudit(vscode.window.activeTextEditor);
    }
  });

  // Initial run
  if (vscode.window.activeTextEditor) {
    runAudit(vscode.window.activeTextEditor);
  }
}

function queryCodeRescue(serverUrl, code) {
  return new Promise((resolve, reject) => {
    const url = new URL('/api/debug', serverUrl);
    const body = JSON.stringify({ code, execute: false });

    const req = http.request(
      url,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body)
        },
        timeout: 4000
      },
      res => {
        let data = '';
        res.on('data', chunk => { data += chunk; });
        res.on('end', () => {
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            reject(e);
          }
        });
      }
    );

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

function deactivate() {
  if (aiHeatmapDecoration) aiHeatmapDecoration.dispose();
  if (securityDecoration) securityDecoration.dispose();
}

module.exports = { activate, deactivate };
