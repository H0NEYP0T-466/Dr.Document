import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import type { ResultResponse, CommunityFile } from '../api/client';
import './ResultDisplay.css';

interface ResultDisplayProps {
  result: ResultResponse;
  onReset: () => void;
}

interface WorkspaceFile {
  filename: string;
  content: string;
  isMarkdown: boolean;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, onReset }) => {
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
    <div className="result-display">
      <div className="result-header">
        <div className="header-content">
          <h2>✨ Documentation Generated!</h2>
          <p className="repo-name">{result.repo_name}</p>
        </div>

        <div className="header-actions">
          <button onClick={handleCopy} className="action-button copy-button">
            {copied ? '✓ Copied!' : '📋 Copy'}
          </button>
          <button onClick={() => handleDownloadFile(selectedFile)} className="action-button download-button">
            📥 Download File
          </button>
          <button onClick={handleDownloadAll} className="action-button download-all-button">
            📦 Download All
          </button>
          <button onClick={onReset} className="action-button reset-button">
            🔄 New Repository
          </button>
        </div>
      </div>

      <div className="result-stats">
        <div className="stat-card">
          <div className="stat-value">{result.files_analyzed}</div>
          <div className="stat-label">Files Analyzed</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{result.headings?.length ?? '—'}</div>
          <div className="stat-label">Sections Written</div>
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
        {/* File Explorer */}
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

        {/* File Preview */}
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

export default ResultDisplay;

