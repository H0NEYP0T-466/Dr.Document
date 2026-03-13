import { useState, useEffect, useRef } from 'react'
import './App.css'
import RepoInput from './components/RepoInput'
import AgentWorkspace from './components/AgentWorkspace'
import ResultDisplay from './components/ResultDisplay'
import { apiClient } from './api/client'
import type { StatusUpdate, ResultResponse, MultiModeResults } from './api/client'
import { AGENT_DEFINITIONS } from './types'
import type { Agent } from './types'

/** Shape of the agent_update field sent by the backend over WebSocket */
interface AgentUpdatePayload {
  agent_id: string;
  agent_name: string;
  agent_status: string;
  agent_progress?: number;
}

/** Extended WebSocket message that can carry multi-mode events */
interface WsMessage extends StatusUpdate {
  type?: string;
  agent?: string;
  section?: string;
  word_count?: number;
  decision?: string;
  restart_count?: number;
  feedback?: string;
  stage?: string;
  error?: string;
  retry?: number;
  mode?: string;
  files?: string[];
  agent_update?: AgentUpdatePayload;
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
  const [multiModeResults, setMultiModeResults] = useState<MultiModeResults | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [ws, setWs] = useState<WebSocket | null>(null)
  const [ws2, setWs2] = useState<WebSocket | null>(null)
  // Track which modes were requested
  const [requestedModes, setRequestedModes] = useState<string[]>([])
  // Per-mode status messages for separate panel display
  const [modeStatusMessages, setModeStatusMessages] = useState<Record<string, string>>({})
  // Track completion of each flow independently
  const githubDocsCompletedRef = useRef(false)
  const multiModeCompletedRef = useRef(false)
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null)

  // Cleanup WebSocket and polling on unmount
  useEffect(() => {
    return () => {
      if (ws) ws.close()
      if (ws2) ws2.close()
      if (pollRef.current) clearInterval(pollRef.current)
    }
  }, [ws, ws2])

  /**
   * Apply an agent_update payload from a WebSocket message.
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

  /**
   * Apply a multi-mode WebSocket event to the agents list.
   */
  const applyMultiModeEvent = (msg: WsMessage) => {
    if (!msg.type) return

    switch (msg.type) {
      case 'mode_started':
        setModeStatusMessages(prev => ({ ...prev, [msg.mode!]: `Starting ${msg.mode}...` }))
        setStatusMessage(`Starting ${msg.mode}...`)
        break

      case 'agent_started': {
        const agentKey = `${msg.mode}__${msg.agent}__${msg.section ?? ''}`
        const label = msg.section
          ? `[${msg.mode}] ${msg.agent}: ${msg.section}`
          : `[${msg.mode}] ${msg.agent}`
        setAgents(prev => {
          if (prev.some(a => a.id === agentKey)) return prev
          const newAgent: Agent = {
            id: agentKey,
            name: label,
            emoji: '⚙️',
            description: `Running ${msg.agent}`,
            status: 'working',
            mode: msg.mode,
            section: msg.section,
          }
          return [...prev, newAgent]
        })
        setModeStatusMessages(prev => ({ ...prev, [msg.mode!]: `Running ${label}...` }))
        setStatusMessage(`Running ${label}...`)
        break
      }

      case 'agent_completed': {
        const agentKey = `${msg.mode}__${msg.agent}__${msg.section ?? ''}`
        setAgents(prev =>
          prev.map(a =>
            a.id === agentKey ? { ...a, status: 'completed', progress: 100 } : a
          )
        )
        break
      }

      case 'manager_decision': {
        if (msg.decision === 'RESTART') {
          const statusMsg = `[${msg.mode}] Section "${msg.section}" restarting (${msg.restart_count}/3)`
          setModeStatusMessages(prev => ({ ...prev, [msg.mode!]: statusMsg }))
          setStatusMessage(statusMsg)
        }
        break
      }

      case 'formatter_compiling': {
        const statusMsg = `[${msg.mode}] Compiling ${msg.stage}...`
        setModeStatusMessages(prev => ({ ...prev, [msg.mode!]: statusMsg }))
        setStatusMessage(statusMsg)
        break
      }

      case 'mode_completed': {
        const statusMsg = `[${msg.mode}] Complete ✓`
        setModeStatusMessages(prev => ({ ...prev, [msg.mode!]: statusMsg }))
        setStatusMessage(statusMsg)
        break
      }

      case 'job_completed':
        setStatusMessage('All modes complete!')
        break

      default:
        break
    }
  }

  /**
   * Handles the legacy GitHub Docs flow (single mode).
   * Returns a websocket so it can be stored separately.
   */
  const handleGitHubDocsFlow = async (repoUrl: string, onAllDone: () => void) => {
    const response = await apiClient.processRepository(repoUrl)

    const websocket = apiClient.connectWebSocket(
      response.job_id,
      (wsUpdate: StatusUpdate & { agent_update?: AgentUpdatePayload }) => {
        const progress = (wsUpdate as WsMessage).progress ?? 0
        setOverallProgress(prev => Math.max(prev, progress))
        const msg = (wsUpdate as WsMessage).message ?? ''
        setStatusMessage(msg)
        setModeStatusMessages(prev => ({ ...prev, github_docs: msg }))

        if ((wsUpdate as WsMessage).agent_update) {
          applyAgentUpdate((wsUpdate as WsMessage).agent_update!)
        }

        if (wsUpdate.status === 'completed') {
          githubDocsCompletedRef.current = true
          fetchResult(response.job_id, onAllDone)
        } else if (wsUpdate.status === 'failed') {
          setError(wsUpdate.message)
          setAppState('error')
        }
      },
      (err) => { console.error('WebSocket error:', err) },
      () => { console.log('WebSocket closed') }
    )

    return websocket
  }

  /**
   * Handles the new multi-mode flow.
   * Returns a websocket so it can be stored separately.
   */
  const handleMultiModeFlow = async (repoUrl: string, modes: string[], onAllDone: () => void) => {
    const response = await apiClient.generate({ repo_url: repoUrl, modes })
    const jobId = response.job_id

    const websocket = apiClient.connectWebSocket(
      jobId,
      (wsUpdate) => {
        applyMultiModeEvent(wsUpdate as WsMessage)

        if ((wsUpdate as WsMessage).type === 'job_completed') {
          multiModeCompletedRef.current = true
          fetchMultiModeResults(jobId, onAllDone)
        }
      },
      (err) => { console.error('WebSocket error:', err) },
      () => { console.log('WebSocket closed') }
    )

    // Fallback: also poll results every 5 seconds
    pollRef.current = setInterval(async () => {
      try {
        const results = await apiClient.getMultiModeResults(jobId)
        setMultiModeResults(results)
        if (results.status === 'completed' && !multiModeCompletedRef.current) {
          multiModeCompletedRef.current = true
          if (pollRef.current) clearInterval(pollRef.current)
          onAllDone()
        }
      } catch (e) {
        console.error('Failed to poll results:', e)
      }
    }, 5000)

    return websocket
  }

  const handleSubmit = async (repoUrl: string, modes: string[]) => {
    try {
      setAppState('processing')
      setError(null)
      setStatusMessage('Starting documentation generation...')
      setOverallProgress(0)
      setAgents(buildInitialAgents())
      setResult(null)
      setMultiModeResults(null)
      setRequestedModes(modes)
      setModeStatusMessages({})
      githubDocsCompletedRef.current = false
      multiModeCompletedRef.current = false

      const hasGithubDocs = modes.includes('github_docs')
      const multiModes = modes.filter(m => m !== 'github_docs')
      const hasMultiModes = multiModes.length > 0

      // Determine how many flows are running so we know when ALL are done
      const flowsExpected = (hasGithubDocs ? 1 : 0) + (hasMultiModes ? 1 : 0)
      let flowsDone = 0

      const onFlowDone = () => {
        flowsDone++
        if (flowsDone >= flowsExpected) {
          setAppState('completed')
          setAgents(prev => prev.map(a => ({ ...a, status: 'completed', progress: 100 })))
        }
      }

      if (hasGithubDocs && !hasMultiModes) {
        // Only GitHub Docs
        const websocket = await handleGitHubDocsFlow(repoUrl, onFlowDone)
        setWs(websocket)
      } else if (!hasGithubDocs && hasMultiModes) {
        // Only multi-mode
        const websocket = await handleMultiModeFlow(repoUrl, multiModes, onFlowDone)
        setWs(websocket)
      } else if (hasGithubDocs && hasMultiModes) {
        // Both flows in parallel
        const [websocket1, websocket2] = await Promise.all([
          handleGitHubDocsFlow(repoUrl, onFlowDone),
          handleMultiModeFlow(repoUrl, multiModes, onFlowDone),
        ])
        setWs(websocket1)
        setWs2(websocket2)
      } else {
        // Nothing selected — shouldn't happen but handle gracefully
        setError('Please select at least one output mode')
        setAppState('error')
      }

    } catch (err) {
      console.error('Failed to process repository:', err)
      setError(err instanceof Error ? err.message : 'Failed to process repository')
      setAppState('error')
    }
  }

  const fetchResult = async (id: string, onDone?: () => void) => {
    try {
      const resultData = await apiClient.getResult(id)
      setResult(resultData)
      if (onDone) onDone()
      else {
        setAppState('completed')
        setAgents(prev => prev.map(a => ({ ...a, status: 'completed', progress: 100 })))
      }
    } catch (err) {
      console.error('Failed to fetch result:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch result')
      setAppState('error')
    }
  }

  const fetchMultiModeResults = async (jobId: string, onDone?: () => void) => {
    try {
      const results = await apiClient.getMultiModeResults(jobId)
      setMultiModeResults(results)
      if (onDone) onDone()
      else {
        setAppState('completed')
        setAgents(prev => prev.map(a => ({ ...a, status: 'completed', progress: 100 })))
      }
    } catch (err) {
      console.error('Failed to fetch multi-mode results:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch results')
      setAppState('error')
    }
  }

  const handleReset = () => {
    if (ws) ws.close()
    if (ws2) ws2.close()
    if (pollRef.current) clearInterval(pollRef.current)
    setAppState('input')
    setResult(null)
    setMultiModeResults(null)
    setError(null)
    setOverallProgress(0)
    setStatusMessage('')
    setModeStatusMessages({})
    setAgents(buildInitialAgents())
    setRequestedModes([])
    githubDocsCompletedRef.current = false
    multiModeCompletedRef.current = false
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
          modes={requestedModes}
          modeStatusMessages={modeStatusMessages}
        />
      )}

      {appState === 'completed' && (result || multiModeResults) && (
        <ResultDisplay
          result={result}
          multiModeResults={multiModeResults}
          onReset={handleReset}
        />
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

