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
            'target': 'new',
        }

