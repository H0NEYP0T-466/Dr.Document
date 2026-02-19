/**
 * Type definitions for Dr. Document
 */

export interface Agent {
  id: string;
  name: string;
  status: 'idle' | 'working' | 'completed' | 'failed';
  emoji: string;
  description: string;
  progress?: number;
  result?: string;
}

export interface WorkflowState {
  jobId: string | null;
  status: string;
  progress: number;
  message: string;
  agents: Agent[];
  result: any | null;
  error: string | null;
}

export const AGENT_DEFINITIONS: Omit<Agent, 'status' | 'progress' | 'result'>[] = [
  {
    id: 'code_reader',
    name: 'Code Reader',
    emoji: '👀',
    description: 'Analyzing code structure and dependencies',
  },
  {
    id: 'requirements_extractor',
    name: 'Requirements Extractor',
    emoji: '📋',
    description: 'Extracting functional requirements',
  },
  {
    id: 'manager',
    name: 'Manager',
    emoji: '👔',
    description: 'Reviewing quality and providing feedback',
  },
  {
    id: 'readme_writer',
    name: 'README Writer',
    emoji: '✍️',
    description: 'Generating comprehensive documentation',
  },
  {
    id: 'final_reviewer',
    name: 'Final Reviewer',
    emoji: '🔍',
    description: 'Validating completeness and accuracy',
  },
];
