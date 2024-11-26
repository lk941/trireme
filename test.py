import pandas as pd
import requests
import json

# Read the Excel file
df = pd.read_excel("testdata/Software_Change_Request_ID_Generation.xlsx", sheet_name="Software Change Request")
# Convert to text, e.g., converting to CSV format or a specific structure
data_as_text = df.to_csv(index=False)

# Set up the request
url = "http://localhost:11434/api/generate"
payload = {
    "model": "mistral",
    "prompt": f"Based on the following data, please generate sample test data and the expected IDs:\n{data_as_text}'"
}
headers = {"Content-Type": "application/json"}

# Set up the request
# url = "http://localhost:11434/api/generate"
# payload = {
#     "model": "mistral",
#     "prompt": "give me 5 synonyms for tired"
# }
# headers = {"Content-Type": "application/json"}

# Send the request with `stream=True` to handle the streamed response
response = requests.post(url, json=payload, headers=headers, stream=True)

# Store the responses in a list
responses = []

# Process each line as a separate JSON object
for line in response.iter_lines():
    if line:
        line_data = line.decode('utf-8')
        try:
            json_line = json.loads(line_data)
            response_text = json_line.get("response", "")
            responses.append(response_text)  # Collect each response part
            #print(response_text)  # Print each part
        except ValueError:
            print("Error parsing JSON line:", line_data)

# Join all collected responses into a single output if needed
full_response = "".join(responses)
print("\nFull response:\n", full_response)