import { Stack } from '@mui/material';

import Logo from '../../assets/real-state-logo.png';
import NavList from './NavList';

import '../DesktopHeader.scss'

const navItems: string[] = ["home", "aluguel", "venda", "sobre", "contato"]


function DeskTopHeader() {
  return (
    <Stack
      direction="row"
      component="header"
      justifyContent="space-between"
      alignItems="center"
      margin="0 20px"
    >
      <Stack
        direction="row"
        component="div"
        width="100%"
        justifyContent="flex-start"
        alignItems="center"
        margin="auto"
        gap={2}
      >
        <img id="logo" src={Logo} width='150px' height="150px" alt='logo' />
      </Stack>
      <Stack direction="row" component="nav">
        <NavList items={navItems} />
      </Stack>
    </Stack>
  )
}

export default DeskTopHeader;
