import React, { useState } from 'react';
import {
  Avatar,
  Popover,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Button,
  Typography,
} from '@material-ui/core';
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import AddIcon from '@mui/icons-material/Add';
import ChangeCircleIcon from '@mui/icons-material/ChangeCircle';

import { theme } from '../../styles/styles';
import { useCookie } from '../../hooks/useCookie';
import { useNavigate } from 'react-router-dom';

export function AvatarLoginListItem() {
  const navigate = useNavigate()
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [cookieValue, _] = useCookie('credentials');

  const handlePopoverOpen = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handlePopoverClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);

  return (
    <div style={{ display: 'flex' }}>
      <Button
        disableTouchRipple
        onClick={handlePopoverOpen}
        aria-owns={open ? 'login-options-popover' : undefined}
        aria-haspopup="true"
      >
        <Avatar style={{ backgroundColor: theme.palette.green.main }}>
          <AccountBoxIcon />
        </Avatar>
      </Button>
      <div>
        <Typography component="h2">{`Olá, ${cookieValue.username}`}</Typography>
        <Popover
          id="login-options-popover"
          open={open}
          anchorEl={anchorEl}
          onClose={handlePopoverClose}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'center',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'center',
          }}
        >
          <List>
            <ListItem button onClick={() =>navigate('/logged/add-property') }>
              <ListItemIcon>
                <AddIcon />
              </ListItemIcon>
              <ListItemText primary="Adicionar propriedade" />
            </ListItem>
            <ListItem button>
              <ListItemIcon>
                <ChangeCircleIcon />
              </ListItemIcon>
              <ListItemText primary="Atualizar propriedade" />
            </ListItem>
          </List>
        </Popover>
      </div>
    </div>
  )
}
