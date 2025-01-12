from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=
"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"
)

def index(request):
    print("Rendering index.html")
    return render(request, 'index.html')

def generate_bim(request):
    print("Received request for generate_bim")

    if request.method == "POST":
        # Get the prompt from the user input
        prompt = request.POST.get("prompt", "")
        print(f"Received prompt: {prompt}")

        if not prompt:
            print("Error: No prompt provided")
            return JsonResponse({"error": "No prompt provided"}, status=400)

        try:
            print("Sending prompt to OpenAI API...")

            # Use the client to create a chat completion
            response = client.chat.completions.create(
                model="gpt-4",  # Specify the chat-based model
                messages=[
                    {"role": "system", "content": "You are a BIM expert. Generate BIM JSON data based on the given prompt."},
                    {"role": "user", "content": prompt},
                ]
            )

            print("OpenAI API call succeeded")
            print(f"Raw OpenAI Response: {response}")

            # Extract the content from the response
            bim_data = response.choices[0].message.content
            print(f"BIM JSON Data: {bim_data}")

            return JsonResponse({"bim_data": bim_data})
        except Exception as e:
            print(f"Error while calling OpenAI API: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    print("Error: Invalid request method")
    return JsonResponse({"error": "Invalid request method"}, status=400)
