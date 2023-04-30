import { useContext } from 'react';
import { Box } from '@material-ui/core';
import { useQuery } from 'react-query';

import Hero from './components/Hero';
import { AppContext, AppContextType } from '../../context/appContext';
import DeskTopHeader from '../../components/header/DesktopHeader';
import MobileHeader from '../../components/header/MobileHeader';

const BASE_URL = import.meta.env.VITE_BASE_URL

function Home() {
  const abortController = new AbortController();
  const abortSignal = abortController.signal;

  const { data } = useQuery('my-data', async () => {
    const url = `${BASE_URL}/properties`;
    const request = await fetch(url, { signal: abortSignal });
    return request.json()
  });

  const { isMobileScreen } = useContext<AppContextType>(AppContext);
  console.log(data)

  return (
    <>
      {isMobileScreen && <MobileHeader />}
      {!isMobileScreen && <DeskTopHeader />}
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
