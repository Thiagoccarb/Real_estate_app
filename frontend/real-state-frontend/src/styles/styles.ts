import { createTheme, Theme } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { grey } from '@mui/material/colors';

declare module '@material-ui/core/styles/createPalette' {
  interface Palette {
    green: PaletteColor;
  }
  interface PaletteOptions {
    green?: PaletteColorOptions;
  }
}


export const theme = createTheme({
  palette: {
    primary: {
      main: grey[800],
      dark: grey[900],
      light: grey[700]
    },
    green: {
      main: '#1D4743',
    }
  },
});

export const useStyles = makeStyles((theme: Theme) => ({
  navButton: ({ color = theme.palette.primary.dark }: { color: string }) => ({
    color: `${color} !important`,
    '&:focus': {
      outline: 'none'
    },
    '&.Mui-focused': {
      outline: 'none'
    },
    '&:hover': {
      backgroundColor: 'transparent !important',
      color: `${theme.palette.primary.dark} !important`
    },
  }),
}));