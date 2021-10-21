const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const glob = require("glob");

module.exports = {
   entry: glob.sync('./assets/packs/**.js').reduce(function(obj, el){
     obj[path.parse(el).name] = el;
     return obj
   },{}),
   output: {
      filename: '[name].js',
      path: path.resolve(__dirname,'..', 'static'),
      clean: true,
   },
   module: {
      rules: [
         {
            test: /\.js$/,
            exclude: /node_modules/,
            use: {
               loader: 'babel-loader',
               options: {
                  presets: ['@babel/preset-env'],
               },
            },
         },
         {
            test: /\.css$/i,
            include: path.resolve(__dirname,'..', 'assets','style'),
            use: ['style-loader', 'css-loader', 'postcss-loader'],
         },
      ]
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