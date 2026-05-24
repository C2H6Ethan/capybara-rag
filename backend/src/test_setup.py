import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import anthropic

# Load .env from project root
load_dotenv(Path(__file__).parent.parent.parent / ".env")

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=100,
    messages=[{"role": "user", "content": "Say hello capybara in one sentence"}]
)

print(message.content[0].text)