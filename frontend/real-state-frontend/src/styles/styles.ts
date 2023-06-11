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
  typography: {
    h2: {
      fontSize: '5vmin',
      fontWeight: 700,
      margin: '20px 0'
    },
    h3: {
      fontSize: '3.5vmin',
      fontWeight: 500,
      margin: '20px 0'
    },
    h4: {
      fontSize: '3.0vmin',
      fontWeight: 500,
      margin: '20px 0'
    },
    // h5: {
    //   fontSize: '1rem',
    //   fontWeight: 600,
    // },
    // h6: {
    //   fontSize: '0.875rem',
    //   fontWeight: 600,
    // },
    // subtitle1: {
    //   fontSize: '1.31rem',
    //   fontWeight: 700,
    // },
    // subtitle2: {
    //   fontSize: '0.875rem',
    //   fontWeight: 700,
    // },
    // body1: {
    //   fontSize: '1rem',
    //   fontWeight: 400,
    // },
    // body2: {
    //   fontSize: '0.875rem',
    //   fontWeight: 500,
    // },
    // caption: {
    //   fontSize: '0.875rem',
    //   fontWeight: 400,
    // },
    // overline: {
    //   fontSize: '0.75rem',
    //   fontWeight: 600,
    // },
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
  shadows: {
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.2)',
    transition: 'transform 0.3s, box-shadow 0.3s',
    '&:hover': {
      boxShadow: '0 8px 20px rgba(0, 0, 0, 0.3)',
      transform: 'translateY(-2px)',
    },
  },
}));