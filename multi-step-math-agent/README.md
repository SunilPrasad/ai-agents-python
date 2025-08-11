
Multi-Step Math Agent (Python) — Tool Calling Demo

A tiny, beginner-friendly AI agent that plans a math problem into steps and calls tools repeatedly (add → multiply → divide) until it reaches the final answer. Great for learning and for posting step-by-step screenshots on X.

⸻

What You’ll Learn
	•	What tool calling is and why LLMs use it
	•	How the OpenAI tools array works
	•	How the model decides to call a tool vs. answer with text
	•	A minimal planning loop that executes multiple tool calls

⸻

Why Do LLMs Need Tool Calls?

LLMs are great at language but have limits:
	1.	They can be wrong at exact tasks (e.g., arithmetic) because they predict tokens, not numbers.
	2.	They can’t access external data by default (APIs, databases, live info).

Tool calls let the model stay the planner/decider and delegate precise work to reliable code (your functions). In this project, the model chooses when to call add, multiply, and divide—so arithmetic is always correct and auditable.

⸻

How OpenAI Tool Calling Works (In Practice)
	1.	You send the model:
	•	A system message (how it should behave).
	•	The user request (“add 2 and 3, multiply by 12, then divide by 2”).
	•	A tools array (the “menu” of functions it’s allowed to use).
	•	tool_choice="auto" so the model may call tools.
	2.	If the model decides it needs a tool, its response includes tool_calls like:
{
  "tool_calls": [
    {
      "id": "call_123",
      "type": "function",
      "function": { "name": "add", "arguments": "{\"a\":2,\"b\":3}" }
    }
  ]
}

Your Python code executes the function, then sends the tool result back to the model as a tool message.
	4.	The model uses that result to plan the next step (another tool call) or to finish with a text answer.


 
