import openai

#import os
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Use variável de ambiente

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        n=1,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

if __name__ == "__main__":
    print("Assistant: Hello, how can I assist you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Assistant: Goodbye!")
            break
        response = chat_with_gpt(user_input)
        print(f"Assistant: {response}")