import argparse
import os
import sys
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    _ = parser.add_argument("user_prompt", type=str, help="User prompt")
    _ = parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()

    _ = load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable wasn't found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages: list[Any] = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": args.user_prompt,
        },
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    max_retries = 20
    for _ in range(max_retries):
        if generate_content(client, messages, args.verbose):
            return

    print(
        f"Error: Agent exceed maximum iterations ({max_retries}) without producing final response"
    )
    sys.exit(1)


def generate_content(client: OpenAI, messages: list[Any], verbose: bool) -> bool:

    response = client.chat.completions.create(
        model="openrouter/free", messages=messages, tools=available_functions
    )

    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        print("Response:")
        print(message.content)
        return True

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        result_message = call_function(tool_call, verbose)
        messages.append(result_message)
        if "content" not in result_message:
            raise RuntimeError("No content in tool call result message")
        if verbose:
            print(f" -> {result_message['content']})")

    return False


if __name__ == "__main__":
    main()
