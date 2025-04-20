import { extendTheme, type ThemeConfig } from '@chakra-ui/react'

const config: ThemeConfig = {
  initialColorMode: 'dark',
  useSystemColorMode: true,
}

const theme = extendTheme({
  config,
  styles: {
    global: (props: any) => ({
      body: {
        bg: props.colorMode === 'dark' ? 'gray.900' : 'gray.50',
      },
    }),
  },
  components: {
    Textarea: {
      defaultProps: {
        focusBorderColor: 'blue.400',
      },
    },
    Card: {
      baseStyle: {
        container: {
          borderRadius: 'lg',
        },
      },
    },
  },
})

export default theme