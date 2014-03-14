from openerp.tests.common import TransactionCase


class TestProduct(TransactionCase):
    def _get_record(self, str_id):
        cr, uid = self.cr, self.uid

        model, int_id = self.registry('ir.model.data').get_object_reference(
            cr, uid, 'sale_suggest', str_id
        )
        return self.registry(model).browse(cr, uid, int_id)

    def test_get_quantity_no(self):
        suggest = self._get_record('suggest_no')
        quantity = suggest.get_quantity(3)
        self.assertEquals(quantity, 4.5)

    def test_get_quantity_up(self):
        suggest = self._get_record('suggest_up')
        quantity = suggest.get_quantity(4)
        self.assertEquals(quantity, 3.0)

    def test_get_quantity_down(self):
        suggest = self._get_record('suggest_down')
        quantity = suggest.get_quantity(4)
        self.assertEquals(quantity, 0.0)
