import { Drawer, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import HomeIcon from '@mui/icons-material/Home';
import InfoIcon from '@mui/icons-material/Info';
import ContactMailIcon from '@mui/icons-material/ContactMail';
import PersonIcon from '@mui/icons-material/Person';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';

type IProps = {
  toggleMenu: () => void;
  isMenuOpen: boolean;
}
export function MobileSidebar({ toggleMenu, isMenuOpen }: IProps) {
  return (
    <Drawer anchor='right' open={isMenuOpen} onClose={toggleMenu}>
      <List>
        <ListItem onClick={toggleMenu}>
          <ListItemIcon>
            <MenuIcon />
          </ListItemIcon>
          <ListItemText primary='Menu' />
        </ListItem>
        <ListItem >
          <ListItemIcon>
            <HomeIcon />
          </ListItemIcon>
          <ListItemText primary='Aluguel' />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <InfoIcon />
          </ListItemIcon>
          <ListItemText primary='Vendas' />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <ContactMailIcon />
          </ListItemIcon>
          <ListItemText primary='Sobre' />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <PersonIcon />
          </ListItemIcon>
          <ListItemText primary='Contato' />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <ExitToAppIcon />
          </ListItemIcon>
          <ListItemText primary='Login' />
        </ListItem>
      </List>
    </Drawer>
  )
}
