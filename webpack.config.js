const webpack = require('webpack');
const path = require('path');

module.exports = {
  devtool: 'eval-source-map',
  entry: "./public/js/index.js",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "public")
  },
  mode: "development",

  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              ['@babel/preset-env', {
                useBuiltIns: 'entry',
                modules: false,
                targets: [
                  'last 2 firefox versions',
                  'last 2 chrome versions',
                  'last 2 edge versions',
                  'last 2 ios versions',
                ],
                exclude: ["transform-regenerator"]
              }]
            ]
          }
        }
      }
    ]
  },
  plugins: [
    new webpack.ProvidePlugin({
      process: 'process/browser',
    }),
  ]
}