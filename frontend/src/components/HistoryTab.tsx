import { Box, Table, Thead, Tbody, Tr, Th, Td, Button, useColorMode, Modal, ModalOverlay, ModalContent, ModalHeader, ModalCloseButton, ModalBody, useDisclosure } from '@chakra-ui/react'
import { useState } from 'react'
import { useQuery } from 'react-query'
import ReactJson from 'react-json-view'

// Update the interface to include created_at
interface HistoryItem {
  user_prompt: string
  id: string // Add this line
  responses: Array<{
    provider: string
    model: string
    content: string
    prompt_tokens: number
    completion_tokens: number
    total_tokens: number
    cost: number
    latency: number
  }>
}

export default function HistoryTab() {
  const { colorMode } = useColorMode()
  const [page, setPage] = useState(1)
  const [selectedItem, setSelectedItem] = useState<HistoryItem | null>(null)
  const { isOpen, onOpen, onClose } = useDisclosure()
  const itemsPerPage = 5

  const { data, isLoading, error } = useQuery<HistoryItem[]>('history', async () => {
    const response = await fetch('/api/comparison/history')
    if (!response.ok) throw new Error('Failed to fetch history')
    const data = await response.json()
    // Sort by created_at in descending order (newest first)
    return data.sort((a, b) => b.id - a.id)
  })

  const paginatedData = data?.slice((page - 1) * itemsPerPage, page * itemsPerPage) || []

  const handleRowClick = (item: HistoryItem) => {
    setSelectedItem(item)
    onOpen()
  }

  return (
    <Box>
      <Table variant="simple" colorScheme={colorMode === 'dark' ? 'gray' : 'blackAlpha'}>
        <Thead>
          <Tr>
            <Th>Prompt</Th>
            <Th>Models</Th>
            <Th>Tokens</Th>
            <Th>Cost</Th>
            <Th>Latency</Th>
          </Tr>
        </Thead>
        <Tbody>
          {paginatedData.map((item, index) => (
            <Tr 
              key={index} 
              onClick={() => handleRowClick(item)}
              cursor="pointer"
              _hover={{ bg: colorMode === 'dark' ? 'gray.700' : 'gray.100' }}
            >
              <Td>{item.user_prompt}</Td>
              <Td>
                {item.responses.map((r, i) => (
                  <Box key={i} mb={2}>
                    <strong>{r.model}</strong>: {r.content.substring(0, 50)}...
                  </Box>
                ))}
              </Td>
              <Td>
                {item.responses.map((r, i) => (
                  <Box key={i} mb={2}>
                    {r.total_tokens} ({r.prompt_tokens}+{r.completion_tokens})
                  </Box>
                ))}
              </Td>
              <Td>
                {item.responses.map((r, i) => (
                  <Box key={i} mb={2}>
                    ${r.cost.toFixed(5)}
                  </Box>
                ))}
              </Td>
              <Td>
                {item.responses.map((r, i) => (
                  <Box key={i} mb={2}>
                    {r.latency.toFixed(2)}s
                  </Box>
                ))}
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>

      {/* JSON View Modal */}
      <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Response Details</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            {selectedItem && (
              <ReactJson
                src={selectedItem}
                theme={colorMode === 'dark' ? 'monokai' : 'rjv-default'}
                displayDataTypes={false}
                collapsed={false}
              />
            )}
          </ModalBody>
        </ModalContent>
      </Modal>

      {data && data.length > itemsPerPage && (
        <Box mt={4} display="flex" justifyContent="center">
          <Button 
            onClick={() => setPage(p => Math.max(1, p - 1))} 
            disabled={page === 1}
            mr={2}
          >
            Previous
          </Button>
          <Button 
            onClick={() => setPage(p => p + 1)} 
            disabled={page * itemsPerPage >= (data?.length || 0)}
          >
            Next
          </Button>
        </Box>
      )}
    </Box>
  )
}