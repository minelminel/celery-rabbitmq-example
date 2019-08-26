import json

def post_json(client, url, json_dict):
    ''' Send dictionary json_dict as a json to the specified url '''
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')

def de_json(response):
    ''' Decode json from response '''
    return json.loads(response.data.decode('utf-8'))
