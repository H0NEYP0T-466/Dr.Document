import { useState, useEffect } from 'react'
import './App.css'
import RepoInput from './components/RepoInput'
import AgentWorkspace from './components/AgentWorkspace'
import ResultDisplay from './components/ResultDisplay'
import { apiClient } from './api/client'
import type { StatusUpdate, ResultResponse } from './api/client'
import { AGENT_DEFINITIONS } from './types'
import type { Agent } from './types'

type AppState = 'input' | 'processing' | 'completed' | 'error';

function App() {
  const [appState, setAppState] = useState<AppState>('input')
  const [agents, setAgents] = useState<Agent[]>([])
  const [overallProgress, setOverallProgress] = useState(0)
  const [statusMessage, setStatusMessage] = useState('')
  const [result, setResult] = useState<ResultResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [ws, setWs] = useState<WebSocket | null>(null)

  // Initialize agents
  useEffect(() => {
    const initialAgents: Agent[] = AGENT_DEFINITIONS.map(def => ({
      ...def,
      status: 'idle',
      progress: 0,
    }))
    setAgents(initialAgents)
  }, [])

  // Cleanup WebSocket on unmount
  useEffect(() => {
    return () => {
      if (ws) {
        ws.close()
      }
    }
  }, [ws])

  const updateAgentStatus = (status: string, progress: number) => {
    // Map status to agents
    const statusToAgentMap: { [key: string]: number } = {
      'cloning': -1,
      'analyzing': 0,
      'extracting_requirements': 1,
      'manager_review': 2,
      'writing_readme': 3,
      'final_review': 4,
      'completed': 4,
    }

    const activeAgentIndex = statusToAgentMap[status]

    setAgents(prev => prev.map((agent, idx) => {
      if (idx < activeAgentIndex) {
        return { ...agent, status: 'completed', progress: 100 }
      } else if (idx === activeAgentIndex) {
        return { ...agent, status: 'working', progress: Math.min(progress, 100) }
      } else {
        return { ...agent, status: 'idle', progress: 0 }
      }
    }))
  }

  const handleSubmit = async (repoUrl: string) => {
    try {
      setAppState('processing')
      setError(null)
      setStatusMessage('Starting documentation generation...')
      setOverallProgress(0)

      // Start the job
      const response = await apiClient.processRepository(repoUrl)

      // Connect to WebSocket for real-time updates
      const websocket = apiClient.connectWebSocket(
        response.job_id,
        (update: StatusUpdate) => {
          setOverallProgress(update.progress)
          setStatusMessage(update.message)
          updateAgentStatus(update.status, update.progress)

          // If completed, fetch the result
          if (update.status === 'completed') {
            fetchResult(response.job_id)
          } else if (update.status === 'failed') {
            setError(update.message)
            setAppState('error')
          }
        },
        (error) => {
          console.error('WebSocket error:', error)
        },
        () => {
          console.log('WebSocket closed')
        }
      )

      setWs(websocket)

    } catch (err) {
      console.error('Failed to process repository:', err)
      setError(err instanceof Error ? err.message : 'Failed to process repository')
      setAppState('error')
    }
  }

  const fetchResult = async (id: string) => {
    try {
      const resultData = await apiClient.getResult(id)
      setResult(resultData)
      setAppState('completed')
      
      // Mark all agents as completed
      setAgents(prev => prev.map(agent => ({
        ...agent,
        status: 'completed',
        progress: 100,
      })))
    } catch (err) {
      console.error('Failed to fetch result:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch result')
      setAppState('error')
    }
  }

  const handleReset = () => {
    if (ws) {
      ws.close()
    }
    setAppState('input')
    setResult(null)
    setError(null)
    setOverallProgress(0)
    setStatusMessage('')
    setAgents(AGENT_DEFINITIONS.map(def => ({
      ...def,
      status: 'idle',
      progress: 0,
    })))
  }

  return (
    <div className="app">
      {appState === 'input' && (
        <RepoInput onSubmit={handleSubmit} disabled={false} />
      )}

      {appState === 'processing' && (
        <AgentWorkspace 
          agents={agents}
          overallProgress={overallProgress}
          statusMessage={statusMessage}
        />
      )}

      {appState === 'completed' && result && (
        <ResultDisplay result={result} onReset={handleReset} />
      )}

      {appState === 'error' && (
        <div className="error-container">
          <div className="error-content">
            <h2>❌ Error</h2>
            <p>{error || 'An unexpected error occurred'}</p>
            <button onClick={handleReset} className="reset-button">
              Try Again
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
