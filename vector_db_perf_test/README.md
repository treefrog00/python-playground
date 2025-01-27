performance investigation of ingesting documents into a vector database for a local application (i.e. no cloud, no clusters, etc)

Featuring:
==========

Chroma
-> currently running entirely within the Python ingestion process (chunking, vectorization, any index building, etc), though can also be run in client-server mode
-> possibly automatically builds an index during ingestion?
-> core engine in Python

qdrant:
-> run in a docker container, but embedding is done in the Python ingestion process
-> indexing is I think dependent on what the optimizer decides, and will quite possibly be run on a background task by qdrant anyway, which isn't measured
-> core engine in Rust

weaviate
-> configured to run separate contains for both the db and a transformers vectorizer via docker-compose, so only the chunking and API calls are in the Python ingestion process. Haven't looked into how it handles indexes either.
-> core engine in Go

sqlite-vec
-> runs everything in the Python ingestion process
-> at the time of writing doesn't support indexing for vectors
-> currently has persistence entirely disabled
-> core engine is in C

vectorization only:
-> runs chunking and vectorization in the Python ingestion process, then discards the result

Not yet featured even though they are available as local dbs: milvus, pgvector

All are are configured to use the ONNX version of all-MiniLM-L6-v2 (384D) on CPU, though I still need to double check that exactly the same model and runtime is definitely being used in all cases.

Results
=======

Currently just one single run of each, plus sometimes I was using my computer for other things:

Chroma:

Ingest duration poem.txt: 0.35262107849121094 seconds
Ingest duration complete_shakespeare.txt: 114.04281854629517 seconds

Qdrant:

Ingest duration documents/poem.txt: 0.03750181198120117 seconds
Ingest duration documents/complete_shakespeare.txt: 45.048046588897705 seconds

sqlite-vec:

Ingest duration documents/poem.txt: 0.03622937202453613 seconds
Ingest duration documents/complete_shakespeare.txt: 48.0281662940979 seconds

Only vectorization:
Ingest duration documents/poem.txt: 0.09737586975097656 seconds
Ingest duration documents/complete_shakespeare.txt: 48.0729079246521 seconds

Weaviate:

Decided not to bother running the test for Weaviate because by this point I'd realized that

a) the main bottlneck is vectorization, which doesn't depend on the db
b) different dbs have different defaults as to whether or not they build an index, and in many cases index building will in any case happen asynchronously
c) Weaviate looks like the least sensible option for a local application anyway, it's very much designed to be run as a cloud service, maybe even more so than qdrant

More notes on the choice of embedding model
===========================================

ONNX version of all-MiniLM-L6-v2 (384D) on CPU

There are actually multiple ONNX versions of this model ('onnx/model.onnx', 'onnx/model_O1.onnx', 'onnx/model_O2.onnx', 'onnx/model_O3.onnx', 'onnx/model_O4.onnx', 'onnx/model_qint8_arm64.onnx', 'onnx/model_qint8_avx512.onnx', 'onnx/model_qint8_avx512_vnni.onnx', 'onnx/model_quint8_avx2.onnx'). I assume that by default all 3 of chroma/qdrant/weaviate default to the first of these, but maybe not...

In Chroma all-MiniLM-L6-v2 is the default vectorizer used by the Python library, batteries included...

In Weaviate the vectorizer is configured in docker-compose.yml

The default used by the Weaviate docs is ollama, and if you select sentence transformers in their configurator then the default is sentence-transformers/multi-qa-MiniLM-L6-cos-v1 (English, 384d):
https://weaviate.io/developers/weaviate/installation/docker-compose#configurator
https://weaviate.io/developers/weaviate/model-providers/transformers/embeddings
https://weaviate.io/developers/weaviate/quickstart/local

In qdrant the model is loaded and run using sentence-transformers in hello.py. Their introductory tutorial uses MiniLM-L6-v2 (384D, like Chroma, but it looks like they use the pytorch version instead of onnx:
https://qdrant.tech/documentation/beginner-tutorials/search-beginners/#

The sqlite-vec version also uses sentence-transformers for vectorization

So too does the vectorization only version

Other things:
=============

* No comparison is made of query performance, which in any case would depend heavily on how persistence and indexing are configured.

* This project is split into separate Python projects, which is due to the weaviate and qdrant Python packages having incompatible dependencies. The shared package and documents are awkwardly symlinked.
