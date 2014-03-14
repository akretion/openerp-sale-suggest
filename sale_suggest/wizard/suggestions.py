from osv import osv, fields


class sale_order_suggest_line(osv.TransientModel):
    _name = 'sale.order.suggest.line'
    _columns = {
        'suggest_id': fields.many2one('sale.order.suggest', select=True),
        'product_id': fields.many2one('product.product', 'Product'),
        'quantity': fields.integer('Quantity')
    }


class sale_order_suggest(osv.TransientModel):
    _name = 'sale.order.suggest'
    _columns = {
        'line_ids': fields.one2many('sale.order.suggest.line', 'suggest_id'),
        'order_id': fields.many2one('sale.order'),
    }

    def add_suggestions(self, cr, uid, ids, context=None):
        order_line_obj = self.pool.get('sale.order.line')
        suggests = self.browse(cr, uid, ids, context)
        for suggest in suggests:
            order = suggest.order_id
            for suggest_line in suggest.line_ids:
                order_line = order_line_obj.product_id_change(
                    cr,
                    uid,
                    [],
                    order.pricelist_id.id,
                    suggest_line.product_id.id,
                    suggest_line.quantity,
                    False,
                    suggest_line.quantity,
                    False,
                    '',
                    order.partner_id.id,
                    False,
                    True,
                    order.date_order,
                    False,
                    order.fiscal_position.id,
                    False,
                    context
                ).get('value')
                order_line['product_id'] = suggest_line.product_id.id
                order_line['product_uom_qty'] = suggest_line.quantity
                order_line['order_id'] = order.id
                order_line_obj.create(cr, uid, order_line)
                
        return True

    def default_get(self, cr, uid, fields, context=None):
        res = super(sale_order_suggest, self).default_get(
            cr, uid, fields, context
        )
        sale_order_id = context.get('active_id')
        order_obj = self.pool.get('sale.order')
        sale_order = order_obj.browse(cr, uid, sale_order_id, context)
        if not sale_order:
            return res
        res.update({
            'order_id': sale_order_id,
            'line_ids': [],
        })
        for line in sale_order.order_line:
            if not line.product_id:
                continue
            if not line.product_id.suggested_product_ids:
                continue
            for product_suggest in line.product_id.suggested_product_ids:
                quantity = line.product_uom_qty * product_suggest.ratio
                rounded = round(quantity)
                if rounded != quantity:
                    quantity = rounded + 1
                res['line_ids'].append((0, 0, {
                    'product_id': product_suggest.suggested_product_id.id,
                    'quantity': quantity,
                }))
        return res
