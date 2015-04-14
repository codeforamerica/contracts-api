import json
from contracts_api_test.unit.test_base import BaseTestCase
from contracts_api.api.models import Stage, Flow

class FlowsResourceTest(BaseTestCase):
    def setUp(self):
        super(FlowsResourceTest, self).setUp()

        # create fixture stages and flows
        Stage.create(name='stage1').save()
        Stage.create(name='stage2').save()
        self.flow = Flow.create(flow_name='flow1', stage_order=[1,2]).save()

    render_templates = False

    def test_list_get(self):
        flows = json.loads(self.client.get('/api/v1/flows').data)
        self.assertEquals(flows['meta']['count'], 1)

    def test_detail_get(self):
        flow = json.loads(self.client.get('/api/v1/flow/{id}'.format(id=self.flow)).data)
        self.assertEquals(flow['flow_name'], 'flow1')
        self.assertEquals(type(flow), dict)

        bad_flow = self.client.get('/api/v1/flow/10000000')
        self.assertEquals(bad_flow.status_code, 404)

    def test_create(self):
        # test good flow create
        flow = self.client.post('/api/v1/flows', data=json.dumps({
            'flow_name': 'flow2',
            'stage_order': [2,1]
        }))
        self.assertEquals(flow.status_code, 201)

        # test duplicate name
        dupe_flow = self.client.post('/api/v1/flows', data=json.dumps({
            'flow_name': 'flow2',
            'stage_order': []
        }))
        self.assertEquals(dupe_flow.status_code, 400)

        # test bad stages
        bad_stages = self.client.post('/api/v1/flows', data=json.dumps({
            'flow_name': 'flow3',
            'stage_order': [1, 2, 100, 101]
        }))
        self.assertEquals(bad_stages.status_code, 400)
        self.assertTrue('100, 101' in bad_stages.data)
        self.assertTrue('1, 2' not in bad_stages.data)

        # test bad data format
        bad_format = self.client.post('/api/v1/flows', data=json.dumps([]))
        self.assertEquals(bad_format.status_code, 403)

    def test_update(self):
        update_url = '/api/v1/flow/{id}'.format(id=self.flow)

        flow = self.client.put(update_url, data=json.dumps({
            'stage_order': [2,1]
        }))
        self.assertEquals(flow.status_code, 200)

        # test bad stages
        bad_stages = self.client.put(update_url, data=json.dumps({
            'stage_order': [100, 101]
        }))
        self.assertEquals(bad_stages.status_code, 400)

        # test 404 for bad stage id
        no_stage = self.client.put('/api/v1/flow/10000000')
        self.assertEquals(no_stage.status_code, 404)

    def test_delete(self):
        flow = self.client.delete('/api/v1/flow/{id}'.format(id=self.flow))
        self.assertEquals(flow.status_code, 204)

        bad_flow = self.client.delete('/api/v1/flow/10000000')
        self.assertEquals(bad_flow.status_code, 404)
