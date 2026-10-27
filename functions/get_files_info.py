import os
from collections.abc import Callable
from functools import reduce

from openai.types.chat import ChatCompletionToolParam

schema_get_files_info: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
        valid_target_dir = (
            os.path.commonpath([working_directory_abs, target_dir])
            == working_directory_abs
        )

        if not os.path.isdir(target_dir):
            return f"Result for '{directory}' directory:\n    Error: {f'"{directory}"'} is not a directory"

        if not valid_target_dir:
            return f"Result for '{directory}' directory:\n    Error: Cannot list {f'"{directory}"'} as it is outside the permitted working directory"

        dir_contents = os.listdir(target_dir)
        reducer: Callable[[str, str], str] = lambda x, y: (
            x
            + f"   - {y}: file_size={os.path.getsize(os.path.join(target_dir, y))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, y))}\n"
        )

        return reduce(
            reducer,
            dir_contents,
            f"Result for {'current' if directory == '.' else f"'{directory}'"} directory:\n",
        )
    except Exception as e:
        return f"Result for {directory} directory:\n    Error: {e}"
