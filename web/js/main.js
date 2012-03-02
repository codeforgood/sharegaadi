function initialize() {	
	var Chennai = new google.maps.LatLng(13.0604220, 80.2495830);
	var initialLocation = Chennai;
	
	var myOptions = {
	  zoom: 15,
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	
	var map = new google.maps.Map(document.getElementById("map_canvas"),
		myOptions);	
	
	if(navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function(position) {
		  initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
		  map.setCenter(initialLocation);
		}, function() {
		  map.setCenter(initialLocation);
		});
	}else {
		map.setCenter(initialLocation);
	}
}
	  	  
$(document).ready(function(){
	$('.dropdown-toggle').dropdown();							
});