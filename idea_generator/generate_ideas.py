"""
This program reads in a long list of historical Python dojo ideas downloaded from Discord with an exporter tool.

It groups the messages by author, and then presents a multi-select of checkboxes to the user, one for each author.

An API call is then made to Claude, with all previous ideas from the selected authors used as examples for the LLM to use as a basis for generating more ideas.
"""

from collections import defaultdict
import json
from pathlib import Path
from dataclasses import dataclass
import inquirer
import anthropic
import os
from itertools import chain
import re

# messages downloaded from Discord with https://github.com/Tyrrrz/DiscordChatExporter
# warning: doing so breaks the Discord TOS
#json_path = Path(__file__).parent / "historical_ideas.txt"
json_path = Path("~/Dropbox/dev/python/dojo_ideas").expanduser() / "historical_ideas.txt"

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise Exception("Please set ANTHROPIC_API_KEY environment variable")

claude = anthropic.Anthropic(api_key=api_key)


@dataclass(frozen=True)
class Message:
    content: str
    author: str


def clean_content(message):
    # a very rough and incomplete url regex
    message = re.sub(r"\bhttp[:/\w\d.?=&-_]+", "", message).strip()

    return message


def main():
    with open(json_path) as f:
        data = json.load(f)

    messages = [
        Message(clean_content(m["content"]), m["author"]["nickname"])
        for m in data["messages"]
    ]

    # remove very short messages, or messages that only contained data removed by cleaning
    messages = [m for m in messages if len(m.content) > 5]

    message_by_author = defaultdict(list)
    for m in messages:
        message_by_author[m.author].append(m.content)

    questions = [
        inquirer.Checkbox(
            "ppl",
            message="Which combination of users should the suggestion be based on? (space to check/uncheck, enter to accept)",
            choices=list(sorted(message_by_author.keys())),
        ),
    ]
    ppl = inquirer.prompt(questions)["ppl"]

    for author, author_messages in message_by_author.items():
        if author not in ppl:
            continue

        print(f"Using messages from {author}:\n")
        for m in author_messages:
            print(f"* {m}\n")
        print("\n")

    # could just have appended them in the printing loop above, but I felt like some practice with iterables...
    selected_messages = list(
        chain.from_iterable(
            author_messages
            for author, author_messages in message_by_author.items()
            if author in ppl
        )
    )

    selected_messages_joined = "\n\n".join(selected_messages)

    claude_user_message = f"""
Here are some example ideas from previous dojos, please come up with several new ideas in the same style:

{selected_messages_joined}
"""

    system_prompt1 = "Your task is to come up with interesting, novel and challenging ideas for a coding dojo, in a similar style to previous ones."

    system_prompt2 = "Your task is to come up with relatively short coding dojo challenges, which are as similar in style as possible to the previous ones."

    system_prompt3 = "Your task is to come up with relatively short coding dojo challenges. The ideas should try to capture the same spirit and personality as a particular person who has already made several suggestions in the past. Come up with suggestions that reflect the personality of the person who came up with the previous suggestions."

    # the cheap model....
    # model="claude-3-haiku-20240307"
    # the more expensive one
    model = "claude-3-5-sonnet-20241022"

    message = claude.messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt3,
        messages=[{"role": "user", "content": claude_user_message}],
    )
    print(message.content[0].text)


if __name__ == "__main__":
    main()
