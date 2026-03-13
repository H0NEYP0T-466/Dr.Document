import React, { useState } from 'react';
import { MODE_CARDS } from '../types';
import type { Mode } from '../types';
import './RepoInput.css';

interface RepoInputProps {
  onSubmit: (repoUrl: string, modes: string[]) => void;
  disabled?: boolean;
}

const RepoInput: React.FC<RepoInputProps> = ({ onSubmit, disabled = false }) => {
  const [repoUrl, setRepoUrl] = useState('');
  const [error, setError] = useState('');

  // Track selected top-level mode cards
  const [selectedModes, setSelectedModes] = useState<Set<Mode>>(new Set(['github_docs']));
  // Track selected sub-options for "Academic Documentation" card
  const [selectedSubOptions, setSelectedSubOptions] = useState<Set<string>>(
    new Set(['software_doc'])
  );

  const validateGitHubUrl = (url: string): boolean => {
    const githubPattern = /^https?:\/\/(www\.)?github\.com\/[\w-]+\/[\w.-]+\/?$/;
    return githubPattern.test(url.trim());
  };

  const toggleMode = (mode: Mode) => {
    setSelectedModes(prev => {
      const next = new Set(prev);
      if (next.has(mode)) {
        next.delete(mode);
      } else {
        next.add(mode);
      }
      return next;
    });
  };

  const toggleSubOption = (optId: string) => {
    setSelectedSubOptions(prev => {
      const next = new Set(prev);
      if (next.has(optId)) {
        next.delete(optId);
      } else {
        next.add(optId);
      }
      return next;
    });
  };

  /** Build the array of backend mode strings to send */
  const buildModeList = (): string[] => {
    const modes: string[] = [];
    for (const card of MODE_CARDS) {
      if (!selectedModes.has(card.id)) continue;

      if (card.subOptions) {
        // For cards with sub-options, add the selected sub-option IDs
        for (const sub of card.subOptions) {
          if (selectedSubOptions.has(sub.id)) {
            modes.push(sub.id);
          }
        }
      } else {
        // For plain cards, use the card id directly
        // 'github_docs' is handled by the existing /api/process-repo flow
        if (card.id !== 'github_docs') {
          modes.push(card.id);
        }
      }
    }
    return modes;
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

    if (selectedModes.size === 0) {
      setError('Please select at least one output mode');
      return;
    }

    // For "Academic Documentation" card, at least one sub-option must be chosen
    const acadCard = MODE_CARDS.find(c => c.subOptions);
    if (acadCard && selectedModes.has(acadCard.id)) {
      const anySubSelected = acadCard.subOptions!.some(s => selectedSubOptions.has(s.id));
      if (!anySubSelected) {
        setError('Please select at least one Academic Documentation sub-option');
        return;
      }
    }

    const modes = buildModeList();
    onSubmit(trimmedUrl, modes);
  };

  const isGithubDocsSelected = selectedModes.has('github_docs');
  const hasAnyMode = selectedModes.size > 0;

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
        </div>

        {/* Mode Selector Cards */}
        <div className="mode-selector">
          <p className="mode-selector-label">Select output mode(s):</p>
          <div className="mode-cards">
            {MODE_CARDS.map(card => {
              const isSelected = selectedModes.has(card.id);
              return (
                <div
                  key={card.id}
                  className={`mode-card ${isSelected ? 'mode-card--selected' : ''} ${disabled ? 'mode-card--disabled' : ''}`}
                  onClick={() => !disabled && toggleMode(card.id)}
                >
                  <div className="mode-card__check">
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => !disabled && toggleMode(card.id)}
                      onClick={e => e.stopPropagation()}
                      disabled={disabled}
                    />
                  </div>
                  <div className="mode-card__body">
                    <span className="mode-card__emoji">{card.emoji}</span>
                    <div className="mode-card__text">
                      <span className="mode-card__title">{card.title}</span>
                      <span className="mode-card__desc">{card.description}</span>
                    </div>
                  </div>
                  {card.subOptions && isSelected && (
                    <div className="mode-card__suboptions" onClick={e => e.stopPropagation()}>
                      {card.subOptions.map(sub => (
                        <label key={sub.id} className="suboption-label">
                          <input
                            type="checkbox"
                            checked={selectedSubOptions.has(sub.id)}
                            onChange={() => !disabled && toggleSubOption(sub.id)}
                            disabled={disabled}
                          />
                          {sub.label}
                        </label>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        <div className="input-wrapper">
          <button
            type="submit"
            className="submit-button"
            disabled={disabled || !repoUrl.trim() || !hasAnyMode}
          >
            {disabled ? '⏳ Processing...' : '🚀 Generate'}
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
          {isGithubDocsSelected
            ? <span>Professional README &amp; More</span>
            : <span>PDF, DOCX &amp; LaTeX Output</span>}
        </div>
      </div>
    </div>
  );
};

export default RepoInput;

