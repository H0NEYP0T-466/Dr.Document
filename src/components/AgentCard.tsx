import React from 'react';
import { Agent } from '../types';
import './AgentCard.css';

interface AgentCardProps {
  agent: Agent;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent }) => {
  const getStatusColor = () => {
    switch (agent.status) {
      case 'working':
        return '#3b82f6';
      case 'completed':
        return '#10b981';
      case 'failed':
        return '#ef4444';
      default:
        return '#6b7280';
    }
  };

  const getStatusText = () => {
    switch (agent.status) {
      case 'working':
        return 'Working...';
      case 'completed':
        return 'Completed';
      case 'failed':
        return 'Failed';
      default:
        return 'Idle';
    }
  };

  const getStatusIcon = () => {
    switch (agent.status) {
      case 'working':
        return '⚙️';
      case 'completed':
        return '✅';
      case 'failed':
        return '❌';
      default:
        return '⏸️';
    }
  };

  return (
    <div className={`agent-card ${agent.status}`}>
      <div className="agent-header">
        <div className="agent-emoji">{agent.emoji}</div>
        <div className="agent-info">
          <h3 className="agent-name">{agent.name}</h3>
          <p className="agent-description">{agent.description}</p>
        </div>
      </div>

      <div className="agent-status">
        <div className="status-indicator" style={{ backgroundColor: getStatusColor() }}>
          <span className="status-icon">{getStatusIcon()}</span>
          <span className="status-text">{getStatusText()}</span>
        </div>
      </div>

      {agent.status === 'working' && agent.progress !== undefined && (
        <div className="agent-progress">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${agent.progress}%` }}
            />
          </div>
          <div className="progress-text">{agent.progress}%</div>
        </div>
      )}

      {agent.result && (
        <div className="agent-result">
          <div className="result-label">Result:</div>
          <div className="result-content">{agent.result}</div>
        </div>
      )}
    </div>
  );
};

export default AgentCard;
