import { Box } from '@material-ui/core';
import { UseQueryResult, useQuery } from 'react-query';
import { Outlet } from 'react-router-dom';

import PropertyCards from '../../components/cards/PropertyCards';
import Footer from '../../components/Footer';

const BASE_URL = import.meta.env.VITE_BASE_URL

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

export interface IData {
  success: boolean,
  error: boolean | string,
  message: null | string,
  next_page: null | string,
  previous_page: null | string,
  result: IResult[]
}

function PropertiesForSale() {
  const abortController = new AbortController();
  const abortSignal = abortController.signal;

  const { data }: UseQueryResult<IData> = useQuery('my-data', async () => {
    const url = `${BASE_URL}/properties`;
    const request = await fetch(url, { signal: abortSignal });
    const response = await request.json()
    return response
  });

  return (
    <>
      <Outlet />
      <Box
        component="section"
        display="flex"
        flexDirection="column"
        style={{ margin: '50px 20px 0 20px' }}
      >
        <PropertyCards title='Venda de imóveis' data={data?.result.filter((item) => item.action == 'sale') ?? []} />
        <Footer />
      </Box>
    </>
  )
}

export default PropertiesForSale;
