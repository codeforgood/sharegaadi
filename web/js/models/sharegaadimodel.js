window.Sharegaadi = Backbone.Model.extend({

    /*initialize:function () {
		 this.set({"source": "chennai","destination": "bangalore"});
		 this.set({"source": "chennai","destination": "delhi"});
    }*/

});

window.SharegaadiCollection = Backbone.Collection.extend({
	
	model:Sharegaadi,
	
	initialize:function(){
		this.add(new this.model({"source": "chennai","destination": "bangalore"}));
		this.add(new this.model({"source": "chennai","destination": "delhi"}));
	}
});