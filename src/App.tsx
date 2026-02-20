import { useState, useEffect } from 'react'
import './App.css'
import RepoInput from './components/RepoInput'
import AgentWorkspace from './components/AgentWorkspace'
import ResultDisplay from './components/ResultDisplay'
import { apiClient } from './api/client'
import type { StatusUpdate, ResultResponse } from './api/client'
import { AGENT_DEFINITIONS } from './types'
import type { Agent } from './types'

/** Shape of the agent_update field sent by the backend over WebSocket */
interface AgentUpdatePayload {
  agent_id: string;
  agent_name: string;
  agent_status: string;
  agent_progress?: number;
}

type AppState = 'input' | 'processing' | 'completed' | 'error';
/** Build the initial static agent list */
const buildInitialAgents = (): Agent[] =>
  AGENT_DEFINITIONS.map(def => ({ ...def, status: 'idle', progress: 0 }))

function App() {
  const [appState, setAppState] = useState<AppState>('input')
  const [agents, setAgents] = useState<Agent[]>(buildInitialAgents())
  const [overallProgress, setOverallProgress] = useState(0)
  const [statusMessage, setStatusMessage] = useState('')
  const [result, setResult] = useState<ResultResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [ws, setWs] = useState<WebSocket | null>(null)

  // Cleanup WebSocket on unmount
  useEffect(() => {
    return () => { if (ws) ws.close() }
  }, [ws])

  /**
   * Apply an agent_update payload from a WebSocket message.
   * - If the agent already exists → update it.
   * - If it's a new section-writer agent → insert it before the 'manager' entry.
   */
  const applyAgentUpdate = (update: AgentUpdatePayload) => {
    const { agent_id, agent_name, agent_status, agent_progress } = update
    const agentStatus = agent_status as Agent['status']

    setAgents(prev => {
      const exists = prev.some(a => a.id === agent_id)

      if (exists) {
        return prev.map(a =>
          a.id === agent_id
            ? { ...a, status: agentStatus, progress: agent_progress ?? a.progress }
            : a
        )
      }

      // New section-writer agent — insert before 'manager'
      const managerIdx = prev.findIndex(a => a.id === 'manager')
      const newAgent: Agent = {
        id: agent_id,
        name: agent_name,
        emoji: '✍️',
        description: 'Writing documentation section',
        status: agentStatus,
        progress: agent_progress ?? 0,
      }
      const next = [...prev]
      const insertAt = managerIdx >= 0 ? managerIdx : next.length
      next.splice(insertAt, 0, newAgent)
      return next
    })
  }

  const handleSubmit = async (repoUrl: string) => {
    try {
      setAppState('processing')
      setError(null)
      setStatusMessage('Starting documentation generation...')
      setOverallProgress(0)
      setAgents(buildInitialAgents())

      const response = await apiClient.processRepository(repoUrl)

      const websocket = apiClient.connectWebSocket(
        response.job_id,
        (wsUpdate: StatusUpdate & { agent_update?: AgentUpdatePayload }) => {
          setOverallProgress(wsUpdate.progress)
          setStatusMessage(wsUpdate.message)

          // Apply per-agent update if present
          if (wsUpdate.agent_update) {
            applyAgentUpdate(wsUpdate.agent_update)
          }

          if (wsUpdate.status === 'completed') {
            fetchResult(response.job_id)
          } else if (wsUpdate.status === 'failed') {
            setError(wsUpdate.message)
            setAppState('error')
          }
        },
        (err) => { console.error('WebSocket error:', err) },
        () => { console.log('WebSocket closed') }
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
      setAgents(prev => prev.map(a => ({ ...a, status: 'completed', progress: 100 })))
    } catch (err) {
      console.error('Failed to fetch result:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch result')
      setAppState('error')
    }
  }

  const handleReset = () => {
    if (ws) ws.close()
    setAppState('input')
    setResult(null)
    setError(null)
    setOverallProgress(0)
    setStatusMessage('')
    setAgents(buildInitialAgents())
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

