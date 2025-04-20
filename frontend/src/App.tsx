import { Box, Container, Grid, Flex, useColorMode } from '@chakra-ui/react'
import { QueryClient, QueryClientProvider } from 'react-query'
import { useState } from 'react'
import ComparisonPanel from './components/ComparisonPanel'
import PromptInput from './components/PromptInput'
import HistoryTab from './components/HistoryTab'

const queryClient = new QueryClient()

function App() {
  const { colorMode } = useColorMode()
  const [activeTab, setActiveTab] = useState<'compare' | 'history'>('compare')
  const [prompt, setPrompt] = useState('') // Add this state

  return (
    <QueryClientProvider client={queryClient}>
      <Box minH="100vh" bg={colorMode === 'dark' ? 'gray.900' : 'gray.50'}>
        <Flex>
          {/* Sidebar */}
          <Box w="200px" p={4} borderRight="1px solid" borderColor={colorMode === 'dark' ? 'gray.700' : 'gray.200'}>
            <Box 
              p={2} mb={2} 
              borderRadius="md" 
              bg={activeTab === 'compare' ? 'blue.500' : 'transparent'}
              color={activeTab === 'compare' ? 'white' : 'inherit'}
              cursor="pointer"
              onClick={() => setActiveTab('compare')}
            >
              Model Comparison
            </Box>
            <Box 
              p={2} 
              borderRadius="md" 
              bg={activeTab === 'history' ? 'blue.500' : 'transparent'}
              color={activeTab === 'history' ? 'white' : 'inherit'}
              cursor="pointer"
              onClick={() => setActiveTab('history')}
            >
              History
            </Box>
          </Box>

          {/* Main Content */}
          <Box flex={1} p={4}>
            {activeTab === 'compare' ? (
              <Container maxW="container.xl" py={8}>
                <PromptInput mb={8} prompt={prompt} setPrompt={setPrompt} /> {/* Pass prompt props */}
                <Grid templateColumns="repeat(3, 1fr)" gap={6}>
                  <ComparisonPanel title="Model 1" />
                  <ComparisonPanel title="Model 2" />
                  <ComparisonPanel title="Model 3" />
                </Grid>
              </Container>
            ) : (
              <HistoryTab />
            )}
          </Box>
        </Flex>
      </Box>
    </QueryClientProvider>
  )
}


export default App;
