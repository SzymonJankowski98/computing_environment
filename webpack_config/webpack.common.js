const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
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
            test: /\.(sa|sc|c)ss$/,
            include: path.resolve(__dirname,'..', 'assets','style'),
            use: [MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader', 'sass-loader'],
         },
      ]
   },
   optimization: {
      minimizer: [
         new CssMinimizerPlugin(),
         new TerserPlugin()
       ],
      splitChunks: {
         chunks: 'all',
         name: 'vendors',
      },
   },
   plugins: [
    new HtmlWebpackPlugin(),
    new MiniCssExtractPlugin()
  ],
};