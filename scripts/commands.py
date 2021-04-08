import click
from scripts.indexing import read_photos

@click.group()
def cli():
    pass

@cli.command()
@click.argument('ids_filename', type=click.Path(exists=True))
@click.argument('features_filename', type=click.Path(exists=True))
def index_precomputed(ids_filename, features_filename):
    read_photos(ids_filename, features_filename)

if __name__ == '__main__':
    cli()