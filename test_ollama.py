import ollama

def chat_with_ai(prompt):
    response = ollama.chat(model="llama2", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Test AI response
user_input = "What is your name?"
ai_response = chat_with_ai(user_input)
print("AI Response:", ai_response)
