import * as React from 'react';
import { Box } from '@mui/system';
import { AppContext, AppContextType } from '../../context/appContext';
import Typography from '@mui/material/Typography';
import { InputAdornment, TextField, Button, Stack } from '@mui/material';
import { AccountCircle, Email, Visibility, VisibilityOff } from '@mui/icons-material';
import IconButton from '@mui/material/IconButton';
import CircularProgress from '@mui/material/CircularProgress';

import './LoginModal.scss';
import CustomModal from './CustomModal';
import { submitCredentials } from '../../utils/api';

export default function LoginModal() {
  const { isOpenLoginModal, handleModal } = React.useContext<AppContextType>(AppContext);

  const [responseStatus, setResponseStatus] = React.useState<number | undefined>(undefined);
  const [isSubmiting, setIsSubmiting] = React.useState<boolean>(false);
  const [showPassword, setShowPassword] = React.useState<boolean>(false);

  const [credentials, setCredentials] = React.useState<{ email: string, password: string, username: string }>({
    email: '',
    password: '',
    username: '',
  });

  const [isValidFields, setValidFields] = React.useState<{ email: boolean, password: boolean, username: boolean }>({
    email: true,
    password: true,
    username: true,
  });

  const loadingIndicator = <CircularProgress size={24} color="inherit" />;

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value, name } = event.target;
    setCredentials({
      ...credentials,
      [name]: value
    })
  };

  const handleShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const validateCredentials = () => {
    const { email, password, username } = credentials;
    const emailRegex = /^[a-zA-Z0-9]+([._]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+\.(com|com\.br|net)$/;
    const passwordRegex = /^(?!.*(\w)\1\1\1)[A-Za-z\d@$!%*?&]{7,}(?=.*[A-Z])(?=.*[@$!%*?&]).*$/;
    const usernameRegex = /^[a-zA-Z0-9]+$/;

    const isValidEmail = emailRegex.test(email);
    const isValidPassword = passwordRegex.test(password);
    const isValidUsername = usernameRegex.test(username);

    setValidFields({
      email: isValidEmail,
      password: isValidPassword,
      username: isValidUsername,
    });

    return isValidEmail && isValidPassword && isValidUsername;
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const isValid = validateCredentials();
    if (isValid) {
      setIsSubmiting(true)
      const response = await submitCredentials(credentials);
      setTimeout(() => setIsSubmiting(false), 1500);
      setTimeout(() => setResponseStatus(response?.status), 1500);
    }
  };

  React.useEffect(() => {
    if (!isOpenLoginModal) {
      setCredentials({
        username: '',
        email: '',
        password: '',
      });
    }
    return () => {
      setCredentials({
        username: '',
        email: '',
        password: '',
      });
    };
  }, [isOpenLoginModal]);


  return (
    <CustomModal
      open={isOpenLoginModal}
      onClose={() => handleModal(false)}
    >
      <Box className="login-modal">
        <Typography textAlign="center" variant="h3">Login</Typography>
        <form onSubmit={handleSubmit}>
          <Box mt={2}>
            <TextField
              name="username"
              fullWidth
              variant="outlined"
              label="Usuário"
              error={!isValidFields.username}
              helperText={!isValidFields.username ? 'Campo usuário é obrigatório' : ''}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <AccountCircle />
                  </InputAdornment>
                ),
              }}
              value={credentials.username}
              onChange={handleChange}
            />
          </Box>
          <Box mt={2}>
            <TextField
              name="email"
              fullWidth
              variant="outlined"
              label="Email"
              error={!isValidFields.email}
              helperText={!isValidFields.email ? 'Campo `email` deve ser como usuario@gmail.com(.br)' : ''}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Email />
                  </InputAdornment>
                ),
              }}
              value={credentials.email}
              onChange={handleChange}
            />
          </Box>
          <Box mt={2}>
            <TextField
              name="password"
              fullWidth
              variant="outlined"
              label="Senha"
              type={showPassword ? 'text' : 'password'}
              error={!isValidFields.password}
              helperText={!isValidFields.password ? 'Campo `senha` deve conter pelo menos 7 caracteres, 1 letra maiúscula, não mais que 3 caracteres repetidos consecutivos' : ''}

              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    {showPassword ? (
                      <IconButton onClick={handleShowPassword}>
                        <Visibility />
                      </IconButton>
                    ) : (
                      <IconButton onClick={handleShowPassword}>
                        <VisibilityOff />
                      </IconButton>
                    )}
                  </InputAdornment>
                ),
              }}
              value={credentials.password}
              onChange={handleChange}
            />
          </Box>
          {
            responseStatus === 201
            && (
              <Typography component="h3" width="100%" mt={2} textAlign="center" color="red">
                Usuário criado com sucesso!
              </Typography>
            )
          }
          {
            (responseStatus === 422)
            && (
              <Typography component="h3" width="100%" mt={2} textAlign="center" color="red">
                Email já cadastrado, tente novamente usando outro email.
              </Typography>
            )
          }
          {
            (responseStatus !== 201 && responseStatus !== 422 && responseStatus)
            && (
              <Typography component="h3" width="100%" mt={2} textAlign="center" color="red">
                Houve um error ao enviar os dados, por favor tente novamente.
              </Typography>
            )
          }
          <Stack component="div" width="100%" direction="row" justifyContent="center">
            <Button
              type="submit"
              sx={{ mt: 2, textAlign: 'center' }}
              variant="contained"
              disabled={isSubmiting}
              startIcon={isSubmiting ? loadingIndicator : null}
            >
              {isSubmiting ? 'enviando' : 'enviar'}
            </Button>
          </Stack>
        </form>
      </Box >
    </CustomModal >
  );
}