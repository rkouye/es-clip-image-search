import click
from scripts.indexing import ensure_index_exist, load_photos_in_index, read_photos
import os


@click.group()
def cli():
    pass


@cli.command()
@click.option('--es_url', default=os.environ.get('ES_URL'))
@click.option('--index_name', default='photos')
@click.option('--start', type=click.INT, default=None)
@click.option('--end', type=click.INT, default=None)
@click.argument('ids_filename', type=click.Path(exists=True))
@click.argument('features_filename', type=click.Path(exists=True))
def index_precomputed(ids_filename, features_filename, es_url, index_name, start, end):
    ids, features = read_photos(
        ids_filename=ids_filename, features_filename=features_filename)
    load_photos_in_index(es_url=es_url, index_name=index_name,
                         ids=ids[start:end], features=features[start:end])


if __name__ == '__main__':
    cli()
