# pip install openai
# export OPENAI_API_KEY=your_key_here

from openai import OpenAI
import json, sys

client = OpenAI()

# ----- Atomic math tools (pure, auditable functions) -----
def add(a: float, b: float) -> float:
    return a + b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero.")
    return a / b

# ----- Tools array: the "menu" the model can choose from -----
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers.",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                "required": ["a", "b"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiply two numbers.",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                "required": ["a", "b"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "divide",
            "description": "Divide a by b.",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                "required": ["a", "b"]
            },
        },
    },
]

# ----- System prompt: force the model to use tools for arithmetic -----
SYSTEM = (
    "You are a planning agent that MUST solve arithmetic only via the provided tools. "
    "Break the user request into sequential steps (add/multiply/divide), call tools in order, "
    "reuse prior results as needed, and finish with: 'Final answer: <number>'."
)

def run_agent(user_text: str, model: str = "gpt-4o-mini", max_loops: int = 8) -> str:
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_text},
    ]
    step_count = 0

    while step_count < max_loops:
        step_count += 1

        # Ask the model what to do next (talk vs. tool)
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.0,
        )
        msg = resp.choices[0].message

        # If the model wants tools, execute them and feed results back
        if msg.tool_calls:
            for call in msg.tool_calls:
                fn = call.function.name
                args = json.loads(call.function.arguments or "{}")

                try:
                    if fn == "add":
                        result = add(args["a"], args["b"])
                    elif fn == "multiply":
                        result = multiply(args["a"], args["b"])
                    elif fn == "divide":
                        result = divide(args["a"], args["b"])
                    else:
                        result = f"Error: unknown tool {fn}"
                except Exception as e:
                    result = f"Error: {e}"

                print(f"Step {step_count}: {fn}({args.get('a')}, {args.get('b')}) -> {result}")

                # Return tool result to the model as a tool message
                messages.append(msg)  # the tool-call request
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": fn,
                    "content": str(result),
                })
            continue  # loop again so the model can plan the next step

        # No more tool calls => final text answer
        final = (msg.content or "").strip()
        print(final)
        return final

    return "Stopped: reached loop limit without a final answer."

if __name__ == "__main__":
    prompt = "Please add 2 and 3, then multiply by 12, then divide the result by 2."
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    print(f"Query: {prompt}\n")
    _ = run_agent(prompt)
