const { defineConfig } = require("@vue/cli-service");
const fs = require("fs");

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    entry: "./src/main.js",
    devServer: {
      hot: true,
      port: 8025,
      host: "0.0.0.0", // Binding to 0.0.0.0 allows access from external addresses.
      headers: {
        "Access-Control-Allow-Origin": "*",
      },
      allowedHosts: ["maris.com", "localhost", "0.0.0.0"],
      https: {
        key: fs.readFileSync("./ssl/key.pem"),
        cert: fs.readFileSync("./ssl/cert.pem"),
      },
    },
    watchOptions: {
      ignored: /node_modules/,
      poll: 1000,
    },
  },
  pwa: {
    manifestOptions: {
      name: 'Truck App',
      short_name: 'TruckAPP',
      theme_color: "#4DBA87",
      background_color: "#000000",
      display: "standalone",
      icons: [
        {
        src: "./src/static_images/logo.png",
        sizes: "512x512",  // you can specify the sizes you have
        type: "image/png",  // the type of the image
        },
      ],
    },
  },
});
