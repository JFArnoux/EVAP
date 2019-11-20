odoo.define("evap_pos.product_list_view", function(require) {
    "use strict";

    var ProductListWidget = require('point_of_sale.screens').ProductListWidget;
    var QWeb = require('web.core').qweb;

    ProductListWidget.include({
        render_product: function(product) {
            var current_pricelist = this._get_active_pricelist();
            var cache_key = this.calculate_cache_key(product, current_pricelist);
            var cached = this.product_cache.get_node(cache_key);
            if (!cached) {
                var image_url = this.get_product_image_url(product);
                var product_html = QWeb.render('Product', {
                    widget: this,
                    product: product,
                    pricelist: current_pricelist,
                });
                var product_node = document.createElement('div');
                $(product_html).appendTo(product_node)
                product_node = product_node.childNodes[0];
                this.product_cache.cache_node(cache_key, product_node);
                return product_node;
            }
            return cached;
        },
    });
});
