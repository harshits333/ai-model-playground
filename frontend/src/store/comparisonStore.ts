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
  error: string | null
  submitComparison: (prompt: string) => Promise<void>
}

export const useComparisonStore = create<ComparisonState>((set) => ({
  responses: {},
  isLoading: false,
  error: null,
  submitComparison: async (prompt: string) => {
    try {
      set({ isLoading: true, error: null })
      
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
}))