import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI(title="EduGenie - Gemini Powered Learning Assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
client = genai.Client(api_key=API_KEY) if API_KEY else None

def ask_gemini(prompt: str):
    if not client:
        return "Gemini API key is missing. Add GEMINI_API_KEY to your .env file."
    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return response.text
    except Exception as e:
        return f"Gemini API error: {e}"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/qa")
async def qa(data: dict):
    text = data.get("text", "").strip()
    prompt = f"Answer this educational question clearly and concisely:\n{text}"
    return JSONResponse({"result": ask_gemini(prompt)})

@app.post("/explain")
async def explain(data: dict):
    text = data.get("text", "").strip()
    prompt = f"Explain this topic in simple language for a learner. Use examples when useful:\n{text}"
    return JSONResponse({"result": ask_gemini(prompt)})

@app.post("/quiz")
async def quiz(data: dict):
    text = data.get("text", "").strip()
    prompt = f"""Create exactly 3 multiple-choice questions from this educational text.
Return ONLY valid JSON as an array. Each item must contain:
question, options (exactly 4 strings), answer.
Text:
{text}"""
    result = ask_gemini(prompt)
    try:
        cleaned = result.replace("```json", "").replace("```", "").strip()
        return JSONResponse({"result": json.loads(cleaned)})
    except Exception:
        return JSONResponse({"result": result})

@app.post("/summarize")
async def summarize(data: dict):
    text = data.get("text", "").strip()
    prompt = f"Summarize the following educational passage concisely while retaining the important information:\n{text}"
    return JSONResponse({"result": ask_gemini(prompt)})

@app.post("/learn/recommendations")
async def learning_path(data: dict):
    text = data.get("text", "").strip()
    prompt = f"""Create a structured learning path for: {text}
Start from beginner level and progress to advanced level.
Include topics, suggested order, and useful learning resources."""
    return JSONResponse({"result": ask_gemini(prompt)})
