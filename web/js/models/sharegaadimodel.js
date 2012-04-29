window.Sharegaadi = Backbone.Model.extend({

});

window.SharegaadiCollection = Backbone.Collection.extend({
	
	model:Sharegaadi,
	
	initialize:function(){
	    var self = this;
		$.getJSON('data/results.json',function (data) {
			
			setTimeout(function() {
				$.each(data.trips, function(i,trip){				
					self.add(new self.model({"source": trip.source,"destination": trip.destination}));			
				});
			}, 1000);
        });
	}
});