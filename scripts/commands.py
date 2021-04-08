import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('ids_filename', type=click.Path(exists=True))
@click.argument('features_filename', type=click.Path(exists=True))
def index_precomputed(ids_filename, features_filename):
    click.echo(click.format_filename(ids_filename))
    click.echo(click.format_filename(features_filename))

if __name__ == '__main__':
    cli()