import { useState } from 'react'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import { Container, Box, Typography, Paper } from '@mui/material'
import axios from 'axios'
import FileUpload from './components/FileUpload'
import PdfViewer from './components/PdfViewer'
import ResultForm from './components/ResultForm'
import LoadingSpinner from './components/LoadingSpinner'
import './App.css'

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
})

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
    <ThemeProvider theme={theme}>
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Invoice Data Extraction
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2, mb: 4 }}>
          <Paper sx={{ flex: 1, p: 2 }}>
            <FileUpload onFileUpload={handleFileUpload} />
            {file && <PdfViewer file={file} />}
          </Paper>
          
          <Paper sx={{ flex: 1, p: 2 }}>
            {loading && <LoadingSpinner />}
            {error && (
              <Typography color="error" align="center">
                {error}
              </Typography>
            )}
            {extractedData && <ResultForm data={extractedData} />}
          </Paper>
        </Box>
      </Container>
    </ThemeProvider>
  )
}

export default App
