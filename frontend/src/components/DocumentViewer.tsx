import { useState, useRef } from 'react'
import { Document, Page, pdfjs } from 'react-pdf'
import { Box, Button, Text, Stack } from '@chakra-ui/react'

import { AiOutlineZoomIn, AiOutlineZoomOut, AiOutlineLeft, AiOutlineRight } from 'react-icons/ai'

// Set up PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`

interface DocumentViewerProps {
  file: File
}

const DocumentViewer = ({ file }: DocumentViewerProps) => {
  const [numPages, setNumPages] = useState<number | null>(null)
  const [pageNumber, setPageNumber] = useState(1)
  const [scale, setScale] = useState(1.0)
  const containerRef = useRef<HTMLDivElement | null>(null)
  const pageRef = useRef<HTMLCanvasElement | null>(null)

  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages)
    const container = containerRef.current
    const page = pageRef.current
    if (page && container) {
      const scaleFactor = container.clientWidth / page.offsetWidth
      setScale(scaleFactor)
    }
  }

  const goToPreviousPage = () => {
    setPageNumber((prev) => Math.max(prev - 1, 1))
  }

  const goToNextPage = () => {
    setPageNumber((prev) => Math.min(prev + 1, numPages || 1))
  }

  const zoomIn = () => {
    const container = containerRef.current;
    const page = pageRef.current;
    
    if (container && page) {
      // Calculate current center position
      const centerX = container.scrollLeft + container.clientWidth / 2;
      const centerY = container.scrollTop + container.clientHeight / 2;
      
      // Calculate position ratio
      const ratioX = centerX / container.scrollWidth;
      const ratioY = centerY / container.scrollHeight;
      
      // Update scale
      setScale((prev) => prev + 0.1);
      
      // After state update, adjust scroll position in next tick
      setTimeout(() => {
        if (container) {
          // Recalculate scroll position to maintain center
          container.scrollLeft = ratioX * container.scrollWidth - container.clientWidth / 2;
          container.scrollTop = ratioY * container.scrollHeight - container.clientHeight / 2;
        }
      }, 0);
    } else {
      setScale((prev) => prev + 0.1);
    }
  }

  const zoomOut = () => {
    const container = containerRef.current;
    const page = pageRef.current;
    
    if (container && page) {
      // Calculate current center position
      const centerX = container.scrollLeft + container.clientWidth / 2;
      const centerY = container.scrollTop + container.clientHeight / 2;
      
      // Calculate position ratio
      const ratioX = centerX / container.scrollWidth;
      const ratioY = centerY / container.scrollHeight;
      
      // Update scale
      setScale((prev) => Math.max(prev - 0.1, 0.5));
      
      // After state update, adjust scroll position in next tick
      setTimeout(() => {
        if (container) {
          // Recalculate scroll position to maintain center
          container.scrollLeft = ratioX * container.scrollWidth - container.clientWidth / 2;
          container.scrollTop = ratioY * container.scrollHeight - container.clientHeight / 2;
        }
      }, 0);
    } else {
      setScale((prev) => Math.max(prev - 0.1, 0.5));
    }
  }

  return (
    <Box mt={4} width="560px" display="flex" flexDirection="column" height="100%">
      <Stack direction="row" align="center" justifyContent="space-between" mb={2}>
        <Text fontSize="xl" fontWeight="bold">
          PDF Preview
        </Text>
        {numPages && numPages > 1 && (
          <Stack direction="row" align="center" justifyContent="center">
            <Button
              onClick={goToPreviousPage}
              disabled={pageNumber <= 1}
              size="xs"
              colorScheme="blue"
            >
              <AiOutlineLeft size="1.5em" />
            </Button>
            <Text>
              Page {pageNumber} of {numPages}
            </Text>
            <Button
              onClick={goToNextPage}
              disabled={pageNumber >= numPages}
              size="xs"
              colorScheme="blue"
            >
              <AiOutlineRight size="1.5em" />
            </Button>
          </Stack>
        )}
        {numPages === 1 && (
          <Text fontSize="sm" textAlign="center">
            Single page document
          </Text>
        )}
        <Stack direction="row" align="center">
          <Button onClick={zoomOut} size="xs" colorScheme="blue">
            <AiOutlineZoomOut size="1.5em" />
          </Button>
          <Button onClick={zoomIn} size="xs" colorScheme="blue">
            <AiOutlineZoomIn size="1.5em" />
          </Button>
        </Stack>
      </Stack>
      <Box
        ref={containerRef}
        id="document-scroll-container"
        overflow="auto"
        flex="1"
        width="100%"
        position="relative"
      >
        <Stack direction="column" align="center" minW="100%" w="max-content">
          <Document
            file={file}
            onLoadSuccess={onDocumentLoadSuccess}
            loading={<Text>Loading PDF...</Text>}
            error={<Text color="red.500">Error loading PDF.</Text>}
          >
            <Page
              renderTextLayer={false}
              renderAnnotationLayer={false}
              renderMode="canvas"
              pageNumber={pageNumber}
              width={containerRef.current?.clientWidth}
              scale={scale}
              canvasRef={pageRef}
            />
          </Document>
        </Stack>
      </Box>
    </Box>
  )
}

export default DocumentViewer 