# https://python.langchain.com/v0.2/docs/tutorials/sql_qa/

"""
Setup:
sqlite3 chinook.db
.read chinook.sql
"""

from langchain_community.utilities import SQLDatabase
from langchain_anthropic import ChatAnthropic
from langchain_google_vertexai import ChatVertexAI
from langchain.chains import create_sql_query_chain


db = SQLDatabase.from_uri("sqlite:///chinook.db")
# print(db.dialect)
# print(db.get_usable_table_names())
# db.run("SELECT * FROM Artist LIMIT 10;")

#llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
#llm = ChatAnthropic(model="claude-3-haiku-20240307")
llm = ChatVertexAI(model="gemini-1.5-flash")    

chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "How many employees are there"})

response
chain.get_prompts()[0].pretty_print()


# part two
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
chain = write_query | execute_query
chain.invoke({"question": "How many employees are there"})


# part three
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer_prompt
    | llm
    | StrOutputParser()
)

chain.invoke({"question": "How many employees are there"})