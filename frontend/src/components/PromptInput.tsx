import { Box, Button, Textarea, VStack } from '@chakra-ui/react'
import { useState, useEffect } from 'react'
import { useComparisonStore } from '@/store/comparisonStore'

interface PromptInputProps {
  mb?: number | string
  prompt: string
  setPrompt: (prompt: string) => void
}

function PromptInput({ mb, prompt, setPrompt }: PromptInputProps) {
  // Remove the local prompt state:
  // const [prompt, setPrompt] = useState('')
  const [showSuccess, setShowSuccess] = useState(false)
  const { responses, isLoading, isSaving, isSaved, error, submitComparison, saveComparison  } = useComparisonStore()

  useEffect(() => {
    if (isSaved) {
      setShowSuccess(true)
      const timer = setTimeout(() => setShowSuccess(false), 1000) // Hide after 3 seconds
      return () => clearTimeout(timer)
    }
  }, [isSaved])
  
  const handleSubmit = async () => {
    if (!prompt.trim()) return
    try {
      useComparisonStore.setState({ isSaved: false, isSaving: false })
      await submitComparison(prompt) // The store will handle clearing responses
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
      {Object.keys(responses).length > 0 && (
        <>
            <Button 
            onClick={() => saveComparison(prompt)}
            disabled={isSaving || isSaved}
            colorScheme="orange"
            alignSelf="flex-end"
            >
            {isSaved ? 'Saved' : 'Save Comparison'}
            </Button>
            {showSuccess && (
                <Box 
                    position="fixed" 
                    top="4" 
                    left="50%" 
                    transform="translateX(-50%)"
                    bg="green.500" 
                    color="white" 
                    px={4}
                    py={2}
                    borderRadius="md"
                    textAlign="center"
                    zIndex="toast"
                    boxShadow="md"
                    maxWidth="90%"
                >
                    Successfully Saved!
                </Box>
                )}
        </>
        )}
    </VStack>
  )
}

export default PromptInput