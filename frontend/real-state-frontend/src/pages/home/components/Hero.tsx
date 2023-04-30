import React from 'react';
import { Grid } from '@material-ui/core';
import { CSSTransition } from 'react-transition-group';

import img from '../../../assets/mansion.jpg';
import '../home.scss';

const Hero = () => {
  const [zoomIn, setZoomIn] = React.useState<boolean>(false);

  const handleZoomIn = () => {
    setZoomIn(true);
  };

  return (
    <>
      <Grid
        item
        className="hero-container"
        container
      >
        <Grid
          component="div"
          className="hero"
          item
        >
          <CSSTransition
            in={zoomIn}
            timeout={300}
          >
            <picture>
              <source
                type="image/png"
              />
              <img
                loading="lazy"
                decoding="async"

                src={img}
                alt="hero-image"
                className={zoomIn ? "zoomIn" : "zoomIn zoomOut"}
                onLoad={handleZoomIn}
              />
            </picture>
          </CSSTransition>
        </Grid>
      </Grid>
    </>
  );
};

export default Hero;
