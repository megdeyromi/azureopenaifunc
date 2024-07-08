import io
import json
import base64
import os
from fdk import response
from openai import AzureOpenAI

def handler(ctx, data: io.BytesIO=None):
    print("Entering Python handler", flush=True)

    body = {}  # Initialize body with an empty dictionary
    
    try:
        # Read the incoming base64 encoded data
        base64_encoded_data = data.getvalue()
        
        # Decode the base64 data
        decoded_data = base64.b64decode(base64_encoded_data)
        
        # Parse the JSON data
        body = json.loads(decoded_data)
        
        # Extract user prompt from JSON data
        user_prompt = body.get("prompt")
        if not user_prompt:
            raise ValueError("Missing 'prompt' in the request data.")
        
        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            azure_endpoint="https://jaguksouth6726803320.openai.azure.com/",
            api_key="efa992652f52414cb5934735efa47288",
            api_version="2024-02-15-preview",
        )

        # Construct the message
        message_text = [
            {
                "role": "user",
                "content": user_prompt,
            }
        ]

        # Generate completion
        completion = client.chat.completions.create(
            model="gpt-35-turbo",
            messages=message_text,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )

        # Extract the response content
        response_content = completion.choices[0].message.content

        # Prepare the response data
        response_data = {
            "insights": response_content
        }

        print("Exiting Python handler", flush=True)

        return response.Response(
            ctx,
            response_data=json.dumps(response_data),
            headers={"Content-Type": "application/json"}
        )

    except (Exception, ValueError) as ex:
        error_message = f"Error processing request: {str(ex)}"
        print(error_message, flush=True)
        return response.Response(
            ctx,
            response_data=json.dumps({"error": error_message}),
            headers={"Content-Type": "application/json"},
            status_code=500  # Internal Server Error
        )

    finally:
        print("Exiting Python handler", flush=True)
