import openai

def generate_response(prompt, model="fine-tuned-model-id"):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()
