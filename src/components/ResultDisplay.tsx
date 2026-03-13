import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import type { ResultResponse, CommunityFile, MultiModeResults, ModeResult } from '../api/client';
import { apiClient } from '../api/client';
import './ResultDisplay.css';

interface ResultDisplayProps {
  result: ResultResponse | null;
  multiModeResults: MultiModeResults | null;
  onReset: () => void;
}

interface WorkspaceFile {
  filename: string;
  content: string;
  isMarkdown: boolean;
}

const MODE_LABELS: Record<string, string> = {
  research_paper: '🔬 Research Paper',
  software_doc: '🎓 Academic Documentation',
  srs: '📋 SRS (IEEE 830)',
};

const FORMAT_LABELS: Record<string, string> = {
  pdf: '📄 PDF',
  docx: '📝 DOCX',
  tex: '🔤 LaTeX',
};

/* ── GitHub Docs Result Panel ────────────────────────────────── */
const GitHubDocsPanel: React.FC<{ result: ResultResponse }> = ({ result }) => {
  const allFiles: WorkspaceFile[] = [
    { filename: 'README.md', content: result.readme, isMarkdown: true },
    ...(result.community_files || []).map((f: CommunityFile) => ({
      filename: f.filename,
      content: f.content,
      isMarkdown: f.filename.endsWith('.md'),
    })),
  ];

  const [selectedFile, setSelectedFile] = useState<WorkspaceFile>(allFiles[0] ?? { filename: 'README.md', content: '', isMarkdown: true });
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(selectedFile.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadFile = (file: WorkspaceFile) => {
    const blob = new Blob([file.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = file.filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadAll = () => {
    allFiles.forEach(file => handleDownloadFile(file));
  };

  const getFileEmoji = (filename: string) => {
    if (filename === 'README.md') return '📖';
    if (filename === 'LICENSE') return '⚖️';
    if (filename === 'CONTRIBUTING.md') return '🤝';
    if (filename === 'CODE_OF_CONDUCT.md') return '📜';
    if (filename === 'SECURITY.md') return '🔒';
    if (filename === 'SUPPORT.md') return '💬';
    if (filename === 'CODEOWNERS') return '👥';
    return '📄';
  };

  return (
    <div className="result-mode-panel result-mode-panel--github_docs">
      <div className="result-mode-panel__header">
        <div>
          <h3 className="result-mode-panel__title">📚 GitHub Documentation</h3>
          <p className="result-mode-panel__subtitle">{result.repo_name}</p>
        </div>
        <div className="result-mode-panel__actions">
          <button onClick={handleCopy} className="action-button copy-button">
            {copied ? '✓ Copied!' : '📋 Copy'}
          </button>
          <button onClick={() => handleDownloadFile(selectedFile)} className="action-button download-button">
            📥 Download
          </button>
          <button onClick={handleDownloadAll} className="action-button download-all-button">
            📦 All Files
          </button>
        </div>
      </div>

      <div className="result-mode-panel__stats">
        <div className="stat-card">
          <div className="stat-value">{result.files_analyzed}</div>
          <div className="stat-label">Files Analyzed</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{result.headings?.length ?? '—'}</div>
          <div className="stat-label">Sections</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{result.final_review.completeness_score}/100</div>
          <div className="stat-label">Completeness</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{allFiles.length}</div>
          <div className="stat-label">Files Generated</div>
        </div>
      </div>

      <div className="workspace-container">
        <div className="file-explorer">
          <div className="file-explorer-header">
            <h3>📁 Generated Files</h3>
          </div>
          <ul className="file-list">
            {allFiles.map(file => (
              <li
                key={file.filename}
                className={`file-item ${selectedFile.filename === file.filename ? 'active' : ''}`}
                onClick={() => setSelectedFile(file)}
              >
                <span className="file-emoji">{getFileEmoji(file.filename)}</span>
                <span className="file-name">{file.filename}</span>
                <button
                  className="file-download-btn"
                  onClick={e => { e.stopPropagation(); handleDownloadFile(file); }}
                  title={`Download ${file.filename}`}
                >
                  ↓
                </button>
              </li>
            ))}
          </ul>
        </div>

        <div className="file-preview">
          <div className="preview-header">
            <h3>{getFileEmoji(selectedFile.filename)} {selectedFile.filename}</h3>
          </div>
          <div className="markdown-content">
            {selectedFile.isMarkdown ? (
              <ReactMarkdown>{selectedFile.content}</ReactMarkdown>
            ) : (
              <pre className="plain-text-content">{selectedFile.content}</pre>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

/* ── Single Generated-Doc Mode Panel ────────────────────────── */
const GeneratedModePanel: React.FC<{ modeKey: string; modeResult: ModeResult }> = ({ modeKey, modeResult }) => {
  const handleDownloadGenerated = (downloadPath: string, filename: string) => {
    const url = apiClient.getDownloadUrl(downloadPath);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className={`result-mode-panel result-mode-panel--${modeKey}`}>
      <div className="result-mode-panel__header">
        <h3 className="result-mode-panel__title">
          {MODE_LABELS[modeKey] ?? modeKey}
          {' '}
          {modeResult.status === 'completed' ? '✓' :
           modeResult.status === 'failed' ? '✗' : '⏳'}
        </h3>
      </div>

      <div className="result-mode-panel__body">
        {modeResult.status === 'failed' ? (
          <div className="mode-error">
            <p>❌ {modeResult.error || 'Generation failed for this mode.'}</p>
          </div>
        ) : modeResult.status === 'completed' && modeResult.files ? (
          <div className="mode-files">
            <p className="mode-files-label">Download generated files:</p>
            <div className="mode-file-buttons">
              {Object.entries(modeResult.files).map(([fmt, path]) => {
                const ext = path.split('.').pop() ?? fmt;
                const filename = path.split('/').pop() ?? `${modeKey}.${ext}`;
                return (
                  <button
                    key={fmt}
                    className="download-file-btn"
                    onClick={() => handleDownloadGenerated(path, filename)}
                  >
                    {FORMAT_LABELS[fmt] ?? fmt} ↓
                  </button>
                );
              })}
            </div>
          </div>
        ) : (
          <div className="mode-pending">
            <p>⏳ Still generating…</p>
          </div>
        )}
      </div>
    </div>
  );
};

/* ── Main ResultDisplay ──────────────────────────────────────── */
const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, multiModeResults, onReset }) => {
  const modeKeys = multiModeResults ? Object.keys(multiModeResults.modes) : [];
  const hasGithubDocs = !!result;
  const hasMultiMode = modeKeys.length > 0;

  // Count total panels to choose grid layout
  const totalPanels = (hasGithubDocs ? 1 : 0) + modeKeys.length;

  if (!hasGithubDocs && !hasMultiMode) return null;

  return (
    <div className="result-display">
      <div className="result-header">
        <div className="header-content">
          <h2>✨ Generation Complete!</h2>
        </div>
        <div className="header-actions">
          <button onClick={onReset} className="action-button reset-button">
            🔄 New Repository
          </button>
        </div>
      </div>

      {/* Separate result windows per mode */}
      <div className={`result-panels result-panels--${Math.min(totalPanels, 4)}`}>
        {hasGithubDocs && <GitHubDocsPanel result={result!} />}
        {hasMultiMode && modeKeys.map(modeKey => (
          <GeneratedModePanel
            key={modeKey}
            modeKey={modeKey}
            modeResult={multiModeResults!.modes[modeKey]}
          />
        ))}
      </div>
    </div>
  );
};

export default ResultDisplay;


