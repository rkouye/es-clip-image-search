# helios

Sample implementation of natural language image search with OpenAI's [CLIP](https://github.com/openai/CLIP) and [Elasticsearch](https://github.com/elastic/elasticsearch) or [OpenSearch](https://github.com/opensearch-project/OpenSearch).

[🌞 Try it](https://helios-app.vercel.app/)

![Demo](demo.png)

Inspired by https://github.com/haltakov/natural-language-image-search.

The goal is to build a web interface to index and search images with natural language.

The demo use [Unsplash Dataset](https://unsplash.com/data), but you are not limited to it.

## Guide: OpenSearch

### 1- Launch the services

Make sure you have the latest version of [docker](https://www.docker.com/) installed. Then run :

```bash
docker-compose --profile opensearch --profile backend --profile frontend up
```

It will launch the following services:

- [OpenSearch](http://localhost:9200)
- [OpenSearch Dashboards](http://localhost:5601)
- [The search backend](http://localhost:8000)
- [The search frontend](http://localhost:3000?db=opensearch)

By default, opensearch credentials are `admin:admin`.

### 2- Create the index

Next step is to create the index. The template used is defined in [/scripts/opensearch_template.py](./scripts/opensearch_template.py).

We use Approximate k-NN search because we expect a high number of images (+1M). Run the helper script:

```bash
docker-compose run --rm  scripts create-opensearch-index
```

It will create an index named `images`.

### 3 - Optional: Load unsplash dataset

To be searchable, images need to be embedded with CLIP and indexed.

If you want to try it on the [Unsplash Dataset](https://unsplash.com/data), you can compute the features [as done here](https://github.com/haltakov/natural-language-image-search#on-your-machine).
You can also use the [pre-computed features](https://drive.google.com/drive/folders/1WQmedVCDIQKA2R33dkS1f980YsJXRZ-q?usp=sharing), courtesy of [@haltakov](https://github.com/haltakov).

**In both cases, you need the permission of Unsplash.**

You should have two files:

- A csv file with photos ids, let name it `photo_ids.csv`
- A npy file with the features, let name it `features.npy`

Move them to the `/data` folder, so the docker container used to run scripts can access them.

Use the helper script to index the images. For example:

```bash
docker-compose run --rm  scripts index-unsplash-opensearch --start 0 --end 10000 /data/photo_ids.csv /data/features.npy
```

Will index the ids from 0 to 10000.

### 4 - Launch the search

After indexing, you can search for images in the frontend.

The frontend is a simple Next.js app, that send search queries to the backend.

The backend is a python app, that embed search queries with CLIP and send an approximate k-nn request to the OpenSearch service.

The sources code are in the `app` and `api` folders.

## Guide: Elasticsearch (TODO) 🚧
