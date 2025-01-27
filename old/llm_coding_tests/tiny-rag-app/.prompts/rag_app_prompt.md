# RAG App Development Requirements

## Context
You will build a Retrieval-Augmented Generation (RAG) app using the LangChain framework in Python. The app will use the provided LangChain RAG tutorial documentation, which contains the most current API references, code samples, and library details. Your solution must adhere to the relevant approaches and patterns described in that documentation, overriding any conflicting prior knowledge.

The app should allow users to input a web page URL, load all page content, store it in a vector database, and ask questions based on the content via a user-friendly Streamlit web interface. All AI features must be implemented using OpenAI models, specifically GPT-4 Turbo (gpt-4-turbo), and must comply with the listed dependencies and library versions.

## Requirements

### 1. Environment Setup
- Use Python version 3.11
- Use the below library dependencies, without version specifiers to get the latest stable versions:
  - beautifulsoup4
  - langchain
  - langchain-community
  - langchain-openai
  - langchain-chroma
  - python-dotenv
  - streamlit
- Assume the developer will create a Python virtual environment using the python -m venv method to isolate dependencies
- Generate a requirements.txt file specifying all necessary dependencies

### 2. App Features
- Load complete contents of a web page from a user-provided URL
- Display the contents of the web page in the UI for confirmation
- Store the web page content in a ChromaDB vector database for efficient retrieval
- The database and previously stored data must persist across user sessions
- Allow users to ask questions based on the stored content using GPT-4 Turbo
- Use LangChain's retrieval chain mechanism for querying the vector database

### 3. Streamlit UI Design
- Create a web-based interface for the app:
  - Input fields for the web page URL and user questions
  - Buttons for loading content, storing it in the vector database, and running queries
  - Display areas for web page content and query results
- Incorporate a visually appealing design with the following style guidelines:
  - Blues and purples as the primary colors
  - A splash of red for accents (e.g., buttons or headings)
  - Clean, user-friendly layout

### 4. Implementation
- The solution should be modular, with components logically separated to improve maintainability and reusability
- Avoid placing all code into a single file; instead, organize it into multiple modules or files as appropriate
- Generate all required files, functions, methods, imports, and code
- Fully implement the app, including backend logic and UI components
- Ensure clear inline comments explaining key parts of the code

### 5. Constraints
- Do not implement features beyond those described here
- Ensure the LLM answers questions based **only** on the knowledge provided by the loaded web page content stored in the vector database
- Follow best practices for maintainable and modular code
- Use the documentation to ensure compatibility with the latest LangChain APIs and provided library versions

### 6. Delivery
Output the complete project structure, including:
- Python scripts with implemented code
- A requirements.txt file
- Inline comments explaining the functionality of the app

## Instructions to the Coding Assistant
- Follow the provided LangChain documentation meticulously. If you encounter ambiguities or unsupported patterns in your training data, default to the methods specified in the documentation
- Use the specified dependencies and library versions in all implementations
- Ensure the app is logically structured, modular, and easy to maintain