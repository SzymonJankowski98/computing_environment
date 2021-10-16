const path = require('path');

module.exports = {
   module: {
      rules: [
         {
            test: /\.js$/,
            exclude: /node_modules/,
            use: ["babel-loader"]
         }
      ]
   },
   entry: {
      index: './assets/javascript/index.js',
   },
   output: {
      filename: '[name].js',
      path: path.resolve(__dirname,'..', 'static'),
      clean: true,
   },
};