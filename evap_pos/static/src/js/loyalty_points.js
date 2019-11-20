odoo.define("evap_pos.loyalty_points", function(require) {
    'use strict';

    var models = require('point_of_sale.models');
    var _super = models.Order;

    var round_pr = require('web.utils').round_precision;

    require('pos_loyalty.pos_loyalty');

    models.load_fields('res.partner', 'has_no_loyalty_points');

    models.Order = models.Order.extend({
        /**
         * if partner has `has_no_loyalty_points` ticked, s/he can't have the benefit of Loyalty Program.
         * Thus, Loyalty Points needs to be 0.0
         */
        get_won_points: function() {
            // This method is overridden in order to subtract the loyalty points from `Reward` products and calulate the
            // won points. Also return only 5% of won points.

            if (!this.pos.loyalty || !this.get_client() || this.get_client().has_no_loyalty_points) {
                return 0;
            }

            var orderLines = this.get_orderlines();
            var rounding = this.pos.loyalty.rounding;

            var product_sold = 0;
            var total_sold = 0;
            var total_points = 0;

            for (var i = 0; i < orderLines.length; i++) {
                var line = orderLines[i];
                var product = line.get_product();
                var rules = this.pos.loyalty.rules_by_product_id[product.id] || [];
                var overriden = false;

                /*
                    This is the default code, which ignores rewarded products.

                    if (line.get_reward()) {  // Reward products are ignored
                        continue;
                    }
                */

                for (var j = 0; j < rules.length; j++) {
                    var rule = rules[j];
                    var qty_amount = round_pr(line.get_quantity() * rule.pp_product, rounding);
                    var tax_amount = round_pr(line.get_price_with_tax() * rule.pp_currency, rounding);
                    total_points += (qty_amount + tax_amount);

                    /*
                        if customer has used rewarded product then subtract it from the total won points; in order to count
                        won points based on Total and not the Line Amount.
                    */

                    // In default code, rewarded products are ignored.

                    if (line.get_reward()) {
                        total_points -= (qty_amount + tax_amount);
                    }

                    // if affected by a non cumulative rule, skip the others. (non cumulative rules are put
                    // at the beginning of the list when they are loaded )
                    if (!rule.cumulative) {
                        overriden = true;
                        break;
                    }
                }

                // Test the category rules
                if (product.pos_categ_id) {
                    var category = this.pos.db.get_category_by_id(product.pos_categ_id[0]);
                    while (category && !overriden) {
                        var rules = this.pos.loyalty.rules_by_category_id[category.id] || [];
                        for (var j = 0; j < rules.length; j++) {
                            var rule = rules[j];
                            var qty_amount = round_pr(line.get_quantity() * rule.pp_product, rounding);
                            var tax_amount = round_pr(line.get_price_with_tax() * rule.pp_currency, rounding);
                            var amount = qty_amount + tax_amount;
                            total_points += amount;

                            if (line.get_reward())  total_points -= amount;

                            if (!rule.cumulative) {
                                overriden = true;
                                break;
                            }
                        }

                        var _category = category;
                        category = this.pos.db.get_category_by_id(this.pos.db.get_category_parent_id(category.id));
                        if (_category === category) {
                            break;
                        }
                    }
                }

                if (!overriden) {
                    product_sold += line.get_quantity();
                    total_sold += line.get_price_with_tax();
                }
            }

            total_points += round_pr(total_sold * this.pos.loyalty.pp_currency, rounding);
            total_points += round_pr(product_sold * this.pos.loyalty.pp_product, rounding);
            total_points += round_pr(this.pos.loyalty.pp_order, rounding);

            return total_points;
        }
    });
});
