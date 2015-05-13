import requests
import json

def get_descriptions(base_64_file_location, host, idx):
    query = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "file_location": {
                            "query": base_64_file_location
                        }
                    }
                }
            }
        }
    }
    es_query = json.dumps(query)
    uri = host + '/' + idx + '/_search'
    response = requests.post(uri, data=es_query)
    results = json.loads(response.text)

    skills = []
    try:
        skills = results['hits']['hits'][0]['_source']['full_text']
    except Exception:

        return skills

    return skills
