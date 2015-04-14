import json
from contracts_api_test.unit.test_base import BaseTestCase
from contracts_api.api.models import Stage, Flow, Contract

class ContractsResourceTest(BaseTestCase):
    def setUp(self):
        super(ContractsResourceTest, self).setUp()

        # create fixture stages and flows
        Stage.create(name='stage1').save()
        Stage.create(name='stage2').save()
        Flow.create(flow_name='flow1', stage_order=[1,2]).save()
        self.contract = Contract.create(
            item_number='1', spec_number='2', department='foo',
            commodity_title='test', status_comments='none',
            flow_name='flow1', current_stage=1
        ).save()
        self.contract_url = '/api/v1/contract/{id}'.format(id=self.contract)

    render_templates = False

    def test_list_get(self):
        contracts = json.loads(self.client.get('/api/v1/contracts').data)
        self.assertEquals(contracts['meta']['count'], 1)
        self.assertEquals(contracts['results'][0]['item_number'], 1)

    def test_detail_get(self):
        contract = json.loads(self.client.get(self.contract_url).data)
        self.assertEquals(contract['item_number'], 1)
        self.assertEquals(type(contract), dict)

        no_contract = self.client.get('/api/v1/contract/100000')
        self.assertEquals(no_contract.status_code, 404)

    def test_create(self):
        post = self.client.post('/api/v1/contracts', data=json.dumps({
            'item_number': 2, 'spec_number': 2, 'department': 'foo',
            'commodity_title': 'test2', 'status_comments': 'none', 'flow_name': 'flow1',
            'current_stage': 1
        }))

        self.assertEquals(post.status_code, 201)
        self.assertEquals(json.loads(self.client.get('/api/v1/contracts').data)['meta']['count'], 2)

        # invalid stage number should raise errors
        post = self.client.post('/api/v1/contracts', data=json.dumps({
            'item_number': 2, 'spec_number': 2, 'department': 'foo',
            'commodity_title': 'test2', 'status_comments': 'none', 'flow_name': 'flow1',
            'current_stage': 10000000
        }))
        self.assertEquals(post.status_code, 400)

        # invalid flow name should raise errors
        post = self.client.post('/api/v1/contracts', data=json.dumps({
            'item_number': 2, 'spec_number': 2, 'department': 'foo',
            'commodity_title': 'test2', 'status_comments': 'none', 'flow_name': 'INVALIDFLOWNAME',
            'current_stage': 1
        }))
        self.assertEquals(post.status_code, 400)

        # junk request creates a 403
        post = self.client.post('/api/v1/contracts', data=json.dumps([]))
        self.assertEquals(post.status_code, 403)

    def test_update(self):
        put = self.client.put(self.contract_url, data=json.dumps({
            'current_stage': 2
        }))
        self.assertEquals(put.status_code, 200)
        self.assertEquals(json.loads(self.client.get(self.contract_url).data)['current_stage']['id'], 2)

        put = self.client.put('/api/v1/contract/1', data=json.dumps({
            'current_stage': 10000000
        }))
        self.assertEquals(put.status_code, 400)

        put = self.client.put(self.contract_url, data=json.dumps({
            'flow_name': 'SUPERINVALIDNAME'
        }))
        self.assertEquals(put.status_code, 400)

    def test_delete(self):
        delete = self.client.delete(self.contract_url)
        self.assertEquals(delete.status_code, 204)
        self.assertEquals(json.loads(self.client.get('/api/v1/contracts').data)['meta']['count'], 0)

        bad_delete = self.client.delete('/api/v1/contract/10000000')
        self.assertEquals(bad_delete.status_code, 404)
