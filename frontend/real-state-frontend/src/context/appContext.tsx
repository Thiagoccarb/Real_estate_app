import { createContext, ReactNode, useEffect, useState } from 'react';
import { useMediaQuery } from '@material-ui/core';

export type AppContextType = {
  isMobileScreen: boolean;
};

type AppProviderProps = {
  children: ReactNode;
}

const AppContext = createContext<AppContextType>({ isMobileScreen: true });

const AppProvider = ({ children }: AppProviderProps) => {
  const [isMobileScreen, setIsMobileScreen] = useState<boolean>(false);
  const matches = useMediaQuery('(max-width:768px)');

  useEffect(() => {
      setIsMobileScreen(matches);
  }, [matches]);

  const context = {
    isMobileScreen,
  };

  return (
    <AppContext.Provider value={context}>
      {children}
    </AppContext.Provider>
  );
};


export { AppContext, AppProvider };
