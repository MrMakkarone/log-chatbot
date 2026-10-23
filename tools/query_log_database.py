"""### DSL Output Specification

Output a single JSON object matching the `llm_query_dict` schema defined below. Do not include markdown or wrapping unless requested.

---

### JSON Schema Rules

#### 1. `timestamp` (Optional)

* **Type:** Object
* **Keys:** Allowed keys are strictly `"gt"`, `"gte"`, `"lt"`, `"lte"`.
* **Value:** ISO date/datetime string (e.g., `"YYYY-MM-DD"` or `"YYYY-MM-DDTHH:MM:SS"`).
* **Correct Format:**
```json
"timestamp": {
  "gte": "2026-01-01",
  "lt": "2026-02-01"
}

```


* **Invalid:** `{"value": "2026-01-01", "operator": "gte"}` will throw a `ValueError`.

#### 2. `severity` (Optional)

* **Type:** Array of Strings
* **Allowed Values:** `"INFO"`, `"WARN"`, `"ERROR"` (Case-insensitive; normalized to uppercase).
* **Correct Format:**
```json
"severity": ["WARN", "ERROR"]

```



#### 3. Any Other Field Name (Optional)

* **Field Names:** Standard log fields such as `"log_type"`, `"component"`, `"event"`, `"message"`, etc.
* **Type:** String
* **Behavior:** Treated as a wildcard match pattern. Use leading/trailing `*` for substring matching.
* **Correct Format:**
```json
"component": "auth_service",
"message": "*timeout*"

```



---

### Example JSON Outputs

#### Example 1: Full Query

```json
{
  "timestamp": {
    "gte": "2026-10-01",
    "lte": "2026-10-23"
  },
  "severity": ["WARN", "ERROR"],
  "component": "payment-api",
  "message": "*failed*"
}

```

#### Example 2: Date Range & Text Match

```json
{
  "timestamp": {
    "gt": "2026-01-01"
  },
  "event": "user_login"
}

```

#### Example 3: Match All (Empty Query)

```json
{}

```
"""

import subprocess
import json
from typing import List, Optional
import ast


class Tools:

    def __init__(self):
        # self.valves = self.Valves()
        pass

    async def query_relevant_data(self, query: str) -> str:
        """
        :params: query:str: The DSL conform query in a JSON VALID format
        :return: Data is displayed in chat UI. Please inform the user if the data retrieval was successful, and whether the data was displayed successfully.
        """

        if query == None:
            raise ValueError(
                "Please provide a query",
            )

        subprocess_output = subprocess.run(
            [
                "python",
                "/app/custom_scripts/query_log_database.py",
                json.dumps(query),
            ],
            capture_output=True,
            text=True,
        )

        if subprocess_output.returncode != 0:
            return None, f"Script error:\n{subprocess_output.stderr}"

        retrieved_data = ast.literal_eval(subprocess_output.stdout)

        if not retrieved_data:
            raise ValueError("No data found for the specified parameters.")
        if not isinstance(retrieved_data, list):
            raise ValueError(
                "Expected to found a list of database entries, but found non. Is there no data/orders for the specified parameters?"
            )

        result = f"Found {len(retrieved_data)} entries. "

        # Check if retrieved data exceeds 20k token context
        tokens_est = len(str(retrieved_data)) // 4
        if tokens_est > 20000:
            result += f"The number of tokens is {tokens_est} tokens and thereby exceeds the limit of around 18-20k tokens. The answer was truncated to contain roughly 18k tokens."
            result += str(retrieved_data)[:72_000]  # ~18k tokens, with some safety margin
        else:
            result += str(retrieved_data)

        return result
