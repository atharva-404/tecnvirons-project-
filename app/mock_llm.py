
import asyncio

async def stream_llm(prompt: str):
    response = f"AI response to: {prompt}"
    for token in response.split():
        await asyncio.sleep(0.15)
        yield token + " "

async def summarize_session(text: str):
    await asyncio.sleep(1)
    return "Summary: " + text[:150]
