import streamlit as st
import google.generativeai as genai
import json
from models import UserProfile

class MemoryModule:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={"response_mime_type": "application/json"}
        )

    def extract_memory(self, chat_logs: str) -> UserProfile:
        # UPDATED PROMPT: We explicitly tell it how to handle multiple people
        system_prompt = (
            "You are an expert Data Scientist. Analyze the logs. "
            "If the chat involves multiple people, extract a 'Team Context' profile. "
            "1. 'preferences': Work styles or specific dislikes of the team members. "
            "2. 'emotional_patterns': The overall mood (e.g., 'Team is stressed about deployment'). "
            "3. 'facts': Hard data about the incident, names, and roles. "
            "Return a SINGLE JSON object matching this schema: "
            "{'preferences': [], 'emotional_patterns': [], 'facts': []}."
        )

        try:
            print("Attempting to call Gemini API...") 
            response = self.model.generate_content(
                f"{system_prompt}\n\nCHAT LOGS:\n{chat_logs}"
            )
            
            raw_data = json.loads(response.text)
            
            # --- 🛡️ THE FIX IS HERE 🛡️ ---
            # If the AI returns a List (because it found multiple people), 
            # we take the first item or merge them.
            if isinstance(raw_data, list):
                if len(raw_data) > 0:
                    raw_data = raw_data[0] # Take the first object
                else:
                    # Empty list case
                    raw_data = {"preferences": [], "emotional_patterns": [], "facts": []}
            
            # Validate keys exist
            if "facts" not in raw_data: raw_data["facts"] = []
            if "preferences" not in raw_data: raw_data["preferences"] = []
            if "emotional_patterns" not in raw_data: raw_data["emotional_patterns"] = []

            return UserProfile(**raw_data)
            
        except Exception as e:
            st.error(f"❌ Extraction Error: {str(e)}")
            st.warning(f"Raw Output causing error: {response.text if 'response' in locals() else 'None'}")
            return UserProfile(preferences=[], emotional_patterns=[], facts=[])