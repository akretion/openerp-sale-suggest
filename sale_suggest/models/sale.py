from osv import osv, fields


class sale_order(osv.Model):
    _inherit = 'sale.order'

    def _suggestions_form_view_id(self, cr, uid):
        data_obj = self.pool.get('ir.model.data')
        _, view_id = data_obj.get_object_reference(
            cr, uid, 'sale_suggest', 'sale_order_suggest_form'
        )
        return view_id

    def make_suggestions(self, cr, uid, ids, context=None):
        res_id = self._prepare_suggestion(cr, uid, ids, context)
        suggest = self.pool.get('sale.order.suggest').browse(cr, uid, res_id)
        if context is None:
            context = {}
        return {
            'type': 'ir.actions.act_window',
            'name': 'Suggestions',
            'view_id': self._suggestions_form_view_id(cr, uid),
            'view_mode': 'form',
            'context': context,
            'domain' : [],
            'res_model': 'sale.order.suggest',
            'res_id': res_id,
            'target': 'new',
        }

    def _prepare_suggestion(self, cr, uid, ids, context=None):
        assert len(ids) == 1
        sale_order = self.browse(cr, uid, ids[0], context)
        suggest = {
            'order_id': ids[0],
            'line_ids': [],
        }
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
                suggest['line_ids'].append((0, 0, {
                    'product_id': 40, #product_suggest.suggested_product_id.id,
                    'quantity': 69,
                }))
        suggest_obj = self.pool.get('sale.order.suggest')
        suggest_id = suggest_obj.create(cr, uid, suggest, context)
        print suggest_id
        return suggest_id
