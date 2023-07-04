import { UseQueryResult, useQuery } from 'react-query';
import { useParams } from 'react-router-dom';
import PropertyAddressDetails from './PropertyAddressDetails';
import { useMemo, useState } from 'react';
import { Slider, Button, Stack, Box } from '@mui/material';
import ArrowLeftIcon from '@material-ui/icons/ArrowLeft';
import ArrowRightIcon from '@material-ui/icons/ArrowRight';

import './houseDetails.scss'
import { theme, useStyles } from '../../styles/styles';
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

function PropertyDetails() {
  const classes = useStyles({ color: theme.palette.primary.dark })
  const abortController = new AbortController();
  const abortSignal = abortController.signal;
  const { id } = useParams();
  const { data }: UseQueryResult<IData> = useQuery(['my-data', id], async () => {
    const url = `${BASE_URL}/properties?id=${id}`;
    const request = await fetch(url, { signal: abortSignal });
    const response = await request.json();
    return response;
  });

  const [propertyData] = useMemo(() => (data ? data.result : []), [data]);
  const [currentStep, setCurrentStep] = useState(0);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const handleSliderChange = (_: Event, value: number | number[]) => {
    if (typeof value === 'number') {
      setCurrentStep(value);
    }
  };

  const handleOpenDialog = () => {
    setIsDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
  };

  return (
    <>
      <PropertyAddressDetails propertyData={propertyData} />
      <Stack mt={2} mb={2} direction="column" gap={4} justifyContent="center" alignItems="center">
        <Slider
          value={currentStep}
          onChange={handleSliderChange}
          step={1}
          min={0}
          max={propertyData.image_urls.length - 1}
          marks
          style={{ width: '80%', margin: 'auto' }}
        />

        <div style={{ display: 'contents' }} >
          {propertyData.image_urls.map((imageUrl, index) => (
            <picture
              key={index}
              className={`property-image ${index !== currentStep ? 'hidden' : ''}`}
              style={{
                animation: index === currentStep ? 'fade-in 300ms ease-in-out' : 'fade-out 300ms ease-in-out',
              }}
            >
              <source type="image/png" srcSet={imageUrl} />
              <img
                src={imageUrl}
                alt={`Image ${index}`}
                loading="lazy"
                decoding="async"
                width="100%"
              />
            </picture>
          ))}
        </div>
      </Stack>
      <Stack direction="row" justifyContent="center" width="100%" >
        <Button variant="contained" sx={{ margin: "16px 0", width: 'fit-content' }} onClick={handleOpenDialog}>
          Ver todas as fotos
        </Button >
      </Stack>
      <Stack
        className={`${classes.overlay} ${isDialogOpen ? classes.active : ''}`}
      >
        <Button
          disableRipple
          variant="contained"
          className={classes.closeButton}
          onClick={handleCloseDialog}>
          X
        </Button >
        <ArrowLeftIcon
          className={classes.leftArrowButton}
          onClick={() => {
            setCurrentStep((prevStep) => (prevStep - 1) % propertyData.image_urls.length);
          }}
        />
        <ArrowRightIcon
          className={classes.rightArrowButton}
          onClick={() => {
            setCurrentStep((prevStep) => (prevStep + 1) % propertyData.image_urls.length);
          }}
        />
        <Box
          margin="auto"
          width="50%"
          height="50%"
          overflow="hidden"
          style={{
            backgroundImage: `url(${propertyData.image_urls[currentStep]})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat',
          }}
        />
        <Stack
          direction="row"
          margin="16px auto"
          justifyContent="center"
          gap={5}
          width="80%"
          overflow="scroll"
          component="ul"
        >
          {propertyData.image_urls.map((imageUrl, index) => (
            <li
              key={index}
              className="properties-container"
              style={{
                width: '150px',
                height: '100px',
              }}
              onClick={() => setCurrentStep(index)}
            >
              <picture style={{ width: '100%', height: '100%', objectFit: 'cover' }}>
                <source type="image/png" srcSet={imageUrl} />
                <img
                  src={imageUrl}
                  alt={`Image ${index}`}
                  loading="lazy"
                  decoding="async"
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
              </picture>
            </li>
          ))}
        </Stack>
      </Stack>
      <Footer />
    </>
  );
}

export default PropertyDetails;