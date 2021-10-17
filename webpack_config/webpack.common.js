const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const glob = require("glob");

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
   entry: glob.sync('./assets/packs/**.js').reduce(function(obj, el){
     obj[path.parse(el).name] = el;
     return obj
  },{}),
   output: {
      filename: '[name].js',
      path: path.resolve(__dirname,'..', 'static'),
      clean: true,
   },
   optimization: {
      splitChunks: {
         chunks: 'all',
         name: 'vendors',
      },
   },
   plugins: [
    new HtmlWebpackPlugin()
  ],
};