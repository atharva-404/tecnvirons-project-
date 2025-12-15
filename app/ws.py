import time
from fastapi import WebSocket, WebSocketDisconnect
from .db import supabase
from .mock_llm import stream_llm, summarize_session


async def handle_ws(ws: WebSocket, session_id: str):
    await ws.accept()
    start_time = time.time()
    conversation = ""

    # ✅ Insert session ONLY if it does not exist
    if supabase:
        existing = (
            supabase.table("sessions")
            .select("session_id")
            .eq("session_id", session_id)
            .execute()
        )

        if not existing.data:
            supabase.table("sessions").insert({
                "session_id": session_id,
                "user_id": "demo_user"
            }).execute()

    try:
        while True:
            msg = await ws.receive_text()
            conversation += f"User: {msg}\n"

            # ✅ Save user message
            if supabase:
                supabase.table("events").insert({
                    "session_id": session_id,
                    "role": "user",
                    "content": msg
                }).execute()

            # ✅ Stream AI response
            assistant_reply = ""
            async for token in stream_llm(msg):
                assistant_reply += token
                await ws.send_text(token)

            conversation += f"AI: {assistant_reply}\n"

            # ✅ Save only assistant reply
            if supabase:
                supabase.table("events").insert({
                    "session_id": session_id,
                    "role": "assistant",
                    "content": assistant_reply
                }).execute()

    except WebSocketDisconnect:
        pass

    finally:
        # ✅ Post-session processing
        duration = int(time.time() - start_time)
        summary = await summarize_session(conversation)

        if supabase:
            supabase.table("sessions").update({
                "duration_seconds": duration,
                "summary": summary
            }).eq("session_id", session_id).execute()
