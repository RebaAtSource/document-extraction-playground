import React from 'react'
import { Box, Text, VStack, FormControl, FormLabel, Input, SimpleGrid } from '@chakra-ui/react'
import { IInvoice, IAddress } from '../types/invoice'

interface ResultFormProps {
  data: Partial<IInvoice>;
}

interface AddressFieldsProps {
  data: Partial<IAddress>;
}

const AddressFields: React.FC<AddressFieldsProps> = ({ data }) => (
  <VStack spacing={3} align="stretch">
    <FormControl>
      <FormLabel>Company Name</FormLabel>
      <Input value={data.company_name || ''} size="sm" isReadOnly />
    </FormControl>
    <FormControl>
      <FormLabel>Address Line 1</FormLabel>
      <Input value={data.address_line_1 || ''} size="sm" isReadOnly />
    </FormControl>
    <FormControl>
      <FormLabel>Address Line 2</FormLabel>
      <Input value={data.address_line_2 || ''} size="sm" isReadOnly />
    </FormControl>
    <SimpleGrid columns={3} spacing={3}>
      <FormControl>
        <FormLabel>City</FormLabel>
        <Input value={data.city || ''} size="sm" isReadOnly />
      </FormControl>
      <FormControl>
        <FormLabel>State</FormLabel>
        <Input value={data.state || ''} size="sm" isReadOnly />
      </FormControl>
      <FormControl>
        <FormLabel>ZIP</FormLabel>
        <Input value={data.zip || ''} size="sm" isReadOnly />
      </FormControl>
    </SimpleGrid>
  </VStack>
);

const ResultForm: React.FC<ResultFormProps> = ({ data }) => {
  return (
    <Box>
      <Text fontSize="xl" fontWeight="semibold" mb={4}>
        Extracted Data
      </Text>
      <VStack spacing={4} align="stretch">
        {Object.entries(data).map(([key, value]) => {
          const label = key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
          const isAddress = key === 'bill_to_address' || key === 'ship_to_address';
          
          if (isAddress && value) {
            console.log(key, "is address", value);
            return (
              <FormControl key={key}>
                <FormLabel>{label}</FormLabel>
                <AddressFields data={value as Partial<IAddress>} />
              </FormControl>
            )
          }

          return (
            <FormControl key={key}>
              <FormLabel>{label}</FormLabel>
              <Input
                value={value?.toString() || ''}
                size="sm"
                isReadOnly
              />
            </FormControl>
          )
        })}
      </VStack>
    </Box>
  )
}

export default ResultForm 