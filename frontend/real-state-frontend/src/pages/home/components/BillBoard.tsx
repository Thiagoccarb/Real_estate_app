import { Box } from '@material-ui/core';

function Billboard() {

  return (
    <>
      <Box
        component="div"
        position="relative"
        width="200px"
        height="calc(100vw / 1.5)"
        color="red"
        style={{ opacity: "0.5" }}
        zIndex={2}
      >
        <h1>test</h1>
      </Box>
    </>
  )
}

export default Billboard;
