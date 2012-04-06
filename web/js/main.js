var AppRouter = Backbone.Router.extend({

    routes:{
        "":"home",
		"about":"about",
		"search":"search",
		"contact":"contact",
		"subscribe" :"subscribe"
    },

    initialize:function () {
        this.headerView = new HeaderView();
        $('.header').html(this.headerView.render().el);
		$('.dropdown-toggle').dropdown();		
    },

    home:function () {
        if (!this.homeView) {
            this.homeView = new HomeView();
            this.homeView.render();
        }
        $('#content').html(this.homeView.el);		
    },
	
	about:function (){
		this.aboutView = new AboutView();
        $('#content').html(this.aboutView.render().el);
	},
	
	search:function (){
		this.searchView = new searchView();
        $('#content').html(this.searchView.render().el);
		initialize_map();	
	},

	contact:function (){
		this.contactView = new contactView();
        $('#content').html(this.contactView.render().el);
	},
	
	subscribe:function (){
		this.subscribeView = new subscribeView();
        $('#content').html(this.subscribeView.render().el);
	}

});

function initialize_map() {	
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
		  addMarker(initialLocation);
		}, function() {
		  map.setCenter(initialLocation);
		});
	}else {
		map.setCenter(initialLocation);
	}
	
	function addMarker(location) {
		var marker = new google.maps.Marker({
			position: location,
			map: map,
			animation: google.maps.Animation.DROP,
			title:"We got you"
		  });		
	}
}
	  	  
$(document).ready(function(){
	
	tpl.loadTemplates(['home', 'header','about', 'search', 'contact', 'subscribe', 'search_result_item'],
		function () {
			app = new AppRouter();
			Backbone.history.start();
		});		
});