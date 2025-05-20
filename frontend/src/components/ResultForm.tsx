import React from 'react'
import { Box, Divider, Text, VStack, FormControl, FormLabel, Input, SimpleGrid, NumberInput, NumberInputField } from '@chakra-ui/react'
import { IInvoice, IAddress, ILineItem } from '../types/interfaces'

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
  data: Partial<ILineItem>;
}

const currencyFields = ['total', 'packaging_fee', 'freight', 'sales_tax', 'prepayments_deposit', 'balance_due', 'unit_price', 'extended_price', 'subtotal'];
const dateFields = ['invoice_date', 'due_date', 'ship_date'];

const choseInputType = (key: string, value: string | number | null) => {
  if (dateFields.includes(key)) {
    return (
      <Input
        type="date"
        defaultValue={value ? new Date(value as string).toISOString().split('T')[0] : ''}
        size="sm"
      />
    );
  }
  if (currencyFields.includes(key)) {
    return (
      <NumberInput precision={2} defaultValue={value as number} size="sm">
        <NumberInputField alignItems="right" />
      </NumberInput>
    );
  }
  return (
    <Input
      defaultValue={value?.toString() || ''}
      size="sm"
    />
  );
};


const AddressFields: React.FC<AddressFieldsProps> = ({ data }) => {
  const fields = [
    { label: 'Company Name', key: 'company_name', colSpan: 3 },
    { label: 'Address Line 1', key: 'address_line_1', colSpan: 3 },
    { label: 'Address Line 2', key: 'address_line_2', colSpan: 3 },
    { label: 'City', key: 'city', colSpan: 3 },
    { label: 'State', key: 'state', colSpan: 2 },
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
    { label: 'Spec Tag', key: 'spec_tag', colSpan: 6 },
    { label: 'Description', key: 'description', colSpan: 6 },
    { label: 'Quantity', key: 'quantity', colSpan: 2 },
    { label: 'Units', key: 'units', colSpan: 2 },
    { label: 'Overage', key: 'overage', colSpan: 2 },
    { label: 'Discount', key: 'discount', colSpan: 3 },
    { label: 'Unit Price', key: 'unit_price', colSpan: 3 },
    { label: 'Extended Price', key: 'extended_price', colSpan: 6 },
    { label: 'FOB', key: 'fob', colSpan: 6 },
  ];

  return (
    <SimpleGrid columns={6} spacing={3} mb={16}>
      {fields.map(({ label, key, colSpan }) => (
        <FormControl key={key} gridColumn={`span ${colSpan}`}>
          <FormLabel>{label}</FormLabel>
          {choseInputType(key, data[key as keyof ILineItem] ?? null)}
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
                  {Array.isArray(value) && value.map((item: ILineItem, index: number) => (
                    <ItemFields key={`item-${index}`} data={item as Partial<ILineItem>} />
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