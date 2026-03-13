import React, { useState } from 'react';
import type { Agent } from '../types';
import AgentCard from './AgentCard';
import './AgentWorkspace.css';

const MODE_LABELS: Record<string, string> = {
  github_docs: '📚 GitHub Docs',
  research_paper: '🔬 Research Paper',
  software_doc: '🎓 Software Doc',
  srs: '📋 SRS',
};

interface AgentWorkspaceProps {
  agents: Agent[];
  overallProgress: number;
  statusMessage: string;
  modes?: string[];
}

const AgentWorkspace: React.FC<AgentWorkspaceProps> = ({
  agents,
  overallProgress,
  statusMessage,
  modes = [],
}) => {
  const hasModeTabs = modes.length > 1;
  const [activeMode, setActiveMode] = useState<string | null>(
    modes.length > 0 ? modes[0] : null
  );

  // Group agents by mode (agents without a mode key go into the shared bucket)
  const sharedAgents = agents.filter(a => !a.mode);
  const modeAgents = (mode: string) => agents.filter(a => a.mode === mode);

  const displayAgents = hasModeTabs && activeMode !== null
    ? [...sharedAgents, ...modeAgents(activeMode)]
    : agents;

  return (
    <div className="agent-workspace">
      <div className="workspace-header">
        <h2>🏢 Agent Office</h2>
        <p className="workspace-subtitle">Multi-Agent AI System at Work</p>

        <div className="overall-progress">
          <div className="progress-info">
            <span className="progress-label">Overall Progress</span>
            <span className="progress-percentage">{overallProgress}%</span>
          </div>
          <div className="progress-bar-large">
            <div
              className="progress-fill-large"
              style={{ width: `${overallProgress}%` }}
            />
          </div>
          <div className="status-message">{statusMessage}</div>
        </div>

        {/* Mode tab bar — only shown when multiple modes are running */}
        {hasModeTabs && (
          <div className="mode-tab-bar">
            <button
              className={`mode-tab ${activeMode === null ? 'mode-tab--active' : ''}`}
              onClick={() => setActiveMode(null)}
            >
              All
            </button>
            {modes.map(mode => (
              <button
                key={mode}
                className={`mode-tab ${activeMode === mode ? 'mode-tab--active' : ''}`}
                onClick={() => setActiveMode(mode)}
              >
                {MODE_LABELS[mode] ?? mode}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="agents-grid">
        {displayAgents.map((agent) => (
          <AgentCard key={agent.id} agent={agent} />
        ))}
      </div>
    </div>
  );
};

export default AgentWorkspace;

