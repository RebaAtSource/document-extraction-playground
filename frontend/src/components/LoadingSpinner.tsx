import { Box, Spinner, Text, VStack } from '@chakra-ui/react'

const LoadingSpinner = () => {
  return (
    <VStack spacing={4} p={4}>
      <Spinner
        thickness="4px"
        speed="0.65s"
        emptyColor="gray.200"
        color="blue.500"
        size="xl"
      />
      <Text fontSize="xl" fontWeight="semibold">
        Processing PDF...
      </Text>
      <Text fontSize="sm" color="gray.500">
        Extracting invoice data using AI
      </Text>
    </VStack>
  )
}

export default LoadingSpinner 