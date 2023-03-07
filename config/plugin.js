'use strict';

/** @type Egg.EggPlugin */
const nunjucks = {
  enable: true,
  package: 'egg-view-nunjucks'
};
const io = {
  enable: true,
  package: 'egg-socket.io',
};


const cors = {
  enable: true,
  package: 'egg-cors',
};

const jwt={
  enable: true,
  package: 'egg-jwt',
};



module.exports = { nunjucks, io, cors, jwt};
