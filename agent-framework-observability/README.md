# Experimenting with agentic AI frameworks and observability services

### Global local setup:

install uv

install direnv:

https://github.com/direnv/direnv/blob/master/docs/installation.md

add direnv hook:

https://github.com/direnv/direnv/blob/master/docs/hook.md

The models are currently configured to use Google Gemini, using auth via

```
gcloud auth application-default login
```

Each project has its own uv Python project and venv, with common files in the `common` package added via a symlink in each folder.

## The agentic frameworks and their observability tools:

There are many LLM observability services, and they are usually built to support multiple agentic frameworks. Often though the companies building agentic frameworks have a particular observability tool that they advertise in their docs, due to it being made by the same company or the existence of a partnership between companies.

This repo contains small experiments with a small subset of the many agent frameworks and observability services out there, focusing on the observability tools that they specifically advertise in their docs. A list of popular general LLM observability tools not used here can be found at the end of this README.

### CrewAI + AgentOps

https://docs.crewai.com/how-to/agentops-observability

AgentOps comes first in the observability tool integrations documented on the CrewAI website, I think they have some sort of partnership.

### LangChain + LangSmith

https://docs.smith.langchain.com/observability/how_to_guides/trace_with_langchain

LangChain and LangSmith are from the same company.

### LangGraph + Langsmith

LangGraph and LangSmith are from the same company.

https://docs.smith.langchain.com/observability/how_to_guides/trace_with_langgraph

### Orchestra + Braintrust

At the time of writing Braintrust in the only observability platform mentioned in the Orchestra documentation.

https://docs.orchestra.org/orchestra/observability

### PydanticAI + Logfire

https://ai.pydantic.dev/logfire/

PydanticAI and Pydantic logfire are from the same company.


### Other options not mentioned here

There are many other LLM observability platforms out there. Furthermore, LLM observability is often added on to frameworks that were originally built for more general ML evaluation and experiment tracking.

* Langtrace - unassociated with LangSmith/LangChain/LangGraph, despite the name. Open source AI observability and evals project.

* Langfuse - very popular open source platform for traces and evals

* Weights & Biases (including Weave) - the W&B MLOps platform has been around for quite a while, and is likely valued at over $1 billion. Weave is a lightweight tool they've released focused on evaluating and tracking AI applications.

* Comet - popular MLOps platform that's been around for quite a while

* Helicone - another MLOps platform

* Humanloop - seed funded company focused on building an LLM evals platform

* MLflow - a general open source MLOps platform that has been around quite a long time now (launched 2018), and that has more recently added lots of features specific to LLMs

* OpenLIT - open source AI engineering observability & ops framework

* Portkey

* ClearML - popular general MLOps platform

* GCP VertexAI

* Amazon Bedrock

* Azure - a whole variety of different services



