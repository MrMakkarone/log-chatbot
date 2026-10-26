These are tools from Open WebUI. These are only COPIES. log-chatbot/tools/tool_x.py is never called!

In case you freshly set up Open WebUI and want the current functionality/tools, import the JSON [query_log_database.json](https://github.com/MrMakkarone/log-chatbot/tree/main/tools/query_log_database.json) and [get_current_time.json](https://github.com/MrMakkarone/log-chatbot/tree/main/tools/get_current_time.json) into the locally hosted Open WebUI ->Workspace->Tools->drop down next to create.

The LLM only reads the tool description and the function doc string, e.g. 

```python
def call_this_function(example_parameter: str):
    """
    params:example_parameter (str): Give the example parameter based on the user query.
    """
```
