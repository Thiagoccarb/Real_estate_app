import { useContext } from 'react';
import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";
import {
  Bathtub as BathtubIcon,
  KingBed as KingBedIcon,
} from '@material-ui/icons';
import { Stack } from '@mui/material';
import { Box, Button, Typography } from '@material-ui/core';

import '../home.scss';
import { AppContext, AppContextType } from '../../../context/appContext';
import { IResult } from '../Home';

const Caroussel = ({ data }: { data: IResult[] | undefined }) => {
  const { isMobileScreen } = useContext<AppContextType>(AppContext);

  if (!data) return (<Typography variant='h1' component='h1'> there was an error fetching properties data </Typography>)

  const responsive = {

    desktop: {
      breakpoint: { max: 3400, min: 768 },
      items: 1,
    },

    mobile: {
      breakpoint: { max: 768, min: 0 },
      items: 1,
    },
  };

  return (
    <Box id="caroussel-container">
      <Typography style={{ textAlign: 'center', color: '#0D3149' }}
        variant='h2'
        component="h2"
      >
        Novidades da semana
      </Typography>
      <Carousel
        arrows={true}
        swipeable={false}
        showDots={false}
        responsive={responsive}
        ssr={true}
        infinite={true}
        autoPlay={true}
        autoPlaySpeed={10000}
        keyBoardControl={true}
      >
        {
          data.map((item,) => (
            <Stack
              direction={isMobileScreen ? 'column' : 'row'}
              width='100%'
              id="caroussel-card"
            >
              <img src={item.image_urls[0]} className={isMobileScreen ? 'carousel-image-mobile' : 'carousel-image-desktop'} />
              <Stack
                direction='column'
              >
                <Typography variant='h2' component="h3">{item.name}</Typography>
                <Typography variant='h3' component="h4">{item.description}</Typography>
                <Stack direction="row" gap={2} alignItems="center">
                  <Button style={{ backgroundColor: '#C42F21', borderRadius: 0 }} >
                    Saiba mais
                  </Button>
                  <Stack direction="row" alignItems="center">
                    <KingBedIcon style={{ color: '#C42F21' }} />
                    <span>{item.bedrooms ?? ''}</span>
                  </Stack>
                  <Stack direction="row" alignItems="center">
                    <BathtubIcon style={{ color: '#C42F21' }} />
                    <span>{item.bathrooms ?? ''}</span>
                  </Stack>
                </Stack>
              </Stack>
            </Stack>
          ))
        }
      </Carousel>
    </Box>
  );
};

export default Caroussel;
