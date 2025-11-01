# import os
# import google.generativeai as genai
# import json

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# def call_llm(system_prompt: str, user_query: str) -> dict:
#     """
#     Routes query via Gemini → returns JSON dict
#     """

#     model = genai.GenerativeModel("gemini-2.0-flash")

#     try:
#         response = model.generate_content(
#             [
#                 {"role": "system", "parts": system_prompt},
#                 {"role": "user", "parts": user_query}
#             ]
#         )

#         text = response.text.strip()

#         # Try parsing JSON strictly
#         try:
#             return json.loads(text)
#         except Exception as e:
#             print("⚠️ Non-JSON response from model:", text)
#             return {"agent": "none", "user": "unknown"}

#     except Exception as e:
#         print(f"❌ Gemini error: {e}")
#         return {"agent": "none", "user": "unknown"}
