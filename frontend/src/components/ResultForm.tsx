import { Box, Typography, TextField } from '@mui/material';

interface ResultFormProps {
  data: {
    [key: string]: string | null;
  };
}

const ResultForm = ({ data }: ResultFormProps) => {
  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Extracted Data
      </Typography>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        {Object.entries(data).map(([key, value]) => (
          <TextField
            key={key}
            label={key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
            value={value || ''}
            multiline={key.includes('address')}
            rows={key.includes('address') ? 3 : 1}
            InputProps={{
              readOnly: true,
            }}
            fullWidth
            variant="outlined"
            size="small"
          />
        ))}
      </Box>
    </Box>
  );
};

export default ResultForm; 