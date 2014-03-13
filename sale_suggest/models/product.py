from osv import osv, fields


class product_suggest(osv.Model):
    _name = 'product.suggest'
    _columns = {
        'product_id': fields.many2one('product.product', 'Product'),
        'suggested_product_id': fields.many2one(
            'product.product',
            'Suggested product'
        ),
        'ratio': fields.float('Ratio', digits=[2, 1]),
        'rounding': fields.selection(
            [('no', 'no'), ('up', 'up'), ('down', 'down')],
            'Rounding method'
        ),
    }


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
