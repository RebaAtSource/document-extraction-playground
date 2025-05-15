import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Box, Text, Center } from '@chakra-ui/react'

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
    <Center
      {...getRootProps()}
      p={6}
      border="2px"
      borderStyle="dashed"
      borderColor={isDragActive ? "blue.500" : "gray.200"}
      bg={isDragActive ? "blue.50" : "white"}
      cursor="pointer"
      transition="all 0.2s"
      _hover={{ bg: "gray.50" }}
      borderRadius="md"
    >
      <input {...getInputProps()} />
      <Box textAlign="center">
        <Text fontSize="lg" fontWeight="semibold" mb={2}>
          {isDragActive ? 'Drop the PDF here' : 'Drag & drop a PDF file here'}
        </Text>
        <Text fontSize="sm" color="gray.500">
          or click to select a file
        </Text>
      </Box>
    </Center>
  )
}

export default FileUpload 