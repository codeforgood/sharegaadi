window.SearchListView = Backbone.View.extend({

    tagName:'ul',

    className:'nav nav-list',

    render:function (eventName) {
        $(this.el).empty();
        _.each(this.model.models, function (sharegaadi) {
            $(this.el).append(new SearchListItemView({model:sharegaadi}).render().el);
        }, this);
        return this;
    }
});

window.SearchListItemView = Backbone.View.extend({

    tagName:"li",

    initialize:function () {
        this.template = _.template(tpl.get('search_result_item'));
        this.model.bind("change", this.render, this);
        this.model.bind("destroy", this.close, this);
    },

    render:function (eventName) {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }

});