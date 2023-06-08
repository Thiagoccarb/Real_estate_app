import { Drawer, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import HomeIcon from '@mui/icons-material/Home';
import InfoIcon from '@mui/icons-material/Info';
import ContactMailIcon from '@mui/icons-material/ContactMail';
import PersonIcon from '@mui/icons-material/Person';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router-dom';

type IProps = {
  toggleMenu: () => void;
  isMenuOpen: boolean;
}
export function MobileSidebar({ toggleMenu, isMenuOpen }: IProps) {
  const navigate = useNavigate();
  const [, , removeCookie] = useCookies(['credentials']);

  const handleLogout = () => {
    removeCookie('credentials');
    setTimeout(() => navigate('/home'), 1500);
    toggleMenu();
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
        <ListItem onClick={toggleMenu}>
          <ListItemIcon>
            <HomeIcon />
          </ListItemIcon>
          <ListItemText primary='Aluguel' />
        </ListItem>
        <ListItem onClick={toggleMenu}>
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
        <ListItem onClick={toggleMenu}>
          <ListItemIcon>
            <LockOpenIcon />
          </ListItemIcon>
          <ListItemText primary='Login' />
        </ListItem>
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
