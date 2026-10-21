## Start up Open WebUI and elasticsearch instances

```python
docker compose up
```

## Add tools
[README.md](https://github.com/MrMakkarone/log-chatbot/tools/README.md)

## Add models
[README.md](https://github.com/MrMakkarone/log-chatbot/models/README.md)

## Set up OpenRouter
[OpenRouter API key](https://openrouter.ai/workspaces/default/keys)

## Set connections

Admin Panel -> Settings -> Connections -> set URL to https://openrouter.ai/api/v1 and use the user token for the Bearer authentication.

The user token: Found under profile-icon (right top) -> Settings -> Accounts -> API keys -> JWT token (might need to be activated if not yet visible: admin panel -> Settings -> General -> Enable API keys)
