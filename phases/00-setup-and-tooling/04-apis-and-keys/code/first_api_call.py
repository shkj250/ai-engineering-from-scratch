
import os
import json
import urllib.request
from openai import OpenAI

def call_with_sdk():
    client = OpenAI(
        api_key=os.environ.get('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com"
    )

    response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

    print(response.choices[0].message.content)

def call_raw_http():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("Set DEEPSEEK_API_KEY environment variable first")
        return

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    body = json.dumps(
        {
        "model": "deepseek-v4-flash",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Hello I am using the API!"}
        ],
        "thinking": {"type": "enabled"},
        "reasoning_effort": "high",
        "stream": False
      }
        ).encode()

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))

            print(f"Raw HTTP response: {result['choices'][0]['message']['content']}")

            usage = result.get("usage", {})
            print(
                f"Tokens used: "
                f"{usage.get('prompt_tokens')} in, "
                f"{usage.get('completion_tokens')} out, "
                f"{usage.get('total_tokens')} total"
            )

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {error_body}")

    except urllib.error.URLError as e:
        print(f"Network Error: {e.reason}")




if __name__ == "__main__":
    print("=== API Calls ===\n")
    print("1. Using the SDK:")
    call_with_sdk()
    print("\n2. Using raw HTTP:")
    call_raw_http()
