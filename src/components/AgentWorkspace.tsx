import React from 'react';
import { Agent } from '../types';
import AgentCard from './AgentCard';
import './AgentWorkspace.css';

interface AgentWorkspaceProps {
  agents: Agent[];
  overallProgress: number;
  statusMessage: string;
}

const AgentWorkspace: React.FC<AgentWorkspaceProps> = ({
  agents,
  overallProgress,
  statusMessage,
}) => {
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

      <div className="agents-grid">
        {agents.map((agent) => (
          <AgentCard key={agent.id} agent={agent} />
        ))}
      </div>
    </div>
  );
};

export default AgentWorkspace;
