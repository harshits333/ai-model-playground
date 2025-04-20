import { Box, Container, Grid, useColorMode } from '@chakra-ui/react'
import { QueryClient, QueryClientProvider } from 'react-query'
import ComparisonPanel from './components/ComparisonPanel'
import PromptInput from './components/PromptInput'

const queryClient = new QueryClient()

function App() {
  const { colorMode } = useColorMode()

  return (
    <QueryClientProvider client={queryClient}>
      <Box minH="100vh" bg={colorMode === 'dark' ? 'gray.900' : 'gray.50'}>
        <Container maxW="container.xl" py={8}>
          <PromptInput mb={8} />
          <Grid templateColumns="repeat(3, 1fr)" gap={6}>
            <ComparisonPanel title="Model 1" />
            <ComparisonPanel title="Model 2" />
            <ComparisonPanel title="Model 3" />
          </Grid>
        </Container>
      </Box>
    </QueryClientProvider>
  );
}

export default App;
