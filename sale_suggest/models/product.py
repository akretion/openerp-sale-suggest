from osv import osv, fields


class product_suggest(osv.Model):
    _name = 'product.suggest'
    _columns = {
        'product_id': fields.many2one(
            'product.product', 'Product', required=True
        ),
        'suggested_product_id': fields.many2one(
            'product.product',
            'Suggested product',
            required=True,
        ),
        'ratio': fields.float('Ratio', digits=[12, 3]),
        'rounding': fields.selection(
            [('no', 'no'), ('up', 'up'), ('down', 'down')],
            'Rounding method'
        ),
    }

    _defaults = {
        'rounding': 'no',
        'ratio': 1,
    }

    def get_quantity(self, cr, uid, id, product_quantity, context=None):
        if hasattr(id, '__iter__'):
            assert len(id) == 1
            id = id[0]
        product_suggest = self.browse(cr, uid, id, context)
        quantity = product_quantity * product_suggest.ratio
        rounded = round(quantity)
        if rounded == quantity or product_suggest.rounding == 'no':
            return quantity
        if product_suggest.rounding == 'up':
            return round(quantity + 0.5)
        return round(quantity - 0.5)


class product_product(osv.Model):
    _inherit = 'product.product'
    _columns = {
        'suggested_product_ids': fields.one2many(
            'product.suggest',
            'product_id',
            'Suggested products'
        ),
        'suggested_for_product_ids': fields.one2many(
            'product.suggest',
            'suggested_product_id',
            'Suggest this product with'
        ),
    }
