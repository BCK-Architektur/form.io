from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
import json

# Initialize the OpenAI client using the key from settings
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def index(request):
    print("Rendering index.html")
    return render(request, 'index.html')

    # def generate_bim(request):
    #     print("Received request for generate_bim")

    #     if request.method == "POST":
    #         # Get the prompt from the user input
    #         prompt = request.POST.get("prompt", "")
    #         print(f"Received prompt: {prompt}")

    #         if not prompt:
    #             print("Error: No prompt provided")
    #             return JsonResponse({"error": "No prompt provided"}, status=400)

    #         try:
    #             print("Sending prompt to OpenAI API...")

    #             # Use the client to create a chat completion
    #             response = client.chat.completions.create(
    #                 model="gpt-4",  # Specify the chat-based model
    #                 messages=[
    #                     {"role": "system", "content": "You are a BIM expert. Generate BIM JSON data based on the given prompt."},
    #                     {"role": "user", "content": prompt},
    #                 ]
    #             )

    #             print("OpenAI API call succeeded")
    #             print(f"Raw OpenAI Response: {response}")

    #             # Extract the content from the response
    #             bim_data = response.choices[0].message.content
    #             print(f"BIM JSON Data: {bim_data}")

    #             return JsonResponse({"bim_data": bim_data})
    #         except Exception as e:
    #             print(f"Error while calling OpenAI API: {e}")
    #             return JsonResponse({"error": str(e)}, status=500)

    #     print("Error: Invalid request method")
    #     return JsonResponse({"error": "Invalid request method"}, status=400)


import json

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

            # Validate JSON format of the BIM data
            try:
                json_data = json.loads(bim_data)

                # Check for required `src` key and add a placeholder if missing
                if "src" not in json_data:
                    json_data["src"] = "https://xeokit.io/examples/models/xkt/duplex/dataset.xkt"  # Example placeholder

                print(f"Validated BIM JSON Data: {json_data}")
                return JsonResponse({"bim_data": json_data})

            except json.JSONDecodeError as e:
                print(f"Invalid JSON format received: {e}")
                return JsonResponse({"error": "Invalid JSON format returned from OpenAI"}, status=500)

        except Exception as e:
            print(f"Error while calling OpenAI API: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    print("Error: Invalid request method")
    return JsonResponse({"error": "Invalid request method"}, status=400)
