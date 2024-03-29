import { useContext } from 'react';
import { Stack, Button } from '@mui/material';

import Divider from '@mui/material/Divider';
import '../DesktopHeader.scss'

import { theme, useStyles } from '../../styles/styles';
import { createHoverUnderlineEffect } from '../../styles/effects';
import { useLocation, useNavigate } from 'react-router-dom';
import { AppContextType, AppContext } from '../../context/appContext';
import { AvatarLoginListItem } from './AvatarLoginListItem';

import { useCookie } from '../../hooks/useCookie';

type Item = {
  items: string[]
}

function NavList({ items }: Item) {
  const [cookieValue, , deleteCookie] = useCookie('credentials');
  const { handleModal } = useContext<AppContextType>(AppContext);
  const { pathname } = useLocation();
  const [, path] = pathname.split('/')

  const navigate = useNavigate()
  const classes = useStyles({ color: theme.palette.primary.dark })

  const greenHoverEffectCss = createHoverUnderlineEffect(theme.palette.green.main)
  return (
    <Stack
      direction="row"
      divider={<Divider variant="fullWidth" orientation="vertical" flexItem />}
      alignItems="center"
      component="ul"
      height="fit-content"
      gap={2}
    >
      {
        items.map((item) => (
          <Button
            component="li"
            disableRipple
            key={item}
            disableFocusRipple={true}
            className={classes.navButton}
            sx={{
              ...greenHoverEffectCss, color: path === item
                ? `${theme.palette.green.main} !important`
                : 'inherit'
            }}
            onClick={() => navigate(`/${item}`)}
          >
            {item}
          </Button>
        ))
      }
      {
        cookieValue && (
          <Button
            component="li"
            disableRipple
            disableFocusRipple={true}
            className={classes.navButton}
            sx={{
              ...greenHoverEffectCss, color: 'inherit'
            }}
            onClick={() => {
              deleteCookie('credentials');
              setTimeout(() => navigate('/home'), 1500);
            }}
          >
            Sair
          </Button>
        )
      }
      {
        !cookieValue && (
          <Button
            component="li"
            color='inherit'
            disableRipple
            disableFocusRipple={true}
            className={classes.navButton}
            sx={greenHoverEffectCss}
            onClick={() => handleModal(true)}
          >
            login
          </Button>
        )
      }
      {
        cookieValue && <AvatarLoginListItem />
      }
    </Stack>
  )
}

export default NavList;
