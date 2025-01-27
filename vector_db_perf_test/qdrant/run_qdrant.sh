docker pull qdrant/qdrant
docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_db:/qdrant/storage:z" \
    qdrant/qdrant