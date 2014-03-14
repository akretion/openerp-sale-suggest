from osv import osv, fields


class sale_order_suggest_line(osv.TransientModel):
    _name = 'sale.order.suggest.line'
    _columns = {
        'product_id': fields.many2one('product.product', 'Product'),
        'quantity': fields.integer('Quantity')
    }


class sale_order_suggest(osv.TransientModel):
    _name = 'sale.order.suggest'
    _columns = {
        'line_ids': fields.one2many('sale.order.suggest.line', 'product_id'),
        'order_id': fields.many2one('sale.order'),
    }

    def add_suggestions(self, cr, uid, ids, context=None):
	return True
