These are tools from Open WebUI. These are only COPIES. log-chatbot/tools/tool_x.py is never called!

In case you freshly set up Open WebUI and want the current functionality, copy paste these tools into the local hosted Open WebUI->Workspace->Tools->New Tool(top right)->copy paste tool->Save(right bottom corner).

The LLM only reads the tool description and the function doc string, e.g. 

```python
def call_this_function(example_parameter: str):
    """
    params:example_parameter (str): Give the example parameter based on the user query.
    """
```
