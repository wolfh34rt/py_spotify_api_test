const path = require("path");

var base_config = {
	watch: true
	entry: {
		index: "./src/js/index.js",
		rainbow_sort_album_data: "./src/js/rainbow_sort_album_data.js"
	},
	output: {
		path: path.resolve("./dist/js"),
		filename: "[name].js",
	},
	module: {
		rules: [
		{
			test: /\.css$/,
			use: [
				{ loader: "style-loader" },
				{ loader: "css-loader" },
				{ loader: "less-loader" }
			]
		},
		{
			test: /\.m?js$/,
			exclude: /(node_modules|bower_components)/,
			use: { 
					loader: "babel-loader",
					options: {
						presets: ["@babel/preset-env"],
						plugins: ["@babel/plugin-proposal-object-rest-spread"]
				}
			}
		}]
	}
}

module.exports = base_config;
