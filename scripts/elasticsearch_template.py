index_template = {
    "mappings": {
        "dynamic": "strict",
        "dynamic_templates": [],
        "properties": {
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
