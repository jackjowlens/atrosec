from fastapi import FastAPI
from app.schemas import UserRequest, StatusResponse, SecurityResponse
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app= FastAPI()

api_key=os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
model_name = os.getenv("OPENAI_MODEL", "cohere/north-mini-code:free")

client=AsyncOpenAI(api_key=api_key, base_url=base_url)

@app.get('/health')
def status_check():
    return {'status': 'ok'}

@app.post('/api/v1/audit',response_model=SecurityResponse)
async def audit_code(request: UserRequest):
    completion = await client.beta.chat.completions.parse(
    model=model_name,
    temperature=request.temperature,
    response_format=SecurityResponse,
    messages=[
        {
            "role": "system",
            "content": (
                "Ты аудитор безопасности компании AtroSec. Твоя задача — проверять код на уязвимости. "
                "Старайся соотносить ошибки и уязвимости со стандартами безопасности. "
                "Если не хватает контекста и ты не уверен в наличии ошибки, укажи, что контекста недостаточно. "
                "Обязательно предложи безопасное исправление."
            ),
        },
        {
            "role": "user",
            "content": f"Язык: {request.language}\nСам код:\n```\n{request.code_str}\n```",
        },
    ],
    )

    result = completion.choices[0].message.parsed
    return result



