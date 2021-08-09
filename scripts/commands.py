import click
from scripts.indexing import ensure_index_exist, load_unsplash_photos_in_index, read_unsplash_photos
import os
from scripts.opensearch_template import index_template as opensearch_index_template


@click.group()
def cli():
    pass


@cli.command()
@click.option('--es_url', default=os.environ.get('ES_URL'))
@click.option('--index_name', default='images')
@click.option('--start', type=click.INT, default=None)
@click.option('--end', type=click.INT, default=None)
@click.argument('ids_filename', type=click.Path(exists=True))
@click.argument('features_filename', type=click.Path(exists=True))
def index_precomputed(ids_filename, features_filename, es_url, index_name, start, end):
    ensure_index_exist(es_url=es_url, index_name=index_name)
    ids, features = read_unsplash_photos(
        ids_filename=ids_filename, features_filename=features_filename)
    load_unsplash_photos_in_index(es_url=es_url, index_name=index_name,
                                  ids=ids[start:end], features=features[start:end])


@cli.command()
@click.option('--opensearch_url', default=os.environ.get('OPENSEARCH_URL'))
@click.option('--index_name', default='images')
def create_opensearch_index(opensearch_url, index_name):
    ensure_index_exist(es_url=opensearch_url, index_name=index_name,
                       index_template=opensearch_index_template)


@cli.command()
@click.option('--opensearch_url', default=os.environ.get('OPENSEARCH_URL'))
@click.option('--index_name', default='images')
@click.option('--start', type=click.INT, default=None)
@click.option('--end', type=click.INT, default=None)
@click.argument('ids_filename', type=click.Path(exists=True))
@click.argument('features_filename', type=click.Path(exists=True))
def index_unsplash_opensearch(ids_filename, features_filename, opensearch_url, index_name, start, end):
    ensure_index_exist(es_url=opensearch_url, index_name=index_name,
                       index_template=opensearch_index_template)
    ids, features = read_unsplash_photos(ids_filename=ids_filename,
                                         features_filename=features_filename)
    load_unsplash_photos_in_index(es_url=opensearch_url, index_name=index_name,
                                  ids=ids[start:end], features=features[start:end])


if __name__ == '__main__':
    cli()
