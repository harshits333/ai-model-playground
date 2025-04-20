import { Box, Card, CardBody, CardHeader, Heading, Text, VStack, Stat, StatLabel, StatNumber, StatGroup, CardFooter } from '@chakra-ui/react'
import { useComparisonStore } from '@/store/comparisonStore'
import { useEffect, useRef } from 'react'

interface ComparisonPanelProps {
  title: string
}

function ComparisonPanel({ title }: ComparisonPanelProps) {
  const { responses, isLoading } = useComparisonStore()
  const responseRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleScroll = (e: Event) => {
      const scrolledPanel = e.target as HTMLDivElement
      const panels = document.querySelectorAll('.response-panel')
      
      panels.forEach((panel) => {
        if (panel !== scrolledPanel) {
          panel.scrollTop = scrolledPanel.scrollTop
        }
      })
    }

    const currentRef = responseRef.current
    if (currentRef) {
      currentRef.addEventListener('scroll', handleScroll)
    }

    return () => {
      if (currentRef) {
        currentRef.removeEventListener('scroll', handleScroll)
      }
    }
  }, [])

  return (
    <Card h="600px" display="flex" flexDirection="column">
      <CardHeader pb={2}>
        <Heading size="md" color="white">{responses[title] ? `[${responses[title].provider}] ${responses[title].model}` : title}</Heading>
      </CardHeader>
      <CardBody
        ref={responseRef}
        className="response-panel"
        overflowY="auto"
        css={{
          '&::-webkit-scrollbar': {
            width: '4px',
          },
          '&::-webkit-scrollbar-track': {
            width: '6px',
          },
          '&::-webkit-scrollbar-thumb': {
            background: 'gray.500',
            borderRadius: '24px',
          },
        }}
      >
        {isLoading ? (
          <Text color="gray.500">Generating response...</Text>
        ) : responses[title] ? (
          <VStack align="stretch" spacing={4}>
            <Box flex="1" overflowY="auto">
              <Text whiteSpace="pre-wrap">{responses[title].content}</Text>
            </Box>
          </VStack>
        ) : (
          <Text color="gray.500">No response yet</Text>
        )}
      </CardBody>
      <CardFooter pb={2}>
      <Box bg="black.100" p={4} position="sticky" bottom={0} zIndex={1} width="100%" height="auto">
              <StatGroup flexWrap="wrap" justifyContent="space-between">
                {responses[title]?.total_tokens && (
                  <Stat size="sm" flex="1 1 30%">
                    <StatLabel color="blue.500">Tokens</StatLabel>
                    <StatNumber color="blue.500">{responses[title]?.total_tokens}</StatNumber>
                  </Stat>
                )}
                {responses[title]?.latency && (
                  <Stat size="sm" flex="1 1 30%">
                    <StatLabel color="green.500">Latency</StatLabel>
                    <StatNumber color="green.500">{responses[title]?.latency.toFixed(2)}s</StatNumber>
                  </Stat>
                )}
                {responses[title]?.cost && (
                  <Stat size="sm" flex="1 1 30%">
                    <StatLabel color="red.500">Cost</StatLabel>
                    <StatNumber color="red.500">${responses[title]?.cost.toFixed(5)}</StatNumber>
                  </Stat>
                )}
                {/* Add more stats here as needed */}
              </StatGroup>
            </Box>
      </CardFooter>
    </Card>
  )
}

export default ComparisonPanel