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
  result: ResultShape | null;
  error: string | null;
}

/** Minimal shape for workflow result (matches ResultResponse from api/client) */
export interface ResultShape {
  [key: string]: unknown;
}

/** Static agents that are always shown in the UI */
export const AGENT_DEFINITIONS: Omit<Agent, 'status' | 'progress' | 'result'>[] = [
  {
    id: 'codebase_summarizer',
    name: 'Codebase Summarizer',
    emoji: '👁️',
    description: 'Reading every file and building a concise codebase summary',
  },
  {
    id: 'headings_selector',
    name: 'Headings Selector',
    emoji: '📋',
    description: 'Deciding which documentation sections to include',
  },
  {
    id: 'manager',
    name: 'Manager',
    emoji: '👔',
    description: 'Reviewing each section and requesting improvements if needed',
  },
  {
    id: 'final_reviewer',
    name: 'Final Reviewer',
    emoji: '🔍',
    description: 'Validating the complete README and approving the final output',
  },
  {
    id: 'community_license',
    name: 'LICENSE',
    emoji: '📄',
    description: 'Generating MIT License file',
  },
  {
    id: 'community_contributing_md',
    name: 'CONTRIBUTING.md',
    emoji: '📄',
    description: 'Generating contribution guidelines',
  },
  {
    id: 'community_code_of_conduct_md',
    name: 'CODE_OF_CONDUCT.md',
    emoji: '📄',
    description: 'Generating code of conduct',
  },
  {
    id: 'community_security_md',
    name: 'SECURITY.md',
    emoji: '📄',
    description: 'Generating security policy',
  },
  {
    id: 'community_support_md',
    name: 'SUPPORT.md',
    emoji: '📄',
    description: 'Generating support guide',
  },
  {
    id: 'community_codeowners',
    name: 'CODEOWNERS',
    emoji: '📄',
    description: 'Generating code ownership file',
  },
  {
    id: 'community_final_reviewer',
    name: 'Community Final Reviewer',
    emoji: '🔍',
    description: 'Validating all community health files',
  },
];

