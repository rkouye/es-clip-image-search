import pandas as pd
import numpy as np
import datetime
from elasticsearch import Elasticsearch, helpers
from scripts.template import index_template
import click


def read_photos(ids_filename: str, features_filename: str):
    print('Loading files...', end=' ')
    ids = pd.read_csv(ids_filename)
    features = np.load(features_filename)
    print('✅')
    return ids, features


def ensure_index_exist(es_url: str, index_name: str):
    es = Elasticsearch([es_url])
    index_exist = es.indices.exists(index=index_name)
    if index_exist:
        print('Index exist')
    else:
        print('Index doesn\'t exist')
        es.indices.create(index=index_name, body=index_template)
        print('Index created')


def load_photos_in_index(ids, features, es_url, index_name):
    es = Elasticsearch([es_url])
    now = datetime.datetime.utcnow()
    actions = ({
        "_id": id,
        "_index": index_name,
        "features": features,
        "@timestamp": now
    } for id, features in zip(ids['photo_id'], features))

    loading = helpers.parallel_bulk(client=es, actions=actions)
    print('Loading photos...')
    with click.progressbar(loading) as task:
        for success, info in task:
            if not success:
                print('A document failed:', info)

    print('Loaded photos')
