function initialize() {
	var Chennai = new google.maps.LatLng(13.0604220, 80.2495830);
	var myOptions = {
	  center: Chennai,
	  zoom: 15,
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	
	var map = new google.maps.Map(document.getElementById("map_canvas"),
		myOptions);
}
	  	  
$(document).ready(function(){
	$('.dropdown-toggle').dropdown();							
});