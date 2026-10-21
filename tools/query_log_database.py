import subprocess
import json
from typing import List, Optional
import ast

import requests



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
