import { useState } from 'react'
import { Container, Divider, Box, Text, Stack, FormControl, Input, FormLabel } from '@chakra-ui/react'
import axios from 'axios'
import FileUpload from './components/FileUpload'
import PdfViewer from './components/PdfViewer'
import ResultForm from './components/ResultForm'
import LoadingSpinner from './components/LoadingSpinner'

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:3000',
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Accept': 'application/json'
  }
})

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [extractedData, setExtractedData] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileUpload = async (uploadedFile: File) => {
    setFile(uploadedFile)
    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', uploadedFile)

    try {
      console.log('Sending request to backend...')
      console.log('File being sent:', uploadedFile.name, uploadedFile.type, uploadedFile.size)
      
      const response = await api.post('/api/process-pdf', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / (progressEvent.total ?? progressEvent.loaded))
          console.log(`Upload Progress: ${percentCompleted}%`)
        }
      })
      
      console.log('Response received:', response)

      if (response.data.success) {
        const parsedData = JSON.parse(response.data.data)
        console.log('Parsed data:', parsedData)
        setExtractedData(parsedData)
      } else {
        throw new Error(response.data.error || 'Failed to extract data')
      }
    } catch (err) {
      console.error('Error details:', err)
      if (axios.isAxiosError(err)) {
        const errorMessage = err.response?.data?.error || err.message || 'Failed to process PDF'
        console.error('Axios error:', {
          message: err.message,
          response: err.response?.data,
          status: err.response?.status,
          headers: err.response?.headers
        })
        setError(errorMessage)
      } else {
        setError(err instanceof Error ? err.message : 'An unexpected error occurred')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container maxW="container.xl" py={8}>
      <Text fontSize="2xl" fontWeight="bold" textAlign="center" mb={6}>
        Document Data Extraction
      </Text>
      
      <Stack direction={{ base: 'column', md: 'row' }} spacing={4}>
        <Box flex={1} p={4} borderWidth="1px" borderRadius="lg">
          <FileUpload onFileUpload={handleFileUpload} />
          {file && <PdfViewer file={file} />}
        </Box>
        
        <Box flex={1} backgroundColor="white" shadow="md" p={4} borderRadius="lg">
          {loading && <LoadingSpinner />}
          {error && (
            <Text color="red.500" textAlign="center">
              {error}
            </Text>
          )}
          {extractedData && <ResultForm data={extractedData} />}
        </Box>
      </Stack>
    </Container>
  )
}

export default App
