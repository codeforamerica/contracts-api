import json
from contracts_api_test.unit.test_base import BaseTestCase
from contracts_api.api.models import Stage

class StagesResourceTest(BaseTestCase):
    def setUp(self):
        super(StagesResourceTest, self).setUp()

        # create fixture stages and flows
        self.stage = Stage.create(name='stage1').save()
        self.stage_url = '/api/v1/stage/{id}'.format(id=self.stage)

    render_templates = False

    def test_list_get(self):
        stages = json.loads(self.client.get('/api/v1/stages').data)
        self.assertEquals(stages['meta']['count'], 1)

    def test_detail_get(self):
        stage = json.loads(self.client.get(self.stage_url).data)
        self.assertEquals(stage['name'], 'stage1')
        self.assertEquals(type(stage), dict)

        bad_stage = self.client.get('/api/v1/stage/10000000')
        self.assertEquals(bad_stage.status_code, 404)

    def test_create(self):
        stage = self.client.post('/api/v1/stages', data=json.dumps({
            'name': 'stage2',
            'properties': [
                {'stage_property': 'DESCRIPTION_HERE'},
                {'stage_property': 'DESCRIPTION_HERE2'}
            ]
        }))
        self.assertEquals(stage.status_code, 201)
        self.assertEquals(json.loads(self.client.get('/api/v1/stages').data)['meta']['count'], 2)

        # a malformed property should cancel the whole transaction
        malformed_post = self.client.post('/api/v1/stages', data=json.dumps({
            'name': 'stage3',
            'properties': [{'stage_property': 'DESCRIPTION_HERE'}, {'malformed': None}]
        }))
        self.assertEquals(malformed_post.status_code, 400)
        self.assertEquals(json.loads(self.client.get('/api/v1/stages').data)['meta']['count'], 2)

        bad_data = self.client.post('/api/v1/stages', data=json.dumps([]))
        self.assertEquals(bad_data.status_code, 403)

    def test_update(self):
        self.client.put(self.stage_url, data=json.dumps({
            'name': 'stage2'
        }))
        self.assertEquals(json.loads(self.client.get(self.stage_url).data)['name'], 'stage2')

        malformed_name = self.client.put(self.stage_url, data=json.dumps({
            'name': None
        }))
        self.assertEquals(malformed_name.status_code, 400)

        self.client.put(self.stage_url, data=json.dumps({
            'properties': [
                {'stage_property': 'DESCRIPTION_HERE3'},
                {'stage_property': 'DESCRIPTION_HERE4'}
            ]
        }))

        new_props_properties = [i.get('stage_property') for i in json.loads(self.client.get(self.stage_url).data)['stage_properties']]
        # assert the new ones are there
        self.assertTrue('DESCRIPTION_HERE3' in new_props_properties)
        self.assertTrue('DESCRIPTION_HERE4' in new_props_properties)
        # assert the old ones aren't
        self.assertTrue('DESCRIPTION_HERE' not in new_props_properties)
        self.assertTrue('DESCRIPTION_HERE2' not in new_props_properties)

        bad_data = self.client.put(self.stage_url, data=json.dumps({
            'properties': [{'stage_property': ''}]
        }))
        self.assertEquals(bad_data.status_code, 400)


    def test_delete(self):
        stage = self.client.delete(self.stage_url)
        self.assertEquals(stage.status_code, 204)

        bad_stage = self.client.delete('/api/v1/stage/10000000')
        self.assertEquals(bad_stage.status_code, 404)
