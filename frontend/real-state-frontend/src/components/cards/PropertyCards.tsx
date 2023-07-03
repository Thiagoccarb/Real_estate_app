import { useContext } from 'react';
import { Card, CardContent, Typography } from '@material-ui/core';
import { Bathtub as BathtubIcon, KingBed as KingBedIcon } from '@material-ui/icons';
import { Box } from '@mui/system';
import Carousel from 'react-multi-carousel';
import { useNavigate } from 'react-router-dom';

import { AppContext, AppContextType } from '../../context/appContext';
import { IResult } from '../../pages/home/Home';
import { theme, useStyles } from '../../styles/styles';
import '../../pages/home/home.scss';

const PropertyCards = ({ data, title }: { data: IResult[] | [], title: string }) => {
  const navigate = useNavigate()
  const classes = useStyles({ color: theme.palette.primary.dark });
  const { isMobileScreen } = useContext<AppContextType>(AppContext);

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
    <>
      {

        data.length > 0 && (
          <Box style={{ margin: '50px 0' }}>
            <Typography style={{ textAlign: 'center', color: '#0D3149' }}
              variant='h2'
              component="h2"
            >
              {title}
            </Typography>
            <Box
              display="flex"
              flexDirection={isMobileScreen ? 'column' : 'row'}
              width='100%'
              justifyContent="center"
              gap={2}
            >
              {data.map((property) => (
                <Card
                  style={{ width: isMobileScreen ? '100%' : '30%', cursor: 'pointer', listStyle: 'none' }}
                  component="li"
                  key={property.id}
                  className={classes.shadows}
                  onClick={() => {
                    const forRentPath = title.split(' ').includes('Aluguel') ? 'aluguel' : 'venda'
                    navigate(`/${forRentPath}/${property.id}`)
                  }}
                >
                  <picture>
                    <source type="image/png" />
                    <Carousel
                      arrows={false}
                      responsive={responsive}
                      ssr={true}
                      infinite={true}
                      autoPlay={true}
                      autoPlaySpeed={5000}
                      keyBoardControl={true}
                    >
                      {
                        property.image_urls.map((image, ind) => (
                          <img
                            className="property-image"
                            loading="lazy"
                            decoding="async"
                            src={image}
                            alt={`property-picture-${ind + 1}`}
                          />
                        ))
                      }
                    </Carousel>
                  </picture>
                  <CardContent >
                    <Typography style={{ color: '#0D3149', fontWeight: '700', textAlign: 'center', height: isMobileScreen ? '50px' : '100px', overflow: 'scroll' }}
                      variant='h3'
                      component="h3"
                    >
                      {property.name}
                    </Typography>
                    <Typography
                      style={{ color: '#0D3149', textAlign: 'center', height: isMobileScreen ? '100px' : '200px', overflow: 'scroll' }}
                      variant='h4'
                      component="h4"
                    >
                      {property.description}
                    </Typography>
                    <Box display="flex" justifyContent="space-evenly">
                      <Box display="flex" alignItems="center">
                        <KingBedIcon style={{ color: '#C42F21' }} />
                        <span>{property.bedrooms ?? ''}</span>
                      </Box>
                      <Box display="flex" alignItems="center">
                        <BathtubIcon style={{ color: '#C42F21' }} />
                        <span>{property.bathrooms ?? ''}</span>
                      </Box>
                    </Box>
                  </CardContent>
                </Card>
              ))}
            </Box>
          </Box >
        )
      }
    </>
  );
};

export default PropertyCards;
