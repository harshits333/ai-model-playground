import { Box, Button, Textarea, VStack } from '@chakra-ui/react'
import { useState } from 'react'
import { useComparisonStore } from '@/store/comparisonStore'

interface PromptInputProps {
  mb?: number | string
}

function PromptInput({ mb }: PromptInputProps) {
  const [prompt, setPrompt] = useState('')
  const { submitComparison, isLoading } = useComparisonStore()

  const handleSubmit = async () => {
    if (!prompt.trim()) return
    try {
      await submitComparison(prompt)
    } catch (error) {
      console.error('Failed to submit comparison:', error)
    }
  }

  return (
    <VStack spacing={4} align="stretch" mb={mb}>
      <Box position="relative">
        <Textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your prompt here..."
          size="lg"
          minH="150px"
          resize="vertical"
          disabled={isLoading}
        />
      </Box>
      <Button
        colorScheme="blue"
        isLoading={isLoading}
        onClick={handleSubmit}
        alignSelf="flex-end"
      >
        Compare Models
      </Button>
    </VStack>
  )
}

export default PromptInput