import { useState } from 'react'
import { Document, Page, pdfjs } from 'react-pdf'
import { Box, IconButton, Typography } from '@mui/material'
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

  return (
    <Box sx={{ mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        PDF Preview
      </Typography>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          maxHeight: '500px',
          overflow: 'auto'
        }}
      >
        <Document
          file={file}
          onLoadSuccess={onDocumentLoadSuccess}
          loading={<Typography>Loading PDF...</Typography>}
          error={<Typography color="error">Error loading PDF.</Typography>}
        >
          <Page
            pageNumber={pageNumber}
            renderTextLayer={true}
            renderAnnotationLayer={true}
            scale={1.2}
          />
        </Document>
        {numPages && (
          <Typography variant="body2" sx={{ mt: 1 }}>
            Page {pageNumber} of {numPages}
          </Typography>
        )}
      </Box>
    </Box>
  )
}

export default PdfViewer 