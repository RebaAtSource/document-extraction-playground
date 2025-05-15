import { useState } from 'react'
import { Document, Page, pdfjs } from 'react-pdf'
import { Box, Button, Text, Stack } from '@chakra-ui/react'
import 'react-pdf/dist/esm/Page/AnnotationLayer.css'
import 'react-pdf/dist/esm/Page/TextLayer.css'

// Set up PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`

interface PdfViewerProps {
  file: File
}

const PdfViewer = ({ file }: PdfViewerProps) => {
  const [numPages, setNumPages] = useState<number | null>(null)
  const [pageNumber, setPageNumber] = useState(1)

  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages)
  }

  const goToPreviousPage = () => {
    setPageNumber((prev) => Math.max(prev - 1, 1))
  }

  const goToNextPage = () => {
    setPageNumber((prev) => Math.min(prev + 1, numPages || 1))
  }

  return (
    <Box mt={4}>
      <Text fontSize="xl" fontWeight="bold" mb={2}>
        PDF Preview
      </Text>
      <Stack direction="column" align="center" w="100%" overflowX="auto">
        <Document
          file={file}
          onLoadSuccess={onDocumentLoadSuccess}
          loading={<Text>Loading PDF...</Text>}
          error={<Text color="red.500">Error loading PDF.</Text>}
        >
          <Page
            pageNumber={pageNumber}
            renderTextLayer={true}
            renderAnnotationLayer={true}
            scale={1.2}
          />
        </Document>
        
        {numPages && numPages > 1 && (
          <Stack direction="row" align="center" mt={4}>
            <Button
              onClick={goToPreviousPage}
              disabled={pageNumber <= 1}
              size="sm"
              colorScheme="blue"
            >
              Previous
            </Button>
            <Text>
              Page {pageNumber} of {numPages}
            </Text>
            <Button
              onClick={goToNextPage}
              disabled={pageNumber >= numPages}
              size="sm"
              colorScheme="blue"
            >
              Next
            </Button>
          </Stack>
        )}
        
        {numPages === 1 && (
          <Text fontSize="sm">
            Single page document
          </Text>
        )}
      </Stack>
    </Box>
  )
}

export default PdfViewer 