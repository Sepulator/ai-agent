import os
import subprocess

from openai.types.chat import ChatCompletionToolParam

schema_run_python_file: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(
            os.path.join(working_directory_abs, file_path)
        )
        valid_target_path = (
            os.path.commonpath([working_directory_abs, target_file_path])
            == working_directory_abs
        )

        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(target_file_path) or not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file_path]

        if args and len(args) > 0:
            command.extend(args)

        result = subprocess.run(
            args=command,
            cwd=working_directory_abs,
            text=True,
            timeout=30,
            capture_output=True,
            check=False,
        )
        output_str = ""

        if result.returncode:
            output_str += f"Process exited with code {result.returncode}"

        if not result.stderr and not result.stdout:
            output_str += "No output produced"
        elif result.stdout:
            output_str += f"STDOUT: {result.stdout}"
        elif result.stderr:
            output_str += f"STDERR: {result.stderr}"

        return output_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
