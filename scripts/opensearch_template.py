index_template = {
    "settings": {
        "index": {
            "knn": True,
        }
    },
    "mappings": {
        "dynamic": "strict",
        "dynamic_templates": [],
        "properties": {
            "url": {
                "type": "keyword",
            },
            "sourceUrl": {
                "type": "keyword",
            },
            "features": {
                "type": "knn_vector",
                "dimension": 512,
                "method": {
                    "name": "hnsw",
                    "space_type": "cosinesimil",
                    "engine": "nmslib",
                }
            },
            "@timestamp": {
                "type": "date"
            }
        }
    },
}
