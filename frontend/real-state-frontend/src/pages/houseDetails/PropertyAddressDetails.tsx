import { useContext } from 'react';
import { Stack, Typography } from '@mui/material';
import BathtubIcon from '@material-ui/icons/Bathtub';
import HotelIcon from '@material-ui/icons/Hotel';
import AttachMoneyIcon from '@material-ui/icons/AttachMoney';

import { theme } from '../../styles/styles';
import { AppContext, AppContextType } from '../../context/appContext';

export interface IResult {
  id: number,
  name: string,
  action: string,
  type: string,
  created_at: string,
  updated_at: null | string,
  price: number,
  bedrooms: number,
  bathrooms: number,
  description: string,
  image_urls: string[]
  address: {
    street_name: string,
    number: number | null,
    cep: string
  },
  city: {
    name: string,
    state: string
  }
}

function PropertyAddressDetails({ propertyData }: { propertyData: IResult }) {
  const { isMobileScreen } = useContext<AppContextType>(AppContext);

  return (
    <Stack direction="column" gap={isMobileScreen ? 2 : 5} margin="50px 20px 0">
      <Typography variant='h2' component="h2" sx={{ ...theme.typography.h2, color: '#0D3149', margin: 0 }}>
        {propertyData.name}
      </Typography>
      <Typography variant='h3' component="h3" sx={{ ...theme.typography.h3, color: '#0D3149', margin: 0 }}>

        {propertyData.description}
      </Typography>
      <Typography variant='h2' component="h2" sx={{ ...theme.typography.h2, color: '#0D3149', margin: 0 }}>
        Endereço
      </Typography>
      <Stack direction="row" gap={1}>
        <Typography variant='h3' component="h3" sx={{ ...theme.typography.h3, color: '#0D3149', margin: 0 }}>

          {
            `${propertyData.address.street_name}
         ${propertyData.address.number},
          ${propertyData.city.name} 
          - ${propertyData.city.state}. CEP: ${propertyData.address.cep}.`
          }
        </Typography>
        <Typography
          style={{ color: '#0D3149' }}
          variant='h4'
          component="h4"
        >
        </Typography>
      </Stack>
      <Stack direction="row" gap={5} flexWrap="wrap" justifyContent="center">
        <Stack direction="row" alignItems="center" gap={1}>
          <BathtubIcon style={{ color: '#0D3149', fontSize: '9vmin' }} />

          <Typography variant='h2' component="h2" sx={{ ...theme.typography.h2, color: '#0D3149', margin: 0 }}>

            {propertyData.bathrooms}
          </Typography>
        </Stack>
        <Stack direction="row" alignItems="center" gap={1}>
          <HotelIcon style={{ color: '#0D3149', fontSize: '9vmin' }} />
          <Typography variant='h2' component="h2" sx={{ ...theme.typography.h2, color: '#0D3149', margin: 0 }}>

            {propertyData.bedrooms}
          </Typography>
        </Stack>
        <Stack direction="row" alignItems="center" gap={1}>
          <AttachMoneyIcon style={{ color: '#0D3149', fontSize: '9vmin' }} />
          <Typography variant='h2' component="h2" sx={{ ...theme.typography.h2, color: '#0D3149', margin: 0 }}>

            {`R$ ${propertyData.price.toFixed(2)}`}
          </Typography>
        </Stack>
      </Stack>
    </Stack>
  )
}

export default PropertyAddressDetails;
