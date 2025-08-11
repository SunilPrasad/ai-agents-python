
Multi-Step Math Agent (Python) — Tool Calling Demo

A tiny, beginner-friendly AI agent that plans a math problem into steps and calls tools repeatedly (add → multiply → divide) until it reaches the final answer.

⸻

What You’ll Learn
- What tool calling is and why LLMs use it
- How the OpenAI tools array works
- How the model decides to call a tool vs. answer with text
- A minimal planning loop that executes multiple tool calls

⸻

Why Do LLMs Need Tool Calls?

Function calling (also known as tool calling) is a powerful way for OpenAI models to interact with external systems and access data beyond their training.

For example, to get the current weather for a city, the LLM may need to call an external function that fetches live weather data. The complexity of this function can vary depending on the agent’s requirements.

Other examples include:

- Checking someone’s availability by reading their calendar

- Retrieving live sports scores (cricket, football, etc.)

- Fetching stock prices or other real-time information

This approach lets AI agents extend their capabilities far beyond static knowledge.
⸻

How OpenAI Tool Calling Works (In Practice)

1. You send the model:
	 - A system message (how it should behave).
	 - The user request (“add 2 and 3, multiply by 12, then divide by 2”).
	 - A tools array (the “menu” of functions it’s allowed to use).
	 - tool_choice="auto" so the model may call tools.
 
2. If the model decides it needs a tool, its response includes tool_calls like:

```json
{
  "tool_calls": [
    {
      "id": "call_123",
      "type": "function",
      "function": { "name": "add", "arguments": "{\"a\":2,\"b\":3}" }
    }
  ]
}
```

3.  Your Python code executes the function, then sends the tool result back to the model as a tool message.
4.	The model uses that result to plan the next step (another tool call) or to finish with a text answer.


 
