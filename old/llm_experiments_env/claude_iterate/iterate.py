from langchain_anthropic import ChatAnthropic
import click
from tempfile import NamedTemporaryFile

@click.command()
@click.option('--artifact', help='HTML + JS file to modify as an artifact')
@click.option('--prompt', help='Prompt for editing the code')
@click.option("--sonnet", is_flag=True, show_default=True, default=False, help="Use Sonnet model rather than cheap Haiku model")
def command(file, prompt, sonnet):
    if sonnet:
        model="claude-3-5-sonnet-20240620"
    else:
        model = "claude-3-haiku-20240307"

    llm = ChatAnthropic(
        model=model,
        max_tokens=4096
    )

    with open(file) as f:
        content = f.read()

    full_prompt = content + "\n" + prompt
    print(full_prompt)
    messages = [
        ("system", "You are an AI programming assistant. You will be provided some HTML and JavaScript code. After the closing </html> tag will come instructions to make improvements. Output only the code."),
        ("human", full_prompt),
    ]
    response = llm.invoke(messages)
    print(response.content)

    with NamedTemporaryFile(delete_on_close=False) as fp:
        f.write(response.content)

        # todo: display git diff, then optionally write to other file

    with open(file, "w") as f:
        f.write(response.content)



if __name__ == '__main__':
    command()