import * as React from 'react';
import clsx from 'clsx';
import { styled } from '@mui/system';
import Modal, { ModalProps } from '@mui/material/Modal';

import './LoginModal.scss';

type CustomModalProps = {
  open: boolean;
  onClose: () => void;
  children: React.ReactElement;
};

const CustomModal = ({ open, onClose, children }: CustomModalProps) => {
  return (
    <div>
      <StyledModal
        open={open}
        onClose={onClose}
        slots={{ backdrop: StyledBackdrop }}
      >
        {children}
      </StyledModal>
    </div>
  );
};

const Backdrop = React.forwardRef<HTMLDivElement, { open?: boolean; className: string }>(
  (props, ref) => {
    const { open, className, ...other } = props;
    return (
      <div
        className={clsx({ 'MuiBackdrop-open': open }, className)}
        ref={ref}
        {...other}
      />
    );
  }
);

const StyledModal = styled(Modal) <ModalProps>`
  position: fixed;
  z-index: 1300;
  right: 0;
  bottom: 0;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const StyledBackdrop = styled(Backdrop) <{ open?: boolean }>`
  z-index: -1;
  position: fixed;
  right: 0;
  bottom: 0;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.8);
  -webkit-tap-highlight-color: transparent;
`;

export default CustomModal;
