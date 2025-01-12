from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
import re

# Initialize the OpenAI client using the key from settings
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def index(request):
    print("Rendering index.html")
    return render(request, 'index.html')

def sanitize_json(json_string):
    """
    Removes trailing commas from JSON strings.
    """
    # Remove trailing commas in arrays and objects
    json_string = re.sub(r",\s*([\]}])", r"\1", json_string)
    return json_string

@csrf_exempt
def generate_bim(request):
    print("Received request for generate_bim")

    if request.method == "POST":
        # Get the prompt from the user input
        prompt = request.POST.get("prompt", "").strip()
        print(f"Received prompt: {prompt}")

        if not prompt:
            print("Error: No prompt provided")
            return JsonResponse({"error": "No prompt provided"}, status=400)

        try:
            print("Sending prompt to OpenAI API...")

            # Use the client to create a chat completion
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a BIM expert. Generate BIM JSON data for the given prompt. "
                            "Ensure the JSON contains keys: 'BuildingElement', 'length', 'properties', and 'geometry'. "
                            "'geometry' must include 'vertices' and 'faces'. Avoid trailing commas."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
            )

            print("OpenAI API call succeeded")
            print(f"Raw OpenAI Response: {response}")

            # Extract the content from the response
            bim_data = response.choices[0].message.content
            print(f"Raw BIM JSON Data: {bim_data}")

            # Sanitize JSON to remove trailing commas
            sanitized_bim_data = sanitize_json(bim_data)
            print(f"Sanitized BIM JSON Data: {sanitized_bim_data}")

            # Validate JSON format
            try:
                json_data = json.loads(sanitized_bim_data)

                # Check for required `src` key and add a placeholder if missing
                if "src" not in json_data:
                    json_data["src"] = "https://xeokit.io/examples/models/xkt/duplex/dataset.xkt"

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
    print("Received request for generate_bim")

    if request.method == "POST":
        # Get the prompt from the user input
        prompt = request.POST.get("prompt", "").strip()
        print(f"Received prompt: {prompt}")

        if not prompt:
            print("Error: No prompt provided")
            return JsonResponse({"error": "No prompt provided"}, status=400)

        try:
            print("Sending prompt to OpenAI API...")

            # Use the client to create a chat completion
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a BIM expert. Generate BIM JSON data for the given prompt. "
                            "Ensure the JSON contains keys: 'BuildingElement', 'length', 'properties', and 'geometry'. "
                            "'geometry' must include 'vertices' and 'faces' for rendering."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
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
                    json_data["src"] = "https://xeokit.io/examples/models/xkt/duplex/dataset.xkt"

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
    """
    Generates BIM JSON from user prompt using OpenAI API.
    """
    if request.method == "POST":
        prompt = request.POST.get("prompt", "").strip()
        if not prompt:
            return JsonResponse({"error": "No prompt provided"}, status=400)

        try:
            # Sending prompt to OpenAI API
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a BIM expert. Generate BIM JSON data for the given prompt. "
                            "Ensure the JSON contains the following keys: "
                            "'BuildingElement', 'length', 'properties', and 'geometry'. "
                            "The 'geometry' key must have 'vertices' and 'faces' for rendering."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
            )

            # Extract BIM data from OpenAI response
            bim_data = response.choices[0].message.content
            try:
                json_data = json.loads(bim_data)

                # Validate and ensure `src` key for .xkt file
                if "src" not in json_data:
                    json_data["src"] = "https://xeokit.io/examples/models/xkt/duplex/dataset.xkt"

                return JsonResponse({"bim_data": json_data})
            except json.JSONDecodeError:
                return JsonResponse(
                    {"error": "Invalid JSON format received from OpenAI."}, status=500
                )
        except Exception as e:
            return JsonResponse({"error": f"OpenAI API error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)