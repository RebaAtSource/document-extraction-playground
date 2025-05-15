import { Box, Text, VStack, FormControl, FormLabel, Input, Textarea } from '@chakra-ui/react'

interface ResultFormProps {
  data: {
    [key: string]: string | null;
  };
}

const ResultForm = ({ data }: ResultFormProps) => {
  return (
    <Box>
      <Text fontSize="xl" fontWeight="semibold" mb={4}>
        Extracted Data
      </Text>
      <VStack spacing={4} align="stretch">
        {Object.entries(data).map(([key, value]) => {
          const label = key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
          const isMultiline = key.includes('address')
          
          return (
            <FormControl key={key}>
              <FormLabel>{label}</FormLabel>
              {isMultiline ? (
                <Textarea
                  value={value || ''}
                  isReadOnly
                  size="sm"
                  rows={3}
                />
              ) : (
                <Input
                  value={value || ''}
                  isReadOnly
                  size="sm"
                />
              )}
            </FormControl>
          )
        })}
      </VStack>
    </Box>
  )
}

export default ResultForm 