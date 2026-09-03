import asyncio
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from runtime.runtime import TranscendingRuntime

app = FastAPI()

# เปิดสิทธิ์ให้ Next.js หน้าบ้านยิงเรียกข้ามพอร์ตได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ประกาศเปิดเครื่องยนต์สมองกลของโครงการไว้ที่ส่วนกลาง
runtime_engine = TranscendingRuntime()


async def generate_brain_thought(user_prompt: str):
    """
    ฟังก์ชันจำลองการดึงความนึกคิดจาก Cognitive Loop ของสมองกล 
    แล้วส่งสัญญาณกลับไปยังหน้าบ้านทีละประโยค (Streaming)
    """
    try:
        # 1. ส่งข้อมูลเข้าสู่ระบบกระตุ้นความคิด (Inference)
        # หมายเหตุ: ปรับแก้ฟังก์ชัน .think หรือ .process ให้ตรงกับโครงสร้างภายในของคุณ
        thought_output = runtime_engine.cognitive.think(
            text=user_prompt, context="[DASHBOARD_LIVE_STREAM]"
        )

        # 2. จำลองการหั่นข้อมูลส่งเป็นคำๆ ยิงกลับไปที่หน้าจอ Chat Window
        words = thought_output.split(" ")
        for word in words:
            # รูปแบบ JSON ที่คอมโพเนนต์แชทหน้าบ้านส่วนใหญ่นิยมแกะอ่าน
            yield json.dumps({"content": word + " "}) + "\n"
            await asyncio.sleep(0.05)  # สร้างดีเลย์เล็กน้อยเพื่อความสมจริง

    except Exception as e:
        yield json.dumps({"error": str(e)}) + "\n"


@app.post("/api/chat")
async def handle_chat_stream(request: Request):
    """
    Endpoint หลักที่ Next.js (พอร์ต 3000) ยิงมารับส่งข้อมูลสดๆ
    """
    body = await request.json()
    # ดึงข้อความ/โจทย์ล่าสุดที่พิมพ์มาจากกล่อง ChatInput.tsx
    messages = body.get("messages", [])
    user_prompt = messages[-1]["content"] if messages else ""

    return StreamingResponse(
        generate_brain_thought(user_prompt), media_type="text/event-stream"
    )


if __name__ == "__main__":
    import uvicorn

    print("🧠 [SYSTEM] Starting Cyber Human Brain Gateway on port 3001...")
    uvicorn.run(app, host="0.0.0.0", port=3001)
