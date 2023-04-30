import { Stack } from '@mui/material';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';

import Logo from '../../assets/real-state-logo.png';

import '../DesktopHeader.scss'

function MobileHeader() {
  return (
    <Stack
      direction="row"
      component="header"
      justifyContent="space-between"
      alignItems="center"
      margin="0 20px"
    >
      <Stack
        component="div"
        maxWidth="100px"
        minWidth="100px"
        minHeight="50px"
      >
        <img id="logo" src={Logo} width="100%" height="100%" alt="logo" />
      </Stack>
      <IconButton disableFocusRipple disableTouchRipple aria-label="menu" sx={{ outline: "none" }} size="large">
        <MenuIcon />
      </IconButton>
    </Stack>
  )
}

export default MobileHeader;
