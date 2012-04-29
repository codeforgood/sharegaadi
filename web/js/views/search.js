window.searchView = Backbone.View.extend({
    
	initialize:function () {
        this.template = _.template(tpl.get('search'));
    },

    render:function (eventName) {
        $(this.el).html(this.template());
		this.searchresults=new SharegaadiCollection;
		$('#search_results', this.el).append(new SearchListView({model:this.searchresults}).render().el);
        return this;
    }

});