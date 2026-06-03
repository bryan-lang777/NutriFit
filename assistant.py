# utils/assistant.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class NutriFitAssistant:
    """Asistente nutricional usando Grok"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
    
    def responder(self, pregunta: str, momento: str = "post", actividad: str = "gym"):
        system_prompt = f"""
        Eres un nutricionista deportivo experto.
        Responde de forma clara, motivadora y profesional.
        Momento: {momento} (post = después de entrenar).
        Actividad: {actividad}.
        """

        try:
            response = self.client.chat.completions.create(
                model="grok-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": pregunta}
                ],
                temperature=0.7,
                max_tokens=600
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ Error con Grok: {str(e)}\n\nRecomendación: Después de entrenar consume proteína + carbohidratos."