export const createHoverUnderlineEffect =(color: string) => ({
  '&::before, &::after': {
    content: '""',
    display: 'block',
    position: 'absolute',
    bottom: 0,
    height: '2px',
    backgroundColor: color,
    transition: 'width 0.2s ease-out',
    width: '0%',
  },
  '&::before': {
    left: '50%',
    transform: 'translateX(-70%)',
  },
  '&::after': {
    right: '50%',
    transform: 'translateX(70%)',
  },
  '&:hover::before, &:hover::after': {
    width: '50% !important',
  },
  '&:hover': {
    backgroundColor: 'transparent !important',
  },
  '&:focus, &.Mui-focusVisible': {
    outline: 'none !important',
  },
})