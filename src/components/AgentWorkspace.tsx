import React from 'react';
import type { Agent } from '../types';
import AgentCard from './AgentCard';
import './AgentWorkspace.css';

const MODE_LABELS: Record<string, string> = {
  github_docs: '📚 GitHub Documentation',
  research_paper: '🔬 Research Paper',
  software_doc: '🎓 Academic Documentation',
  srs: '📋 SRS (IEEE 830)',
};

interface AgentWorkspaceProps {
  agents: Agent[];
  overallProgress: number;
  statusMessage: string;
  modes?: string[];
  modeStatusMessages?: Record<string, string>;
}

interface ModePanelProps {
  modeId: string;
  modeLabel: string;
  agents: Agent[];
  statusMessage: string;
}

const ModePanel: React.FC<ModePanelProps> = ({ modeId, modeLabel, agents, statusMessage }) => {
  const workingCount = agents.filter(a => a.status === 'working').length;
  const completedCount = agents.filter(a => a.status === 'completed').length;
  const totalCount = agents.length;
  const panelProgress = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

  return (
    <div className={`mode-panel mode-panel--${modeId}`}>
      <div className="mode-panel__header">
        <h3 className="mode-panel__title">{modeLabel}</h3>
        <div className="mode-panel__meta">
          <span className="mode-panel__progress-pct">{panelProgress}%</span>
          {workingCount > 0 && (
            <span className="mode-panel__working-badge">{workingCount} active</span>
          )}
        </div>
      </div>
      <div className="mode-panel__progress-bar">
        <div
          className="mode-panel__progress-fill"
          style={{ width: `${panelProgress}%` }}
        />
      </div>
      {statusMessage && (
        <div className="mode-panel__status">{statusMessage}</div>
      )}
      <div className="mode-panel__agents">
        {agents.length === 0 ? (
          <div className="mode-panel__empty">⏳ Waiting for agents to start…</div>
        ) : (
          agents.map(agent => (
            <AgentCard key={agent.id} agent={agent} />
          ))
        )}
      </div>
    </div>
  );
};

const AgentWorkspace: React.FC<AgentWorkspaceProps> = ({
  agents,
  overallProgress,
  statusMessage,
  modes = [],
  modeStatusMessages = {},
}) => {
  // For github_docs, use agents that have no mode tag (the shared legacy agents)
  const githubDocsAgents = agents.filter(a => !a.mode);
  const modeAgents = (mode: string) => agents.filter(a => a.mode === mode);

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
      </div>

      {/* Separate panel per selected mode */}
      {modes.length > 0 ? (
        <div className={`mode-panels mode-panels--${Math.min(modes.length, 4)}`}>
          {modes.map(mode => {
            const panelAgents = mode === 'github_docs' ? githubDocsAgents : modeAgents(mode);
            return (
              <ModePanel
                key={mode}
                modeId={mode}
                modeLabel={MODE_LABELS[mode] ?? mode}
                agents={panelAgents}
                statusMessage={modeStatusMessages[mode] ?? ''}
              />
            );
          })}
        </div>
      ) : (
        /* Fallback: flat grid when no modes are tracked */
        <div className="agents-grid">
          {agents.map((agent) => (
            <AgentCard key={agent.id} agent={agent} />
          ))}
        </div>
      )}
    </div>
  );
};

export default AgentWorkspace;

