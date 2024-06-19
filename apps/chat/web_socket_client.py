# import websocket
# import json

# def on_message(ws, message):
#     print("Received message:", message)

# def on_error(ws, error):
#     print("Error:", error)

# def on_close(ws):
#     print("WebSocket closed")

# def on_open(ws):
#     # Send a sample message
#     message = {
#         'message': 'Hello from the client',
#         'sender': 'client',
#         'recipient_id': 1  # Change recipient ID as needed
#     }
#     ws.send(json.dumps(message))

# if __name__ == "__main__":
#     # WebSocket endpoint URL
#     ws_url = "ws://localhost:8000/ws/chat/1/"  # Change URL and recipient ID as needed

#     # Create WebSocket connection
#     ws = websocket.WebSocketApp(ws_url,
#                                 on_message=on_message,
#                                 on_error=on_error,
#                                 on_close=on_close)

#     ws.on_open = on_open
#     ws.run_forever()
