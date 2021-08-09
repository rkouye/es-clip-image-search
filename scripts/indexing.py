import pandas as pd
import numpy as np
import datetime
from elasticsearch import Elasticsearch, helpers
import click


def read_unsplash_photos(ids_filename: str, features_filename: str):
    print('Loading files...', end=' ', flush=True)
    ids = pd.read_csv(ids_filename)
    features = np.load(features_filename)
    print('✅', flush=True)
    return ids, features


def ensure_index_exist(es_url: str, index_name: str, index_template: dict):
    es = Elasticsearch([es_url])
    index_exist = es.indices.exists(index=index_name)
    if index_exist:
        print(f'Index {index_name} already exist')
    else:
        es.indices.create(index=index_name, body=index_template)
        print(f'Index {index_name} created')


def load_unsplash_photos_in_index(ids, features, es_url, index_name):
    es = Elasticsearch([es_url], timeout=400,
                       max_retries=10, retry_on_timeout=True)
    now = datetime.datetime.utcnow()
    length = len(ids)
    actions = ({
        "_id": f"https://unsplash.com/photos/{id}/",
        "_index": index_name,
        "sourceUrl": f"https://unsplash.com/photos/{id}/",
        "url": f"https://unsplash.com/photos/{id}/download",
        "features": features,
        "@timestamp": now
    } for id, features in zip(ids['photo_id'], features))

    loading = helpers.streaming_bulk(
        client=es,
        actions=actions,
        max_retries=5
    )
    print(f'Loading {length} photos...', flush=True)
    with click.progressbar(loading, length=length) as task:
        for success, info in task:
            if not success:
                print('A document failed:', info)

    print('Loaded photos')
