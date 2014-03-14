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
                order_line = self.prepare_order_line(
                    cr, uid, suggest_line, order, context
                )
                order_line_obj.create(cr, uid, order_line)
        return True

    def prepare_order_line(self, cr, uid, suggest_line, order, context=None):
        order_line_obj = self.pool.get('sale.order.line')
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
        return order_line

    def default_get(self, cr, uid, fields, context=None):
        res = super(sale_order_suggest, self).default_get(
            cr, uid, fields, context
        )
        if context.get('active_model') != 'sale.order':
            return res
        sale_order_id = context.get('active_id')
        order_obj = self.pool.get('sale.order')
        sale_order = order_obj.browse(cr, uid, sale_order_id, context)
        if not sale_order:
            return res
        res.update(self.prepare_suggest(cr, uid, sale_order))
        return res

    def prepare_suggest(self, cr, uid, sale_order):
        suggest = {
            'order_id': sale_order.id,
            'line_ids': [],
        }
        for line in sale_order.order_line:
            if not line.product_id:
                continue
            if not line.product_id.suggested_product_ids:
                continue
            for product_suggest in line.product_id.suggested_product_ids:
                order_has_product = self._sale_order_has_product(
                    sale_order, product_suggest.suggested_product_id.id
                )
                if order_has_product:
                    continue
                suggest_line = self.prepare_suggest_line(
                    cr, uid, product_suggest, line.product_uom_qty
                )
                suggest['line_ids'].append((0, 0, suggest_line))
        return suggest

    def _sale_order_has_product(self, sale_order, product_id):
        for line in sale_order.order_line:
            if line.product_id.id == product_id:
                return True
        return False

    def prepare_suggest_line(self, cr, uid, product_suggest, quantity):
        product_suggest_obj = self.pool.get('product.suggest')
        suggest_quantity = product_suggest_obj.get_quantity(
            cr, uid, product_suggest.id, quantity
        )
        return {
            'product_id': product_suggest.suggested_product_id.id,
            'quantity': suggest_quantity,
        }
