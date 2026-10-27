# Agent Loop

- the loop ends when the model doesn't request any more tool calls, i.e.,
when it has a final response for the user. You should already be handling
this case – returning/printing message.content when there are no tool_calls.
Just make sure that you also break out of the loop, or return from main(),
at this point.

- If the maximum number of iterations is reached and the model still
hasn't produced a final response, print a message explaining what went wrong.
You may also want to exit the program with a code of 1 to indicate failure.
