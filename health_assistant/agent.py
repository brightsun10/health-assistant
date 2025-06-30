# health_assistant/agent.py

import os
import json
import google.generativeai as genai
# from google.generativeai.types import FunctionDeclaration, Schema
from .models import HealthLog

# Configure the Gemini API key
try:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
except AttributeError:
    print("Failed to configure Gemini API key. Ensure GEMINI_API_KEY is set in your .env file.")

class HealthAgent:
    """The core AI agent that processes user messages and uses tools."""

    def __init__(self, user):
        """
        Initializes the agent for a specific user.
        """
        self.user = user
        # This defines the "tool" the agent can use.
        # We tell the model to respond in a specific JSON format if it wants to use this tool.
        self.chat_history = []
        self.log_health_data_tool = {
            "function_declarations": [
                {
                    "name": "log_health_data",
                    "description": "Logs a user's health data, such as meals, symptoms, or exercises.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "log_type": {
                                "type": "string",
                                "description": "The type of data: Meal, Symptom, Exercise"
                            },
                            "content": {
                                "type": "string",
                                "description": "Details like 'oatmeal for breakfast'"
                            }
                        },
                        "required": ["log_type", "content"]
                    }
                }
            ]
        }



        # Initialize the generative model with the tool definition
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            tools=[{
                "function_declarations": [
                    {
                        "name": "log_health_data",
                        "description": "Logs a user's health data (meal, symptom, or exercise).",
                        "parameters": {
                            "type": "OBJECT",  # Note: Use uppercase "OBJECT"
                            "properties": {
                                "log_type": {
                                    "type": "STRING",  # Uppercase
                                    "description": "Type: Meal, Symptom, or Exercise"
                                },
                                "content": {
                                    "type": "STRING",
                                    "description": "Details (e.g., 'Ragi ball and tomato sambar')"
                                }
                            },
                            "required": ["log_type", "content"]
                        }
                    }
                ]
            }]
        )



        
    def _execute_tool_call(self, tool_call):
        """
        Executes a tool call requested by the model.
        """
        if tool_call.name == 'log_health_data':
            args = tool_call.args
            log_type_str = args.get('log_type', 'Unknown').upper()
            content = args.get('content', '')

            # Map the string from the model to our model's enum
            log_type_map = {
                'MEAL': HealthLog.LogType.MEAL,
                'SYMPTOM': HealthLog.LogType.SYMPTOM,
                'EXERCISE': HealthLog.LogType.EXERCISE,
            }
            log_type = log_type_map.get(log_type_str, HealthLog.LogType.UNKNOWN)

            if not content or log_type == HealthLog.LogType.UNKNOWN:
                return "I couldn't save that. Please be more specific about the type (meal, symptom, or exercise) and content of the log."

            try:
                # Create the HealthLog entry in the database
                HealthLog.objects.create(
                    user=self.user,
                    log_type=log_type,
                    content=content
                )
                return f"OK. I've logged that {log_type_str.lower()} for you."
            except Exception as e:
                print(f"Error saving to DB: {e}")
                return "I had trouble saving that right now. Please try again later."
        return "I'm not sure how to do that."


    def get_response(self, user_input, history=None):
        self.chat_history.append({
            "role": "user",
            "parts": [{"text": user_input}]
        })

        try:
            chat = self.model.start_chat(history=self.chat_history)
            print("User input:", user_input)
            response = chat.send_message(user_input)
            print("Raw model response:", response)

            response_text = ""

            # Check if the model responded with a tool/function call
            if response.candidates and hasattr(response.candidates[0].content.parts[0], 'function_call'):
                tool_call = response.candidates[0].content.parts[0].function_call
                print("Tool call detected:", tool_call)
                response_text = self._execute_tool_call(tool_call)
            else:
                # Normal text response
                for part in response.parts:
                    if hasattr(part, 'text'):
                        response_text += part.text
                    else:
                        print("Skipped non-text part:", part)

            # Append model response to chat history (important for future context)
            self.chat_history.append({
                "role": "model",
                "parts": [{"text": response_text}]
            })

            return response_text or "Sorry, I couldn't understand that."

        except Exception as e:
            print("Error during agent response:", e)
            return "Something went wrong with the assistant."







