import { ThemeProvider } from '@material-ui/core';
import { theme } from './styles/styles';

import { AppProvider } from './context/appContext';
import AppRoutes from './Routes';
import LoginModal from './components/modals/LoginModal';

import './App.scss'

function App() {
  return (
    <ThemeProvider theme={theme}>
      <AppProvider>
        <LoginModal />
        <AppRoutes />
      </AppProvider>
    </ThemeProvider>)
}

export default App
