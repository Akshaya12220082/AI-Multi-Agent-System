import os
if self.provider == "openai":
try:
import openai
except Exception:
raise RuntimeError("Please install openai package")
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
raise RuntimeError("OPENAI_API_KEY not set")
self.openai = openai
if not self.model:
self.model = "gpt-4o-mini"
elif self.provider == "gemini":
try:
import google.generativeai as genai
except Exception:
raise RuntimeError("Please install google-generativeai")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
self.genai = genai
if not self.model:
self.model = "gemini-1.5-flash"
elif self.provider == "huggingface":
import requests
self.requests = requests
self.api_key = os.getenv("HUGGINGFACE_API_KEY")
if not self.api_key:
raise RuntimeError("HUGGINGFACE_API_KEY not set")
if not self.model:
self.model = "meta-llama/Llama-3.1-8B-Instruct"
else:
raise ValueError(f"Unsupported provider: {self.provider}")


def complete(self, system: str, prompt: str, temperature: float = 0.2, max_tokens: int = 512):
if self.provider == "openai":
resp = self.openai.ChatCompletion.create(
model=self.model,
messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
temperature=temperature,
max_tokens=max_tokens,
)
return resp.choices[0].message.content.strip()
elif self.provider == "gemini":
prompt_full = f"[SYSTEM]\n{system}\n\n[USER]\n{prompt}"
out = self.genai.generate_text(model=self.model, prompt=prompt_full)
return out.text
elif self.provider == "huggingface":
url = f"https://api-inference.huggingface.co/models/{self.model}"
payload = {"inputs": f"System: {system}\nUser: {prompt}", "parameters": {"max_new_tokens": max_tokens, "temperature": temperature}}
headers = {"Authorization": f"Bearer {self.api_key}"}
r = self.requests.post(url, headers=headers, json=payload, timeout=60)
r.raise_for_status()
data = r.json()
# Support both list/dict responses
if isinstance(data, list) and data:
return data[0].get("generated_text", "")
if isinstance(data, dict) and "generated_text" in data:
return data["generated_text"]
return str(data)