'use strict';

(function() {
	requirejs(['react', 'react-dom'], function(React, ReactDOM) {
		let initialize = function() {
			document.querySelector(".submit_button").addEventListener('mousedown', e => {
				e.currentTarget.style.backgroundColor = "#000000";
			});

			document.querySelector(".submit_button").addEventListener('click', e => {
				let request = new XMLHttpRequest();

				request.onreadystatechange = function() {
					if (this.readyState == 4 && this.status == 200) {
						let json_data = JSON.parse(request.responseText);
						window.location.replace(json_data.authorize_uri);
					}
				};
				
				request.open("POST", "/get_authorize_app_uri", true);
				request.send();
				e.currentTarget.style.backgroundColor = "#ffeeff";
			});
		};

		if (document.readyState === "complete" || (document.readyState !== "loading" && !document.documentElement.doScroll)) {
			initialize();
		} else {
			document.addEventListener("DOMContentLoaded", initialize);
		}
	});
})();