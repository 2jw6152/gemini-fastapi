from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
import os

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중엔 * 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    # Gemini 2.5 Flash
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)  # Thinking 비활성화
        ),
    )

    return {"response": response.text}
