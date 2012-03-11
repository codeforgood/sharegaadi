window.AboutView = Backbone.View.extend({

    initialize:function () {
        this.template = _.template(tpl.get('about'));
    },

    render:function (eventName) {
        $(this.el).html(this.template());
        return this;
    }

});