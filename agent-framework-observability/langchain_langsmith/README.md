Very simple Langchain (with LEL) example that logs traces to Langsmith. No extra setup is required for langsmith beyond ensuring the following is present in .env:

```
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
```

It is also possible to add LANGSMITH_ENDPOINT and LANGSMITH_PROJECT. Without the project env var, the default is to use a project named "default". I'm not sure if LANGSMITH_ENDPOINT is really necessary, it's included in the config generator in the langsmith app but isn't mentioned by newer documentation.

More info on integrating langsmith into langchain apps at:

https://docs.smith.langchain.com/observability/how_to_guides/trace_with_langchain
https://python.langchain.com/v0.1/docs/langsmith/walkthrough/