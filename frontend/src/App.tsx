import { useState, useRef, useEffect } from 'react'
import { Container, Box, Text, Stack} from '@chakra-ui/react'
import axios from 'axios'
import FileUpload from './components/FileUpload'
import PdfViewer from './components/PdfViewer'
import ResultForm from './components/ResultForm'
import LoadingSpinner from './components/LoadingSpinner'

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:3000',
  timeout: 60000, // 60 seconds timeout
  headers: {
    'Accept': 'application/json'
  }
})

interface IInvoice {
  vendor_name?: string;
  invoice_date?: Date | null;
  due_date?: Date | null;
  // Add other fields as necessary
}

// Function to convert string dates to Date objects
const convertToDate = (data: any): Partial<IInvoice> => {
  return {
    ...data,
    invoice_date: data.invoice_date ? new Date(data.invoice_date) : null,
    due_date: data.due_date ? new Date(data.due_date) : null,
  };
};

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [extractedData, setExtractedData] = useState<any>(null)
  const [tokenCounts, setTokenCounts] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const formRefs = useRef<(HTMLDivElement | null)[]>([])

  useEffect(() => {
    const handleScroll = (event: Event) => {
      const target = event.target as HTMLDivElement
      const scrollTop = target.scrollTop
      formRefs.current.forEach((form) => {
        if (form && form !== target) {
          form.scrollTop = scrollTop
        }
      })
    }

    const firstForm = formRefs.current[0]
    if (firstForm) {
      firstForm.addEventListener('scroll', handleScroll)
    }

    return () => {
      if (firstForm) {
        firstForm.removeEventListener('scroll', handleScroll)
      }
    }
  }, [])

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
        const parsedData = response.data.data
        console.log('Parsed data:', parsedData)
        setExtractedData(parsedData)
        setTokenCounts(response.data.tokens)
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
    <Container maxW="100%" py={16}>
      <Text fontSize="2xl" fontWeight="bold" textAlign="center" mb={6}>
        Document Data Extraction
      </Text>
      
      <Stack direction={{ base: 'column', md: 'row' }} spacing={4}>
        <Box flex={1} p={4} borderWidth="1px" borderRadius="lg">
          <FileUpload onFileUpload={handleFileUpload} />
          {file && <PdfViewer file={file} />}
        </Box>
        
        <Box flex={2} backgroundColor="white" shadow="md" p={4} borderRadius="lg">
          {loading && <LoadingSpinner />}
          {error && (
            <Text color="red.500" textAlign="center">
              {error}
            </Text>
          )}
          {extractedData && (
            <Box overflowY="auto" height="calc(100vh - 240px)">
              <Stack direction={{ base: 'column', md: 'row' }} spacing={4}>
                {Object.entries(extractedData).map(([key, data]) => (
                  <Box key={key} mb={4} flex={1} >
                    <ResultForm data={convertToDate(data)} tokenCounts={tokenCounts} model={key}/>
                  </Box>
                ))}
              </Stack>
            </Box>
          )}
        </Box>
      </Stack>
    </Container>
  )
}

export default App
