import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Suspense } from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ErrorBoundary } from 'react-error-boundary';

import Home from './pages/home/Home';

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
  >An error has occurred during fetching data, please try again.
  </h1>;
}

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <ErrorBoundary FallbackComponent={ErrorFallback}>
          <Suspense fallback={<div>Loading...</div>}>
            <Routes>
              <Route path="/home" element={<Home />} />
            </Routes>
          </Suspense>
        </ErrorBoundary>
      </QueryClientProvider>
    </BrowserRouter>
  )
};

export default AppRoutes;
