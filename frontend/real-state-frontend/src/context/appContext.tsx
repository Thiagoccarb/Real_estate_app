import { createContext, ReactNode, useEffect, useState } from 'react';
import { useMediaQuery } from '@material-ui/core';

export type AppContextType = {
  isMobileScreen: boolean;
  isOpenLoginModal: boolean,
  handleModal: (v: boolean) => void;
};

type AppProviderProps = {
  children: ReactNode;
}

const AppContext = createContext<AppContextType>(
  {
    isMobileScreen: false,
    isOpenLoginModal: false,
    handleModal: function (_: boolean): void {
      throw new Error('Function not implemented.');
    }
  });

const AppProvider = ({ children }: AppProviderProps) => {
  const [isMobileScreen, setIsMobileScreen] = useState<boolean>(false);
  const [isOpenLoginModal, setIsOpenLoginModal] = useState<boolean>(false);

  const handleModal = (v: boolean) => setIsOpenLoginModal(v);

  const matches = useMediaQuery('(max-width:768px)');

  useEffect(() => {
    setIsMobileScreen(matches);
  }, [matches]);

  const context = {
    isMobileScreen,
    isOpenLoginModal,
    handleModal,
  };

  return (
    <AppContext.Provider value={context}>
      {children}
    </AppContext.Provider>
  );
};


export { AppContext, AppProvider };
