import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Box, Typography, Paper } from '@mui/material'

interface FileUploadProps {
  onFileUpload: (file: File) => void
}

const FileUpload = ({ onFileUpload }: FileUploadProps) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file && file.type === 'application/pdf') {
      onFileUpload(file)
    }
  }, [onFileUpload])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false
  })

  return (
    <Paper
      {...getRootProps()}
      sx={{
        p: 3,
        border: '2px dashed',
        borderColor: isDragActive ? 'primary.main' : 'grey.300',
        bgcolor: isDragActive ? 'action.hover' : 'background.paper',
        cursor: 'pointer',
        '&:hover': {
          bgcolor: 'action.hover'
        }
      }}
    >
      <input {...getInputProps()} />
      <Box sx={{ textAlign: 'center' }}>
        <Typography variant="h6" gutterBottom>
          {isDragActive ? 'Drop the PDF here' : 'Drag & drop a PDF file here'}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          or click to select a file
        </Typography>
      </Box>
    </Paper>
  )
}

export default FileUpload 