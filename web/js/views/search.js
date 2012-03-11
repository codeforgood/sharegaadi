window.searchView = Backbone.View.extend({

    initialize:function () {
        this.template = _.template(tpl.get('search'));
    },

    render:function (eventName) {
        $(this.el).html(this.template());
        return this;
    }

});