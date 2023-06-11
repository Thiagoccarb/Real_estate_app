import React, { useState, ChangeEvent, useContext, useRef } from 'react';
import {
  Button,
  Checkbox,
  FormControl,
  FormControlLabel,
  FormHelperText,
  FormLabel,
  Grid,
  Input,
  InputAdornment,
  InputLabel,
  MenuItem,
  Radio,
  RadioGroup,
  Select,
  TextField,
  Typography,
  CircularProgress,
  Snackbar,
} from '@material-ui/core';
import {
  PhotoLibrary as PhotoLibraryIcon,
  Bathtub as BathroomIcon,
  KingBed as KingBedIcon,
  Home as HomeIcon,
  Apartment as ApartmentIcon,
  RadioButtonChecked as RadioButtonCheckedIcon,
  RadioButtonUnchecked as RadioButtonUncheckedIcon,
} from '@material-ui/icons';
import { Stack } from '@mui/material';
import InputMask from 'react-input-mask';

import { AppContextType, AppContext } from '../../../context/appContext';
import CurrencyInput from 'react-currency-input-field';
import { brazilianStates } from './states';
import { IProperty } from './interfaces';
import { createProperty, createPropertyImages } from '../../../utils/api';
import { Alert } from './Alert';
import '../AddProperty.scss'

type Action = 'rent' | 'sale';
type Type = 'house' | 'apartament';

interface State {
  name: string;
  action: Action;
  type: Type;
  bathrooms: number;
  rooms: number;
  description: string;
  address: string;
  noNumber: boolean;
  cep: string;
  images: string[];
  draggingIndex: number | null;
  state: typeof brazilianStates[number]['abbreviation'] | '',
  number: number | string,
  city: string,
  price: string,
}

const cepRegex = /^\d{5}-\d{3}$/;

function AddProperty() {
  const inputRef = useRef<HTMLInputElement>(null);
  const { isMobileScreen } = useContext<AppContextType>(AppContext);

  const [SubmissionSuccess, setSubmissionSuccess] = useState<boolean>(false)
  const [isFormSent, setIsFormSent] = useState<boolean>(false)
  const [isSubmiting, setIsSubmiting] = useState<boolean>(false)

  const [state, setState] = useState<State>({
    name: '',
    action: 'rent',
    type: 'house',
    bathrooms: 1,
    rooms: 1,
    description: '',
    address: '',
    noNumber: false,
    cep: '',
    images: [],
    draggingIndex: null,
    state: '',
    number: '',
    city: '',
    price: '',
  });

  const initialStateValidation = {
    name: true,
    action: true,
    type: true,
    bathrooms: true,
    rooms: true,
    description: true,
    address: true,
    noNumber: false,
    cep: true,
    images: true,
    state: true,
    number: true,
    city: true,
    price: true,
  };

  const [formError, setError] = useState<Partial<Record<keyof typeof state, boolean>>>(initialStateValidation);

  const cepInputRef = useRef<HTMLInputElement>(null);

  const handleChange = (event: React.ChangeEvent<{ name?: string; value: unknown }>) => {
    const { name, value, type, checked } = event.target as HTMLInputElement;

    if (['bathrooms', 'rooms'].includes(name) && Number(value) < 0) {
      return null;
    }

    if (type === 'checkbox') {
      setState((prevState) => ({
        ...prevState,
        [name]: checked,
        number: '',
      }));
    } else {
      setState((prevState) => ({
        ...prevState,
        [name]: value,
      }));
    }
  };

  const handlePriceChange = (value: string) => {
    setState((prevState) => ({
      ...prevState,
      price: value
    }));
  };

  const handleImagesChange = (event: ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    const images: string[] = [];
    if (!files) return null;

    for (let i = 0; i < files.length; i++) {
      const file = files[i];

      if (!file.type.startsWith('image/')) {
        continue;
      }

      const reader = new FileReader();
      reader.readAsDataURL(file);

      reader.onload = () => {
        images.push(reader.result as string);

        if (images.length === files.length) {
          setState((prevState) => ({
            ...prevState,
            images,
          }));
        }
      };
    }
  };

  const handleCEPChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const cep = event.target.value;
    setState((prevState) => ({
      ...prevState,
      cep
    }));
    if (cepRegex.test(cep)) {
      try {
        const response = await fetch(`https://opencep.com/v1/${cep.replace('-', '')}`);
        if (response.status === 200) {
          const { logradouro: address, localidade: city, uf } = await response.json();
          setState((prevState) => ({
            ...prevState,
            state: uf,
            address,
            city,
          }))
        } else {
          console.log('Error fetching address data:', response.status);
        }
      } catch (error) {
        console.log('Error fetching address data:', error);
        return null
      }
    }
  };

  const handleDragStart = (index: number) => {
    setState((prevState) => ({
      ...prevState,
      draggingIndex: index,
    }));
  };

  const handleDragOver = (e: React.DragEvent<HTMLImageElement>) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent<HTMLImageElement>, newIndex: number) => {
    e.preventDefault();
    const { draggingIndex } = state;

    const newImages = [...state.images];
    const [draggedImage] = newImages.splice(draggingIndex as number, 1);
    newImages.splice(newIndex, 0, draggedImage);

    setState((prevState) => ({
      ...prevState,
      images: newImages,
      draggingIndex: null,
    }));
  };

  const validateForm = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const errors: Partial<Record<keyof typeof state, boolean>> = {};

    Object.entries(state).forEach(([name, value]) => {
      if (['draggingIndex', 'noNumber'].includes(name)) {
        return;
      }
      else if (name === 'number') {
        if (state.noNumber) {
          return errors[name as keyof typeof state] = true;
        }
        errors[name as keyof typeof state] = value !== ''
      }
      else if (name === 'images') {
        return errors[name as keyof typeof state] = !!state.images.length;
        errors[name as keyof typeof state] = value !== ''
      }
      else if (name === 'cep') {
        errors[name] = cepRegex.test(value);
      } else {
        errors[name as keyof typeof state] = value !== '';
      }
    });
    setError(errors);
    return Object.values(errors).every((e) => e)
  };

  const submitData = async (e: React.FormEvent<HTMLFormElement>) => {
    const isValidForm = validateForm(e);
    if (!isValidForm) return null
    setIsSubmiting(true)
    const data: Omit<IProperty, 'images'> = {
      name: state.name,
      action: state.action,
      type: state.type,
      description: state.description,
      bedrooms: state.rooms,
      bathrooms: state.bathrooms,
      price: parseFloat(state.price.replace(",", ".")),
      city: {
        name: state.city,
        state: state.state
      },
      address: {
        street_name: state.address,
        number: state.number,
        cep: state.cep
      }
    }
    const response = await createProperty(data)

    setSubmissionSuccess(response?.status === 201)
    if (response?.status === 201) {
      const { result: { id } } = response;
      const imagesData = state.images.map((el) => {
        const [, base64String] = el.split(',')
        return base64String
      });
      await createPropertyImages(
        {
          list_str_binary: imagesData,
          property_id: id,
        }
      )
    }
    return setTimeout(() => {
      setIsFormSent(true)
      setIsSubmiting(false)
    }, 1500)
  }

  const renderImages = () => {
    return (
      <Stack
        className='image-container'
        direction="row"
        gap={2}
        marginTop="20px"
      >
        {state.images.map((image, index) => (
          <div style={{ position: 'relative' }}>
            <button
              style={{
                width: 20,
                height: 20,
                position: 'absolute',
                zIndex: 2,
                backgroundColor: 'red',
                borderRadius: '50%',
                top: 0,
                right: 0,
                color: 'white',
                cursor: 'pointer',
                border: 'none',
              }}
              onClick={() => setState((prevState) => ({
                ...prevState,
                images: prevState.images.filter((_, i) => i !== index),
              }))}
            >
              x
            </button>
            <img
              key={index}
              src={image}
              alt={`Imagem ${index}`}
              style={{
                width: 100,
                height: 100,
                cursor: 'move',
                opacity: index === state.draggingIndex ? 0.5 : 1,
              }}
              draggable
              onDragStart={() => handleDragStart(index)}
              onDragOver={handleDragOver}
              onDrop={(e) => handleDrop(e, index)}
            />
          </div>
        ))
        }
      </Stack >
    );
  };

  return (
    <Grid
      container
      component="section"
      style={{ margin: '0 20px', width: 'initial', gap: 20 }}
    >
      <form onSubmit={submitData} style={{ width: '-webkit-fill-available' }} >

        <Grid item style={{ maxWidth: '-webkit-fill-available' }}>
          <input
            accept="image/*"
            style={{ display: 'none' }}
            id="imagens-input"
            multiple
            type="file"
            ref={inputRef}
            onChange={handleImagesChange}
          />
          <label htmlFor="imagens-input">
            <Typography component="h2" variant="h2">
              Adicionar fotos
            </Typography>
            <Typography component="h3" variant="h3">
              Arraste as fotos para escolher sequência
            </Typography>
            <Button variant="contained" color="inherit" onClick={() => inputRef.current?.click()}>
              Importar imagens
              <PhotoLibraryIcon style={{ marginLeft: '10px' }} />
            </Button>
            {!formError?.images && <FormHelperText style={{ color: 'red' }} >Nenhuma imagem foi adicioanda</FormHelperText>}

          </label>
          {renderImages()}
        </Grid>
        <Grid item style={{ width: '100%', margin: 'auto' }}>
          <TextField
            label="Nome"
            name="name"
            value={state.name}
            onChange={handleChange}
            fullWidth
            error={!formError?.name}
            helperText={!formError?.name && "Campo inválido"}
          />
        </Grid>
        <Grid item style={{ width: '100%', margin: 'auto' }}>
          <TextField
            label="Descrição"
            name="description"
            value={state.description}
            onChange={handleChange}
            fullWidth
            multiline
            minRows={3}
            error={!formError?.description}
            helperText={!formError?.description && "Campo inválido"}
          />
        </Grid>
        <Grid item style={{ width: '100%', margin: 'auto' }}>
          <InputMask
            mask="99999-999"
            value={state.cep}
            onChange={handleCEPChange}
          >
            <TextField
              inputRef={cepInputRef}
              name="cep"
              label="CEP"
              fullWidth
              error={!formError?.cep}
              helperText={!formError?.cep && "Campo inválido"}
            />
          </InputMask>
        </Grid>
        <Grid item style={{ width: '100%', margin: 'auto' }}>
          <TextField
            label="Endereço"
            name="address"
            value={state.address}
            onChange={handleChange}
            fullWidth
            error={!formError?.address}
            helperText={!formError?.address && "Campo inválido"}
          />
        </Grid>
        <Stack direction="row" width="100%" gap={2}>
          <Grid item style={{ width: '100%', margin: ' 0 auto', }}>
            <TextField
              label="Cidade"
              name="city"
              onChange={handleChange}
              value={state.city}
              fullWidth
              error={!formError?.city}
              helperText={!formError?.city && "Campo inválido"}
            />
          </Grid>
          <Grid item style={{ width: '100%', margin: 'auto', display: 'flex', flexDirection: 'column' }}>
            <TextField
              label="Número"
              name="number"
              onChange={handleChange}
              value={state.number}
              type="number"
              disabled={state.noNumber}
              error={!formError?.number && !state?.noNumber}
              helperText={!formError?.number && !state?.noNumber && "Campo inválido"}
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={state.noNumber}
                  onChange={handleChange}
                  name="noNumber"
                  color="primary"
                />
              }
              label="Sem número"
            />
          </Grid>
        </Stack>
        <Grid item style={{ width: '100%', margin: 'auto' }}>
          <FormControl fullWidth >
            <InputLabel htmlFor="state">Estado</InputLabel>
            <Select
              id="state"
              name="state"
              value={state.state}
              onChange={handleChange}
              error={!formError?.state}
            >
              {brazilianStates.map((state) => (
                <MenuItem key={state.abbreviation} value={state.abbreviation}>
                  {state.abbreviation}
                </MenuItem>
              ))}
            </Select>
            {!formError?.state && <FormHelperText style={{ color: 'red' }} >Campo inválido</FormHelperText>}
          </FormControl>
        </Grid>
        <Stack
          justifyContent="space-around"
          margin="auto"
          width="100%"
          gap={2}
          direction={isMobileScreen ? 'column' : 'row'}
          mt={2}
        >
          <Grid item>
            <FormControl component="fieldset">
              <FormLabel component="legend">Ação</FormLabel>
              <RadioGroup
                aria-label="action"
                name="action"
                value={state.action}
                onChange={handleChange}
                row
              >
                <FormControlLabel
                  value="rent"
                  control={
                    <Radio
                      icon={<RadioButtonUncheckedIcon />}
                      checkedIcon={<RadioButtonCheckedIcon />}
                    />
                  }
                  label="Aluguel"
                />
                <FormControlLabel
                  value="sale"
                  control={
                    <Radio
                      icon={<RadioButtonUncheckedIcon />}
                      checkedIcon={<RadioButtonCheckedIcon />}
                    />
                  }
                  label="Venda"
                />
              </RadioGroup>
              {!formError?.action && <FormHelperText style={{ color: 'red' }} >Campo inválido</FormHelperText>}
            </FormControl>
          </Grid>
          <Grid item>
            <FormControl component="fieldset">
              <FormLabel component="legend">Tipo</FormLabel>
              <RadioGroup
                aria-label="type"
                name="type"
                value={state.type}
                onChange={handleChange}
                row
              >
                <FormControlLabel
                  value="house"
                  control={<Radio icon={<HomeIcon />} checkedIcon={<HomeIcon />} />}
                  label="Casa"
                />
                <FormControlLabel
                  value="apartment"
                  control={
                    <Radio icon={<ApartmentIcon />} checkedIcon={<ApartmentIcon />} />
                  }
                  label="Apartamento"
                />
              </RadioGroup>
              {!formError?.type && <FormHelperText style={{ color: 'red' }} >Campo inválido</FormHelperText>}
            </FormControl>
          </Grid>
        </Stack>
        <Stack
          margin="auto"
          width="100%"
          gap={2}
          direction={isMobileScreen ? 'column' : 'row'}
        >
          <Grid item style={{ width: '100%' }}>
            <FormControl fullWidth>
              <InputLabel htmlFor="banheiros-input">Banheiros</InputLabel>
              <Input
                fullWidth
                id="banheiros-input"
                name="bathrooms"
                type="number"
                inputProps={{ min: 0 }}
                value={state.bathrooms}
                onChange={handleChange}
                startAdornment={
                  <InputAdornment position="start">
                    <BathroomIcon />
                  </InputAdornment>
                }
                error={!formError?.bathrooms}
              />
              {!formError?.bathrooms && <FormHelperText style={{ color: 'red' }} >Campo inválido</FormHelperText>}
            </FormControl>
          </Grid>
          <Grid item style={{ width: '100%' }}>
            <FormControl fullWidth>
              <InputLabel htmlFor="quartos-input">Quartos</InputLabel>
              <Input
                fullWidth
                id="quartos-input"
                name="rooms"
                type="number"
                inputProps={{ min: 0 }}
                value={state.rooms}
                onChange={handleChange}
                startAdornment={
                  <InputAdornment position="start">
                    <KingBedIcon />
                  </InputAdornment>
                }
                error={!formError?.type}
              />
              {!formError?.type && <FormHelperText style={{ color: 'red' }} >Campo inválido</FormHelperText>}
            </FormControl>
          </Grid>
          <Grid item style={{ width: '100%' }}>
            <TextField
              label="Preço"
              fullWidth
              InputProps={{
                inputComponent: CurrencyInput as any,
                inputProps: {
                  prefix: 'R$',
                  decimalSeparator: ',',
                  groupSeparator: '.',
                  decimalScale: 2,
                  fixedDecimalLength: true,
                  value: state.price,
                  onValueChange: handlePriceChange,
                },
              }}
              error={!formError?.price}
              helperText={!formError?.price && "Campo inválido"}
            />
          </Grid>
        </Stack>
        <Snackbar
          open={isFormSent}
          autoHideDuration={6000}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
          onClose={() => setIsFormSent(false)}
        >
          <Alert severity={SubmissionSuccess ? "success" : "error"}>
            {SubmissionSuccess ? "Propriedade criada com sucesso!" : "Ops, algo deu errado, tente novamente mais tarde!"}
          </Alert>
        </Snackbar>
        <Grid item style={{ display: "flex", justifyContent: "center", width: "100%" }} >
          <Button
            style={{ margin: "16px auto" }}
            variant="contained"
            color="primary"
            type="submit"
            disabled={isSubmiting}
            endIcon={
              isSubmiting ? (
                <CircularProgress size={20} color="inherit" />
              ) : null
            }
          >
            {isSubmiting ? 'Enviando...' : 'Enviar'}
          </Button>
        </Grid>
      </form>
    </Grid >
  );
}

export default AddProperty;