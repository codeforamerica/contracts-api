from contracts_api_test.unit.test_base import BaseTestCase

class ContractsResourceTest(BaseTestCase):
    render_templates = False
    def test_list_get(self):
        self.assertEquals(1,1)
