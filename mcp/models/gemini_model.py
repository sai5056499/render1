import google.generativeai as genai
import os

class get_gemini_response:
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        genai.configure(api_key=self.API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_content(self,prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error: {e}")
            return None
