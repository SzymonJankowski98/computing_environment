var glob = require('glob');
const path = require('path');

module.exports = {
   entry: {
      index: './assets/javascript/index.js',
   },
   output: {
      filename: '[name].js',
      path: path.resolve(__dirname,'..', 'static'),
      clean: true,
   },
};