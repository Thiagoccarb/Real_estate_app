import { ReactNode } from 'react';
import MuiAlert, { AlertColor } from '@mui/material/Alert';

export const Alert = ({ severity, children }: { severity: AlertColor | undefined, children: ReactNode }) => {
  return (
    <MuiAlert elevation={6} variant="filled" severity={severity}>
      {children}
    </MuiAlert>
  );
};
