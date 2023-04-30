import { Box } from '@material-ui/core';
import { useQuery } from 'react-query';

import Hero from './components/Hero';
import { Outlet } from 'react-router-dom';

const BASE_URL = import.meta.env.VITE_BASE_URL

function Home() {
  const abortController = new AbortController();
  const abortSignal = abortController.signal;

  const { data } = useQuery('my-data', async () => {
    const url = `${BASE_URL}/properties`;
    const request = await fetch(url, { signal: abortSignal });
    return request.json()
  });


  return (
    <>
      <Outlet />
      <Box
        component="section"
        display="flex"
        flexDirection="column"
        style={{ margin: '50px 20px 0 20px' }}
      >
        <Hero />
      </Box>
    </>
  )
}

export default Home;
