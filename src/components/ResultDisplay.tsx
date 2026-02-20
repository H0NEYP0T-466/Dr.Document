import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import type { ResultResponse } from '../api/client';
import './ResultDisplay.css';

interface ResultDisplayProps {
  result: ResultResponse;
  onReset: () => void;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, onReset }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(result.readme);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([result.readme], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'README.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
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
          <button onClick={handleDownload} className="action-button download-button">
            📥 Download
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
          <div className="stat-value">{result.final_review.accuracy_score}/100</div>
          <div className="stat-label">Accuracy</div>
        </div>
      </div>

      <div className="readme-preview">
        <div className="preview-header">
          <h3>📄 README.md Preview</h3>
        </div>
        <div className="markdown-content">
          <ReactMarkdown>{result.readme}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
};

export default ResultDisplay;
