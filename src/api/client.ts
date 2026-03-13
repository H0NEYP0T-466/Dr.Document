/**
 * API client for Dr. Document backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8004';

export interface ProcessRepoRequest {
  repo_url: string;
}

export interface ProcessRepoResponse {
  job_id: string;
  status: string;
  message: string;
}

export interface StatusResponse {
  job_id: string;
  status: string;
  progress: number;
  message: string;
}

export interface CommunityFile {
  filename: string;
  content: string;
}

export interface ResultResponse {
  job_id: string;
  repo_name: string;
  repo_url: string;
  readme: string;
  community_files: CommunityFile[];
  files_analyzed: number;
  headings: string[];
  final_review: {
    approved: boolean;
    completeness_score: number;
    accuracy_score: number;
  };
  storage_path: string;
  timestamp: string;
}

export interface StatusUpdate {
  job_id: string;
  status: string;
  progress: number;
  message: string;
  timestamp: string;
}

// Multi-mode API types

export interface GenerateRequest {
  repo_url: string;
  modes: string[];
  options?: Record<string, unknown>;
}

export interface GenerateResponse {
  job_id: string;
  modes_started: string[];
}

export interface ModeResult {
  status: 'pending' | 'processing' | 'completed' | 'failed';
  files?: Record<string, string>;
  error?: string;
}

export interface MultiModeResults {
  job_id: string;
  status: string;
  modes: Record<string, ModeResult>;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Process a GitHub repository
   */
  async processRepository(repoUrl: string): Promise<ProcessRepoResponse> {
    const response = await fetch(`${this.baseUrl}/api/process-repo`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ repo_url: repoUrl }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to process repository');
    }

    return response.json();
  }

  /**
   * Get job status
   */
  async getStatus(jobId: string): Promise<StatusResponse> {
    const response = await fetch(`${this.baseUrl}/api/status/${jobId}`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get status');
    }

    return response.json();
  }

  /**
   * Get job result
   */
  async getResult(jobId: string): Promise<ResultResponse> {
    const response = await fetch(`${this.baseUrl}/api/result/${jobId}`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get result');
    }

    return response.json();
  }

  /**
   * Start a multi-mode documentation generation job.
   */
  async generate(request: GenerateRequest): Promise<GenerateResponse> {
    const response = await fetch(`${this.baseUrl}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to start generation');
    }

    return response.json();
  }

  /**
   * Poll results for a multi-mode job.
   */
  async getMultiModeResults(jobId: string): Promise<MultiModeResults> {
    const response = await fetch(`${this.baseUrl}/api/results/${jobId}`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get results');
    }

    return response.json();
  }

  /**
   * Build a download URL for a generated file.
   * The backend returns paths like /download/{job_id}/{filename}.
   */
  getDownloadUrl(path: string): string {
    // path is already like /download/{job_id}/{filename}
    return `${this.baseUrl}${path}`;
  }

  /**
   * Connect to WebSocket for real-time updates
   */
  connectWebSocket(
    jobId: string,
    onMessage: (data: StatusUpdate) => void,
    onError?: (error: Event) => void,
    onClose?: () => void
  ): WebSocket {
    const wsUrl = this.baseUrl.replace('http', 'ws');
    const ws = new WebSocket(`${wsUrl}/ws/${jobId}`);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      if (onError) onError(error);
    };

    ws.onclose = () => {
      console.log('WebSocket closed');
      if (onClose) onClose();
    };

    // Send ping every 30 seconds to keep connection alive
    const pingInterval = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send('ping');
      } else {
        clearInterval(pingInterval);
      }
    }, 30000);

    return ws;
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseUrl}/health`);
    return response.json();
  }
}

export const apiClient = new ApiClient();

