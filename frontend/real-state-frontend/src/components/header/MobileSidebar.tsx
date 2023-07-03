import { useContext } from 'react';
import { Drawer, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import HomeIcon from '@mui/icons-material/Home';
import InfoIcon from '@mui/icons-material/Info';
import ContactMailIcon from '@mui/icons-material/ContactMail';
import PersonIcon from '@mui/icons-material/Person';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import AddIcon from '@mui/icons-material/Add';
import { useNavigate } from 'react-router-dom';

import { AppContext, AppContextType } from '../../context/appContext';
import { useCookie } from '../../hooks/useCookie';

type IProps = {
  toggleMenu: () => void;
  isMenuOpen: boolean;
}
export function MobileSidebar({ toggleMenu, isMenuOpen }: IProps) {
  const navigate = useNavigate();
  const [cookieValue, , removeCookie] = useCookie('credentials');
  const { handleModal } = useContext<AppContextType>(AppContext);

  const handleLogout = () => {
    removeCookie('credentials');
    setTimeout(() => navigate('/home'), 1500);
    toggleMenu();
  };

  const handleClick = (path: string) => {
    navigate(`/${path}`)
    toggleMenu()
  }

  const handlePopoverOpen = () => {
    navigate('/logged/add-property')
    toggleMenu()
  };

  return (
    <Drawer anchor='right' open={isMenuOpen} onClose={toggleMenu}>
      <List>
        <ListItem onClick={toggleMenu}>
          <ListItemIcon>
            <MenuIcon />
          </ListItemIcon>
          <ListItemText primary='Menu' />
        </ListItem>
        <ListItem onClick={() => handleClick('aluguel')}>
          <ListItemIcon>
            <HomeIcon />
          </ListItemIcon>
          <ListItemText primary='Aluguel' />
        </ListItem>
        <ListItem onClick={() => handleClick('venda')}>
          <ListItemIcon>
            <InfoIcon />
          </ListItemIcon>
          <ListItemText primary='Vendas' />
        </ListItem>
        <ListItem onClick={toggleMenu}>
          <ListItemIcon>
            <ContactMailIcon />
          </ListItemIcon>
          <ListItemText primary='Sobre' />
        </ListItem>
        <ListItem onClick={toggleMenu}>
          <ListItemIcon>
            <PersonIcon />
          </ListItemIcon>
          <ListItemText primary='Contato' />
        </ListItem>
        {
          !cookieValue && (
            <ListItem
              onClick={() => {
                handleModal(true)
              }}
            >
              <ListItemIcon>
                <LockOpenIcon />
              </ListItemIcon>
              <ListItemText primary='Login' />
            </ListItem>
          )
        }
        {
          cookieValue && (
            <>
              <ListItem
                onClick={handlePopoverOpen}
                component="button"
              >
                <ListItemIcon>
                  <AddIcon />
                </ListItemIcon>
                <ListItemText primary="Adicionar propriedade" />
              </ListItem>
            </>

          )
        }
        <ListItem onClick={handleLogout}>
          <ListItemIcon>
            <ExitToAppIcon />
          </ListItemIcon>
          <ListItemText primary="Sair" />
        </ListItem>
      </List>
    </Drawer>
  )
}
