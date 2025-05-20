import React from 'react'
import { Box, Divider, Text, VStack, FormControl, FormLabel, Input, SimpleGrid, NumberInput, NumberInputField } from '@chakra-ui/react'
import { IInvoice, IAddress, IItem } from '../types/invoice'

interface ResultFormProps {
  data: Partial<IInvoice>;
  tokenCounts: {
    input_tokens: number;
    output_tokens: number;
  };
  model: string;
}

interface AddressFieldsProps {
  data: Partial<IAddress>;
}

interface ItemFieldsProps {
  data: Partial<IItem>;
}

const currencyFields = ['total', 'packaging_fee', 'freight', 'sales_tax', 'prepayments_deposit', 'balance_due', 'unit_price', 'extended_price', 'subtotal'];
const choseInputType = (key: string, value: string|number|null) => {
  if (currencyFields.includes(key)) {
    return (<NumberInput precision={2} defaultValue={value as number} size="sm" >
    <NumberInputField alignItems="right"/>
  </NumberInput>)
  }
  return (<Input
    defaultValue={value?.toString() || ''}
    size="sm"
  />);
}


const AddressFields: React.FC<AddressFieldsProps> = ({ data }) => {
  const fields = [
    { label: 'Company Name', key: 'company_name', colSpan: 3 },
    { label: 'Address Line 1', key: 'address_line_1', colSpan: 3 },
    { label: 'Address Line 2', key: 'address_line_2', colSpan: 3 },
    { label: 'City', key: 'city', colSpan: 1 },
    { label: 'State', key: 'state', colSpan: 1 },
    { label: 'ZIP', key: 'zip', colSpan: 1 },
  ];

  return (
    <SimpleGrid columns={3} spacing={3}>
      {fields.map(({ label, key, colSpan }) => (
        <FormControl key={key} gridColumn={`span ${colSpan}`}>
          <FormLabel>{label}</FormLabel>
          <Input defaultValue={data[key as keyof IAddress] || ''} size="sm" />
        </FormControl>
      ))}
    </SimpleGrid>
  );
};

const ItemFields: React.FC<ItemFieldsProps> = ({ data }) => {
  const fields = [
    { label: 'Spec Tag', key: 'spec_tag', colSpan: 5 },
    { label: 'Description', key: 'description', colSpan: 5 },
    { label: 'Quantity', key: 'quantity', colSpan: 1 },
    { label: 'Units', key: 'units', colSpan: 1 },
    { label: 'Overage', key: 'overage', colSpan: 1 },
    { label: 'Discount', key: 'discount', colSpan: 1 },
    { label: 'Unit Price', key: 'unit_price', colSpan: 1 },
    { label: 'Extended Price', key: 'extended_price', colSpan: 5 },
    { label: 'FOB', key: 'fob', colSpan: 5 },
  ];

  return (
    <SimpleGrid columns={5} spacing={3} mb={16}>
      {fields.map(({ label, key, colSpan }) => (
        <FormControl key={key} gridColumn={`span ${colSpan}`}>
          <FormLabel>{label}</FormLabel>
          {choseInputType(key, data[key as keyof IItem] ?? null)}
        </FormControl>
      ))}
    </SimpleGrid>
  );
};

const ResultForm: React.FC<ResultFormProps> = ({ data, tokenCounts, model }) => {
  return (
    <Box display="flex" flexDirection="column">
      <Text fontSize="xl" fontWeight="semibold" mb={4}>
        {model.charAt(0).toUpperCase() + model.slice(1)} Result
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
          <Text fontSize="sm" color="gray.500">{tokenCounts.input_tokens} input tokens, {tokenCounts.output_tokens} output tokens</Text>
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

            else if (key === 'invoice_items' && value) {
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

            else return (
              <FormControl key={key}>
                <FormLabel>{label}</FormLabel>
                {choseInputType(key, value as string | number | null)}
              </FormControl>
            )
          })}
        </VStack>
      </Box>
    </Box>
  )
}

export default ResultForm 