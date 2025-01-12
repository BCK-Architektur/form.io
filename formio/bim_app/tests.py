import openai

openai.api_key = "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"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a BIM expert. Generate BIM JSON data."},
        {"role": "user", "content": "Generate a 5-floor apartment building with modular units."},
    ]
)
print(response)