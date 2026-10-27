# AI Agent

## What Does the Agent Do?

The program is a CLI tool that:

1. Accepts a coding task (e.g., "strings aren't splitting in my app, pweeze fix")
2. Chooses from a set of predefined functions to work on the task, for example:
   - Scan the files in a directory
   - Read a file's contents
   - Overwrite a file's contents
3. Execute the Python interpreter on a file
4. Repeats step 2 until the task is complete (or it fails miserably, which is possible

## Prerequisites

- Python 3.10+ installed
- The uv project/package manager
- Access to a Unix-like shell (e.g. zsh or bash)
- [OpenRouter](https://openrouter.ai/) API key, free tier is enough to test
