index_template = {
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
                "type": "dense_vector",
                "dims": 512
            },
            "@timestamp": {
                "type": "date"
            }
        }
    },
}
