import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Suspense } from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      suspense: true, 
      retry: false,
      onError: (error: unknown) => {
        if ((error as Error).name === 'AbortError') return;
        console.log(error)
        return (
          <h1>An error has occurred during handling data, plase try again</h1>
        )
      },
    },
  },
});
import Home from './pages/home/Home';

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <Suspense fallback={<div>Loading...</div>}>
          < Routes>
            <Route path="/home" element={< Home />} />
          </Routes>
        </Suspense>
      </QueryClientProvider>

    </BrowserRouter >
  )
};

export default AppRoutes;
