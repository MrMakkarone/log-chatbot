# Log chatbot

## Context

I created this log chatbot project to show that I can build a plain chatbot prototype in a week based on my knowledge gained in the previous years.
This project is not vibe coded and aims as a conversation foundation to talk about design choices and challenges when creating a chatbot.  
It should also aid as an explorative insight how chatbots can help and accelerate reading log files and understand problems in their software and hardware, such as printers.

Therefore, I set as a goal that the chatbot should be able to answer questions like: "Please tell me whether there was a problem with the printing for a.jones roughly around 8 o clock at the 20th of October and whether it got resolved."

## Result - Example Chat Conversations

### Example 1
![Example chat conversation 1](https://raw.githubusercontent.com/MrMakkarone/log-chatbot/main/example_conversations/example-1.png)

### Example 1 - Tool Calls
![Example chat tool calls 1](https://raw.githubusercontent.com/MrMakkarone/log-chatbot/main/example_conversations/example-1-tool-calls.png)

### Example 2
![Example chat conversation 2](https://raw.githubusercontent.com/MrMakkarone/log-chatbot/main/example_conversations/example-2.png)

### Example 2 - Tool Calls
![Example chat tool calls 2](https://raw.githubusercontent.com/MrMakkarone/log-chatbot/main/example_conversations/example-2-tool-calls.png)

## Local deployment

### Start up Open WebUI and elasticsearch instances

```python
docker compose up -d
```

### Add tools
[README.md](https://github.com/MrMakkarone/log-chatbot/tree/main/tools/README.md)

### Add models
[README.md](https://github.com/MrMakkarone/log-chatbot/tree/main/models/README.md)

### Set up OpenRouter
[OpenRouter API key](https://openrouter.ai/workspaces/default/keys)

### Set connections

Admin Panel -> Settings -> Connections -> set URL to https://openrouter.ai/api/v1 and use the user token for the Bearer authentication.

Other API chat completions work more or less the same. I used [groq](https://groq.com/)'s (https://api.groq.com/openai/v1)(not GROK!:)) and [mistral](https://mistral.ai/)'s (https://api.mistral.ai/v1) API as well. Sometimes they change free models and rate limits, so simply choose what works best for you.

The user token: Found under profile-icon (right top) -> Settings -> Accounts -> API keys -> JWT token (might need to be activated if not yet visible: admin panel -> Settings -> General -> Enable API keys)
