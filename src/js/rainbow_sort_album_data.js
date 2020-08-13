'use strict';

(function() {
	requirejs(['react', 'react-dom'], function(React, ReactDOM) {
		let initialize = function() {
			let request = new XMLHttpRequest();
			let album_grid = document.querySelector(".album_grid");

			request.onreadystatechange = function() {
				if (this.readyState == 4 && this.status == 200) {
					const json_data = JSON.parse(request.responseText);
					const album_data = JSON.parse(json_data.data);
					let album_grid_container = React.createElement("div",{"className": "grid_container"},
						React.createElement("div",{"className": "album_grid_root"},
							album_data.map(
								(album_data, i) => React.createElement("div",{"className":"saved_album_name","key":i},
									React.createElement("img",{"className":"image","src": album_data.album.image_url} ),
									React.createElement("div",{"className":"artist_name"},"artist_name: " + album_data.album.artist_name),
									React.createElement("div",{"className":"artist_url"},"artist_url: " + album_data.album.artist_url),
									React.createElement("div",{"className":"album_name"},"album_name: " + album_data.album.album_name),
									React.createElement("div",{"className":"dominant_colour"},"dominant_colour: " + album_data.album.dominant_colour),
									React.createElement("br",null,null)
								)
							)
						)
					);

					ReactDOM.render(album_grid_container, album_grid);
				}
			};
			
			request.open("POST", "/get_saved_albums", true);
			request.send();
		};

		if (document.readyState === "complete" || (document.readyState !== "loading" && !document.documentElement.doScroll)) {
			initialize();
		} else {
			document.addEventListener("DOMContentLoaded", initialize);
		}
	});
})();