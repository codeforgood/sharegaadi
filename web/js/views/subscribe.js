window.subscribeView = Backbone.View.extend({

    initialize:function () {
        this.template = _.template(tpl.get('subscribe'));
    },

    render:function (eventName) {
        $(this.el).html(this.template());
        return this;
    }

});