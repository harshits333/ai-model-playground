import { create } from 'zustand'

interface ModelResponse {
  provider: string
  model: string
  content: string
  prompt_tokens: number
  completion_tokens: number
  total_tokens: number
  cost: number
  latency: number
  error: string | null
}

interface ComparisonState {
  responses: Record<string, ModelResponse>
  isLoading: boolean
  isSaving: boolean
  error: string | null
  isSaved: boolean
  submitComparison: (prompt: string) => Promise<void>
  saveComparison: (prompt: string) => Promise<void>
}

export const useComparisonStore = create<ComparisonState>((set, get) => ({
  responses: {},
  isLoading: false,
  isSaving: false,
  error: null,
  isSaved: false,
  submitComparison: async (prompt: string) => {
    try {
      set({ isLoading: true, error: null, responses: {} }) // Clear previous responses
      
      const response = await fetch('/api/comparison', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to get comparison')
      }

      if (!Array.isArray(data.responses)) {
        throw new Error('Invalid response format')
      }

      const providerToModel: Record<string, string> = {
        'openai': 'Model 1',
        'anthropic': 'Model 2',
        'xai': 'Model 3'
      }

      const formattedResponses = data.responses.reduce((acc: Record<string, ModelResponse>, response: ModelResponse) => {
        const modelKey = providerToModel[response.provider]
        if (modelKey) {
          acc[modelKey] = {
            ...response,
            content: response.content || response.error || 'No response received',
            error: response.error
          }
        }
        return acc
      }, {})

      set({ responses: formattedResponses, error: null })
    } catch (error) {
      set({ error: (error as Error).message, responses: {} })
      throw error
    } finally {
      set({ isLoading: false })
    }
  },

  saveComparison: async (prompt: string) => {
    try {
      set({ isSaving: true, error: null, isSaved: false })
      
      const response = await fetch(`/api/comparison/save?actual_prompt=${encodeURIComponent(prompt)}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(Object.values(get().responses)),
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to save comparison')
      }

      set({ isSaved: true })
    } catch (error) {
      set({ error: (error as Error).message })
      throw error
    } finally {
      set({ isLoading: false })
    }
  },
}))