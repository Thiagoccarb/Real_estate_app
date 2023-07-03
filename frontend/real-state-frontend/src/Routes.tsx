import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Suspense, useContext } from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ErrorBoundary } from 'react-error-boundary';

import Home from './pages/home/Home';
import DeskTopHeader from "./components/header/DesktopHeader";
import { MobileHeader } from "./components/header/MobileHeader";
import { AppContext, AppContextType } from "./context/appContext";
import AddProperty from "./pages/adminPage/components/AddProperty";
import PropertiesForRent from "./pages/rent/PropertiesForRent";
import PropertiesForSale from "./pages/sale/PropertiesForSale";
import PropertyDetails from "./pages/houseDetails/PropertyDetails";
import ProtectedRoutes from "./components/ProtectedRoutes";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      suspense: true,
      retry: false,
      onError: (error: unknown) => {
        if ((error as Error).name === 'AbortError') return;
      },
    },
  },
});

function ErrorFallback() {
  return <h1
    style={{
      marginTop: '50px',
      textAlign: "center",
      width: "100%",
      fontSize: "6vmin"
    }}
  >An error has occurred, please try again later.
  </h1>;
}

const AppRoutes = () => {
  const { isMobileScreen } = useContext<AppContextType>(AppContext);

  return (
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <ErrorBoundary FallbackComponent={ErrorFallback}>
          <Suspense fallback={<div>Loading...</div>}>
            {isMobileScreen && <MobileHeader />}
            {!isMobileScreen && <DeskTopHeader />}
            <Routes>
              <Route path="/" element={<Navigate to="/home" replace />} />
              <Route path="/home" element={<Home />} />
              <Route path="/aluguel" element={<PropertiesForRent />} />
              <Route path="/aluguel/:id" element={<PropertyDetails />} />
              <Route path="/venda/:id" element={<PropertyDetails />} />
              <Route path="/venda" element={<PropertiesForSale />} />
              <Route element={<ProtectedRoutes />} >
                <Route path="/logged/add-property" element={<AddProperty />} />
              </Route>
              <Route path="*" element={<h1 style={{ margin: 'auto', textAlign: 'center' }} >Page not found</h1>} />
            </Routes>
          </Suspense>
        </ErrorBoundary>
      </QueryClientProvider>
    </BrowserRouter>
  )
};

export default AppRoutes;
