import requests

# 🚨 Replace this with your OpenRouter API key
API_KEY = "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"

# ✅ Model you're using (this one is fast and free)
MODEL_ID = "mistralai/mistral-7b-instruct:free"

# 📥 Enter your user question below
user_question = "what do you mean by 52 week high?"

# 🧠 System prompt sets the assistant's role and behavior
system_prompt = {
    "role": "system",
    "content": (
        "You are an AI assistant with expert knowledge exclusively in the stock market. "
        "You must only respond to questions strictly related to stock market concepts, trading, investment strategies, IPOs, financial regulations, market indices, or terms used in share markets. "
        "If a user asks anything outside this scope, you must reply with only this message: "
        "'I'm sorry, I am specialized in stock market topics and cannot help with that.' "
        "You must not explain, suggest unrelated resources, or give extra information under any circumstance."
    )
}


# 🗨️ User prompt
user_prompt = {"role": "user", "content": user_question}

# 📡 Call OpenRouter API
def query_openrouter(model_id, messages):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_id,
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        print(f"\n💬 Model Response:\n{reply}")
    else:
        print(f"\n⚠️ Error: {response.status_code} - {response.text}")

# 🏁 Run the script
if __name__ == "__main__":
    messages = [system_prompt, user_prompt]
    query_openrouter(MODEL_ID, messages)