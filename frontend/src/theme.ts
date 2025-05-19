import { extendTheme, type ThemeConfig } from '@chakra-ui/react'

const config: ThemeConfig = {
  initialColorMode: 'light',
  useSystemColorMode: false,
}

const theme = extendTheme({
  config,
  styles: {
    global: {
      body: {
        bg: 'gray.50',
        color: 'gray.800',
      },
    },
  },
  components: {
    Container: {
      baseStyle: {
        maxW: 'container.xl',
      },
    },
    FormLabel: {
      baseStyle: {
        fontSize: 'xs',
        fontWeight: 'medium',
        color: 'gray.500',
        margin: '0',
      },
    },
  },

})

export default theme 