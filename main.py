import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="REALTIME_VOICE_ASSISTANT")


@app.get("/")
async def get_testing_page():

    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Voice Assistant</title>
        </head>
        <body>
            <h1>Testing Voice Assistant WebSocket Connection</h1>
            <div id="log" style="font-family: monospace; background: #222; color: #0f0; padding: 15px; min-height: 200px;">
                Connecting...<br>
            </div>

            <script>
                const logDiv = document.getElementById("log");
                // Connect to the exact same host using the websocket protocol
                const socket = new WebSocket("ws://" + window.location.host + "/voice");

                socket.onopen = function() {
                    logDiv.innerHTML += "🚀 Connection established smoothly!<br>";
                    // Send text to test the server's response
                    socket.send("Hello Server!");
                };

                socket.onmessage = function(event) {
                    logDiv.innerHTML += "📥 From Server: " + event.data + "<br>";
                };

                socket.onclose = function() {
                    logDiv.innerHTML += "🔌 Socket closed.<br>";
                };
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.websocket("/voice")
async def voice_endpoint_main(websocket: WebSocket):
    await websocket.accept()
    print("Client's voice connected to endpoint")
    await asyncio.sleep(1)

    async def inbound_loop():
        try:
            while True:
                data = await websocket.receive()
                if "bytes" in data:
                    raw_bytes = data["bytes"]
                    print("ok, I hear you")
                elif "text" in data:
                    print("text_commands not allowed")
                    await websocket.send_text("I only accept raw bytes")
        except WebSocketDisconnect:
            print("websocket disconnected")

    async def outbound_loop():
        try:
            while True:
                await asyncio.sleep(2)
        except WebSocketDisconnect:
            pass

    try:
        await asyncio.gather(inbound_loop(), outbound_loop())
    except Exception:
        print("connection disrupted")
