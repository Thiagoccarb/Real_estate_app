import { useContext } from 'react';
import { Typography } from '@material-ui/core';
import { Stack } from '@mui/material';

import { AppContext, AppContextType } from '../context/appContext';
import Logo from '../assets/real-state-logo.png';

const Footer = () => {
  const { isMobileScreen } = useContext<AppContextType>(AppContext);

  return (
    <Stack
      direction={isMobileScreen ? 'column' : 'row'}
      gap={isMobileScreen ? 0 : 2}
      bgcolor='#E5E5E5'
      position='absolute'
      left={0}
      width='100vw'
      justifyContent='center'
      alignItems='center'
    >
      <Stack direction='column' gap={isMobileScreen ? 0 : 2} ml={2}>
        <Stack direction='row' alignItems='center' justifyContent='flex-start' >
          <picture>
            <source
              type="image/png"
            />
            <img
              loading="lazy"
              decoding="async"
              width='50px'
              height="50px"
              src={Logo}
              alt="logo-image"
            />
          </picture>
          <Typography 
          style={{ color: '#0D3149', fontWeight: '700', marginLeft: '16px' }}
            variant='h3'
            component="h3"
          >
            Carboneri imóveis
          </Typography>
        </Stack >
        <Typography style={{ color: '##E0F8FE' }}
          variant='h4'
          component="h4"
        >
          A imobilária que acredita nos seus sonhos!
        </Typography>
      </Stack>
      <Stack direction='column' gap={isMobileScreen ? 0 : 2}  ml={2}>
      <Typography style={{ color: '#0D3149', fontWeight: '700' }}
          variant='h3'
          component="h3"
        >
          Venha nos visitar
        </Typography>
        <Typography style={{ color: '##E0F8FE' }}
          variant='h4'
          component="h4"
        >
          Avenida presidente vargas, 99999.
          <br />
          Ribeirão Preto - SP 14026-000
        </Typography>
      </Stack>
      <Stack direction='column' gap={isMobileScreen ? 0 : 2}  ml={2}>
        <Typography style={{ color: '#0D3149', fontWeight: '700' }}
          variant='h3'
          component="h3"
        >
          Atendimento
        </Typography>
        <Typography style={{ color: '##E0F8FE' }}
          variant='h4'
          component="h4"
        >
          Segunda a sexta das 8h às 18h
          <br />
          Sábado das 8h às 13h
        </Typography>
      </Stack>
    </Stack >
  );
};

export default Footer;
