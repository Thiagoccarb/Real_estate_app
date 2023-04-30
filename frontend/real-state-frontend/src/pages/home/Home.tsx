import { useContext } from 'react';
import { Box } from '@material-ui/core';
import { useQuery } from 'react-query';

import Hero from './components/Hero';
import { AppContext, AppContextType } from '../../context/appContext';
import DeskTopHeader from '../../components/header/DesktopHeader';
import MobileHeader from '../../components/header/MobileHeader';

function Home() {
  const { isMobileScreen } = useContext<AppContextType>(AppContext);
  const abortController = new AbortController();
  const abortSignal = abortController.signal;

  const { data } = useQuery('my-data', async () => {
    const url = "https://v2.jokeapi.dev/joke/Any";
    const request = await fetch(url, { signal: abortSignal });
    return request.json()
  });

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
