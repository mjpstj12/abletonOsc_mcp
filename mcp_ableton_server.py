from mcp.server.fastmcp import FastMCP
import asyncio
import json
import socket
import sys
from typing import List, Optional

class AbletonClient:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.responses = {}  # Store futures keyed by (request_id)
        self.lock = asyncio.Lock()
        self._request_id = 0  # counter to generate unique ids
        
        # Asynchronous task to read responses
        self.response_task = None

    async def start_response_reader(self):
        """Background task to read responses from the socket, potentially multiple messages."""
        # Convert self.sock to asyncio Streams
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        loop = asyncio.get_running_loop()
        await loop.create_connection(lambda: protocol, sock=self.sock)

        while self.connected:
            try:
                data = await reader.read(4096)
                if not data:
                    # Connection closed
                    break

                try:
                    msg = json.loads(data.decode())
                except json.JSONDecodeError:
                    print("Invalid JSON from daemon", file=sys.stderr)
                    continue

                resp_id = msg.get('id')

                # If it's a JSON-RPC response
                if 'result' in msg or 'error' in msg or 'status' in msg:
                    # Response to a request
                    async with self.lock:
                        fut = self.responses.pop(resp_id, None)
                    if fut and not fut.done():
                        fut.set_result(msg)
                else:
                    # Otherwise it's an "osc_response" or another type
                    # (According to the daemon code)
                    if msg.get('type') == 'osc_response':
                        # We can route according to the address
                        address = msg.get('address')
                        args = msg.get('args')
                        await self.handle_osc_response(address, args)
                    else:
                        print(f"Unknown message: {msg}", file=sys.stderr)

            except Exception as e:
                print(f"Error reading response: {e}", file=sys.stderr)
                break

    async def handle_osc_response(self, address: str, args):
        """Callback when receiving an OSC message from Ableton."""
        # Simple example: we could do a set_result on a future
        print(f"OSC Notification from {address}: {args}", file=sys.stderr)

    def connect(self):
        """Connect to the OSC daemon via TCP socket."""
        if not self.connected:
            try:
                self.sock.connect((self.host, self.port))
                self.connected = True
                
                # Start the response reader task
                self.response_task = asyncio.create_task(self.start_response_reader())
                return True
            except Exception as e:
                print(f"Failed to connect to daemon: {e}", file=sys.stderr)
                return False
        return True

    async def send_rpc_request(self, method: str, params: dict) -> dict:
        """
        Send a JSON-RPC request (method, params) and wait for the response.
        """
        if not self.connected:
            if not self.connect():
                return {'status': 'error', 'message': 'Not connected to daemon'}

        # Generation of a unique ID
        self._request_id += 1
        request_id = str(self._request_id)

        # Build the JSON-RPC request
        request_obj = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params
        }

        future = asyncio.Future()
        async with self.lock:
            self.responses[request_id] = future

        try:
            self.sock.sendall(json.dumps(request_obj).encode())

            # Wait for the JSON-RPC response
            try:
                msg = await asyncio.wait_for(future, timeout=7.0)
            
            except asyncio.TimeoutError:
                async with self.lock:
                    self.responses.pop(request_id, None)
                return {'status': 'error', 'message': 'Response timeout'}

            # We check if we have a 'result' or an 'error'
            if 'error' in msg:
                return {
                    'status': 'error',
                    'code': msg['error'].get('code'),
                    'message': msg['error'].get('message')
                }
            
            else:
                # For OSC responses, the data is directly in the message
                return {
                    'status': 'ok',
                    'result': msg
                }

        except Exception as e:
            self.connected = False
            return {'status': 'error', 'message': str(e)}

    async def close(self):
        """Close the connection."""
        if self.connected:
            self.connected = False
            if self.response_task:
                self.response_task.cancel()
                try:
                    await self.response_task
                except asyncio.CancelledError:
                    pass
            self.sock.close()


# Initialize the MCP server
mcp = FastMCP("Ableton Live Controller", dependencies=["python-osc"])

# Create Ableton client
ableton_client = AbletonClient()


# ----- TOOLS WITH RESPONSE -----

@mcp.tool()
async def get_track_names(index_min: Optional[int] = None, index_max: Optional[int] = None) -> str:
    """
    Get the names of tracks in Ableton Live.
    
    Args:
        index_min: Optional minimum track index
        index_max: Optional maximum track index
    
    Returns:
        A formatted string containing track names
    """
    params = {}

    if index_min is not None and index_max is not None:
        params["address"] = "/live/song/get/track_names"
        params["args"] = [index_min, index_max]
    else:
        params["address"] = "/live/song/get/track_names"
        params["args"] = []

    response = await ableton_client.send_rpc_request("send_message", params)
   
    if response['status'] == 'ok':
        # The response from send_rpc_request contains the OSC response directly in result
        result = response.get('result', {})
        if not result:
            return "No tracks found"
        track_names = result.get('args', [])
        if not track_names:
            return "No tracks found"
        return f"Track Names: {', '.join(track_names)}"
    else:
        return f"Error getting track names: {response.get('message', 'Unknown error')}"

# customized tools for better translation

@mcp.tool()
async def create_midi_track(after_index: Optional[int] = -1) -> dict:
    params = {"address": "/live/song/create_midi_track", "args": [after_index]}
    response = await ableton_client.send_rpc_request("send_message", params)
    return response

@mcp.tool()
async def create_audio_track(after_index: Optional[int] = -1) -> dict:
    params = {"address": "/live/song/create_audio_track", "args": [after_index]}
    response = await ableton_client.send_rpc_request("send_message", params)
    return response

@mcp.tool()
async def delete_track(track_index: int) -> dict:
    params = {"address": "/live/song/delete_track", "args": [track_index]}
    response = await ableton_client.send_rpc_request("send_message", params)
    return response

@mcp.tool()
async def create_clip_on_track(track_index: int, clip_index: int, length: int)  -> dict:
    params = {"address": "/live/clip_slot/create_clip", "args": [track_index, clip_index, length]}
    response = await ableton_client.send_rpc_request("send_message", params)
    return response

@mcp.tool()
async def add_notes_to_clip(track_index: int, clip_id: int, pitch: int, start_at_beat: float, length_in_beats: Optional[float] = 4, velocity: Optional[int] = 100, mute: Optional[bool] = False) -> dict:
    params = {"address": "/live/clip/add/notes", "args": [track_index, clip_id, pitch, start_at_beat, length_in_beats, velocity, mute]}
    response = await ableton_client.send_rpc_request("send_message", params)
    return response

if __name__ == "__main__":
    try:
        mcp.run()
    finally:
        asyncio.run(ableton_client.close())