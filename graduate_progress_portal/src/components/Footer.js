import React from 'react';

const Footer = () => {
  const footerStyle = {
    backgroundColor: '#630031', // Chicago Maroon 
    height: '30px',
    width: '100%', 
    display: 'flex',
    justifyContent: 'center', 
    alignItems: 'center', 
    position: 'static', 
    marginTop: '40px',
  };

  const paragraphStyle = {
    margin: '0', 
  };

  return (
    <div style={footerStyle}>
      <p style={paragraphStyle}>© 2023 Team BKTP Project</p>
    </div>
  );
};

export default Footer;
