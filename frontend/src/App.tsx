import { useState, useRef, useEffect } from 'react'
import { Container, Box, Text, Stack, Select } from '@chakra-ui/react'
import axios from 'axios'
import FileUpload from './components/FileUpload'
import DocumentViewer from './components/DocumentViewer'
import ResultForm from './components/ResultForm'
import LoadingSpinner from './components/LoadingSpinner'
import { IInvoice, ISpec, IQuote, ISubmittal } from './types/interfaces'
import { transformDocumentData, DocumentType } from './helpers/documentFieldOrders'

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:3000',
  timeout: 60000, // 60 seconds timeout
  headers: {
    'Accept': 'application/json'
  }
})

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [extractedData, setExtractedData] = useState<any>(null)
  const [tokenCounts, setTokenCounts] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [promptType, setPromptType] = useState<string>('invoice')
  const formRefs = useRef<(HTMLDivElement | null)[]>([])
  const [documentTypes, setDocumentTypes] = useState<string[]>([])

  // Function to reset the form and data
  const resetForm = () => {
    setExtractedData(null);
    setTokenCounts(null);
    setError(null);
  }

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

  useEffect(() => {
    const fetchDocumentTypes = async () => {
      try {
        const response = await api.get('/api/document-types')
        if (response.data.success) {
          setDocumentTypes(response.data.document_types)
        } else {
          console.error('Failed to fetch document types')
        }
      } catch (error) {
        console.error('Error fetching document types:', error)
      }
    }

    fetchDocumentTypes()
  }, [])

  const handlePromptTypeChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setPromptType(event.target.value)
  }

  const handleFileUpload = async (uploadedFile: File) => {
    // Reset any previous data before processing new file
    resetForm();
    
    setFile(uploadedFile)
    setLoading(true)

    const formData = new FormData()
    formData.append('file', uploadedFile)
    formData.append('type', promptType)

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

      if (response.data.success) {
        const parsedData = response.data.data;
        console.log('Parsed data:', parsedData);

        // Transform parsedData using the selected document type
        const orderedData = transformDocumentData(parsedData, promptType as DocumentType);

        console.log('Ordered data:', orderedData);
        setExtractedData(orderedData);
        setTokenCounts(response.data.tokens);
      } else {
        throw new Error(response.data.error || 'Failed to extract data');
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
    <Container maxW="100%" px={8} py={8}>
      {/* ------------------ PAGE TITLE AND EXTRACTOR ------------------ */}
      <Box display="flex" alignItems="center" justifyContent="center" mb={6}>
        <Box display="flex" alignItems="center">
          <Select
            value={promptType}
            onChange={handlePromptTypeChange}
            variant="outline"
            fontSize="2xl"
            fontWeight="bold"
            textAlign="center"
            borderColor="gray.300"
            _hover={{ borderColor: 'gray.500' }}
            _focus={{ borderColor: 'blue.500', boxShadow: 'outline' }}
            width="auto"
            mr={2}
          >
            {documentTypes.map((key) => (
              <option key={key} value={key}>{key.charAt(0).toUpperCase() + key.slice(1)}</option>
            ))}
          </Select>
          <Text fontSize="2xl" fontWeight="bold" mr={4}>
            Data Extraction
          </Text>
        </Box>
        <FileUpload onFileUpload={handleFileUpload} />
      </Box>
      
      <Stack direction={{ base: 'column', md: 'row' }} spacing={4} h="calc(100vh - 240px)" m={4} overflow="hidden">
        {/* ------------------ PDF VIEWER ------------------ */}
        <Box p={4} borderWidth="1px" borderRadius="lg" display="flex" flexDirection="column">
          {file && <DocumentViewer file={file} />}
        </Box>
        {/* ------------------ EXTRACTED DATA ------------------ */}
        <Box flex={2} backgroundColor="white" shadow="md" p={4} borderRadius="lg" display="flex" flexDirection="column" overflow="hidden">
          {loading && <LoadingSpinner />}
          {error && (
            <Text color="red.500" textAlign="center">
              {error}
            </Text>
          )}
          {extractedData && (
            <Box overflowY="auto" flex="1">
              <Stack direction={{ base: 'column', md: 'row' }} spacing={4}>
                {Object.entries(extractedData).map(([key, data]) => (
                  <Box key={key} mb={4} flex={1}>
                    <ResultForm data={data as Partial<IInvoice>} tokenCounts={tokenCounts} model={key} />
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
