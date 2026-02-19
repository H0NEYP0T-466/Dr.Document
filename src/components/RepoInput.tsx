import React, { useState } from 'react';
import './RepoInput.css';

interface RepoInputProps {
  onSubmit: (repoUrl: string) => void;
  disabled?: boolean;
}

const RepoInput: React.FC<RepoInputProps> = ({ onSubmit, disabled = false }) => {
  const [repoUrl, setRepoUrl] = useState('');
  const [error, setError] = useState('');

  const validateGitHubUrl = (url: string): boolean => {
    const githubPattern = /^https?:\/\/(www\.)?github\.com\/[\w-]+\/[\w.-]+\/?$/;
    return githubPattern.test(url.trim());
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const trimmedUrl = repoUrl.trim();

    if (!trimmedUrl) {
      setError('Please enter a GitHub repository URL');
      return;
    }

    if (!validateGitHubUrl(trimmedUrl)) {
      setError('Please enter a valid GitHub repository URL (e.g., https://github.com/user/repo)');
      return;
    }

    onSubmit(trimmedUrl);
  };

  return (
    <div className="repo-input-container">
      <div className="repo-input-header">
        <h1>🏥 Dr. Document</h1>
        <p className="subtitle">AI-Powered GitHub Documentation Generator</p>
      </div>

      <form onSubmit={handleSubmit} className="repo-input-form">
        <div className="input-wrapper">
          <input
            type="text"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="https://github.com/username/repository"
            className={`repo-input ${error ? 'error' : ''}`}
            disabled={disabled}
            autoFocus
          />
          <button 
            type="submit" 
            className="submit-button"
            disabled={disabled || !repoUrl.trim()}
          >
            {disabled ? '⏳ Processing...' : '🚀 Generate Documentation'}
          </button>
        </div>
        {error && <div className="error-message">{error}</div>}
      </form>

      <div className="info-section">
        <div className="info-item">
          <span className="info-emoji">🤖</span>
          <span>Multi-Agent AI System</span>
        </div>
        <div className="info-item">
          <span className="info-emoji">📝</span>
          <span>Comprehensive Analysis</span>
        </div>
        <div className="info-item">
          <span className="info-emoji">✨</span>
          <span>Professional README</span>
        </div>
      </div>
    </div>
  );
};

export default RepoInput;
