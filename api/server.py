from sanic import Sanic
from sanic.log import logger
from sanic.response import json
import torch
import os
import clip
from elasticsearch import AsyncElasticsearch

app = Sanic("image-search-api")

device = "cuda" if torch.cuda.is_available() else "cpu"

model_name = os.environ['CLIP_MODEL_NAME']

logger.info('Loading clip model...')
model, preprocess = clip.load(model_name, device=device)
logger.info('done.')

index_name = os.environ.get('INDEX_NAME', 'photos')

es = AsyncElasticsearch([os.environ.get('ES_URL')])


def encode_query(query: str):
    with torch.no_grad():
        # Encode and normalize the search query using CLIP
        text_encoded = model.encode_text(clip.tokenize(query).to(device))
        text_encoded /= text_encoded.norm(dim=-1, keepdim=True)
        return text_encoded.tolist()[0]


@app.get("/")
async def hello_world(request):
    text_features = encode_query("dogs playing the snow")
    resp = await es.search(
        index=index_name,
        body={
            "query": {
                "bool": {
                    "should": [
                        {
                            "script_score": {
                                "query": {"match_all": {}},
                                "script": {
                                    "source":
                                    "cosineSimilarity(params.text_features, 'features')",
                                    "params": {"text_features": text_features},
                                },
                            },
                        },

                    ],
                }
            },
            "_source": False
        },
        size=20,
        request_timeout=100
    )
    return json(resp)
