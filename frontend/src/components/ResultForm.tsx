import React from 'react'
import { Box, Divider, Text, VStack, FormControl, FormLabel, Input, SimpleGrid } from '@chakra-ui/react'
import { IInvoice, IAddress, IItem } from '../types/invoice'

interface ResultFormProps {
  data: Partial<IInvoice>;
}

interface AddressFieldsProps {
  data: Partial<IAddress>;
}

interface ItemFieldsProps {
  data: Partial<IItem>;
}

const AddressFields: React.FC<AddressFieldsProps> = ({ data }) => (
  <VStack spacing={3} align="stretch">
    <FormControl key="company_name">
      <FormLabel>Company Name</FormLabel>
      <Input defaultValue={data.company_name || ''} size="sm" />
    </FormControl>
    <FormControl key="address_line_1">
      <FormLabel>Address Line 1</FormLabel>
      <Input defaultValue={data.address_line_1 || ''} size="sm" />
    </FormControl>
    <FormControl key="address_line_2">
      <FormLabel>Address Line 2</FormLabel>
      <Input defaultValue={data.address_line_2 || ''} size="sm" />
    </FormControl>
    <SimpleGrid columns={3} spacing={3}>
      <FormControl key="city">
        <FormLabel>City</FormLabel>
        <Input defaultValue={data.city || ''} size="sm" />
      </FormControl>
      <FormControl key="state">
        <FormLabel>State</FormLabel>
        <Input defaultValue={data.state || ''} size="sm" />
      </FormControl>
      <FormControl key="zip">
        <FormLabel>ZIP</FormLabel>
        <Input defaultValue={data.zip || ''} size="sm" />
      </FormControl>
    </SimpleGrid>
  </VStack>
);

const ItemFields: React.FC<ItemFieldsProps> = ({ data }) => (
  <VStack spacing={3} align="stretch">
    {Object.entries(data).map(([key, value]) => {
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
            return (
              <FormControl key={key}>
                <FormLabel>{label}</FormLabel>
                <Input
                  defaultValue={value?.toString() || ''}
                  size="sm"
                />
              </FormControl>
            )
      })}
  </VStack>
);

const ResultForm: React.FC<ResultFormProps> = ({ data }) => {
  return (
    <Box height="calc(100vh - 240px)" display="flex" flexDirection="column">
      <Text fontSize="xl" fontWeight="semibold" mb={4}>
        Extracted Data
      </Text>
      <Box 
        flex="1"
        overflowY="auto"
        px={2}
        sx={{
          '&::-webkit-scrollbar': {
            width: '8px',
            borderRadius: '8px',
            backgroundColor: 'gray.100',
          },
          '&::-webkit-scrollbar-thumb': {
            backgroundColor: 'gray.300',
            borderRadius: '8px',
          },
        }}
      >
        <VStack spacing={4} align="stretch">
          {Object.entries(data).map(([key, value]) => {
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
            const isAddress = key === 'bill_to_address' || key === 'ship_to_address';
            
            if (isAddress && value) {
              return (
                <>
                  <FormControl key={key}>
                    <FormLabel fontSize="lg" py={4}>{label}</FormLabel>
                    <AddressFields data={value as Partial<IAddress>} />
                  </FormControl>
                  <Divider my={4}/>
                </>
              )
            }

            if (key === 'invoice_items' && value) {
              return (
                <FormControl key={key}>
                  <FormLabel fontSize="lg" py={4}>Invoice Items</FormLabel>
                  {Array.isArray(value) && value.map((item: IItem, index: number) => (
                    <ItemFields key={`item-${index}`} data={item as Partial<IItem>} />
                  ))}
                  <Divider my={4}/>
                </FormControl>
              )
            }

            return (
              <FormControl key={key}>
                <FormLabel>{label}</FormLabel>
                <Input
                  defaultValue={value?.toString() || ''}
                  size="sm"
                />
              </FormControl>
            )
          })}
        </VStack>
      </Box>
    </Box>
  )
}

export default ResultForm 