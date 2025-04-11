# ableton_live_mcp_server_behemoth
AbletonOscMcp only works in Claude Desktop, extnesible to other AbletonOSC commands
abletomRemoteMcp works in Claude Desktop and Cursor, 



# Ableton Osc Mcp -> https://github.com/Simon-Kansara/ableton-live-mcp-server

## Changes
I couldn't get 'get_track_names' to respond, made a few edits to the osc daemon and mcp server to send and parse track names properly.
Also added in new tools from https://github.com/simonreitinger/ableton-live-mcp-server/tree/main

## 📌 Overview

The **Ableton Live MCP Server** is a server implementing the
[Model Context Protocol (MCP)](https://modelcontextprotocol.io) to facilitate
communication between LLMs and **Ableton Live**. It uses **OSC (Open Sound
Control)** to send and receive messages to/from Ableton Live. It is based on
[AbletonOSC](https://github.com/ideoforms/AbletonOSC) implementation and
exhaustively maps available OSC adresses to
[**tools**](https://modelcontextprotocol.io/docs/concepts/tools) accessible to
MCP clients.

[![Control Ableton Live with LLMs](https://img.youtube.com/vi/12MzsQ3V7cs/hqdefault.jpg)](https://www.youtube.com/watch?v=12MzsQ3V7cs)

This project consists of two main components:

- `mcp_ableton_server.py`: The MCP server handling the communication between
  clients and the OSC daemon.
- `osc_daemon.py`: The OSC daemon responsible for relaying commands to Ableton
  Live and processing responses.

## ✨ Features

- Provides an MCP-compatible API for controlling Ableton Live from MCP clients.
- Uses **python-osc** for sending and receiving OSC messages.
- Based on the OSC implementation from
  [AbletonOSC](https://github.com/ideoforms/AbletonOSC).
- Implements request-response handling for Ableton Live commands.

## ⚡ Installation

### Requirements

- Python 3.8+
- `python-osc` (for OSC communication)
- `fastmcp` (for MCP support)
- `uv` (recommended Python package installer)
- [AbletonOSC](https://github.com/ideoforms/AbletonOSC) as a control surface

### Installation Steps

1. Install `uv` (https://docs.astral.sh/uv/getting-started/installation):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone the repository:

   ```bash
   git clone https://github.com/your-username/mcp_ableton_server.git
   cd mcp_ableton_server
   ```

3. Install the project and its dependencies:

   ```bash
   uv sync
   ```

4. Install AbletonOSC Follow the instructions at
   [AbletonOSC](https://github.com/ideoforms/AbletonOSC)

## 🚀 Usage

### Running the OSC Daemon

The OSC daemon will handle OSC communication between the MCP server and Ableton
Live:

```bash
uv run osc_daemon.py
```

This will:

- Listen for MCP client connections on port **65432**.
- Forward messages to Ableton Live via OSC on port **11000**.
- Receive OSC responses from Ableton on port **11001**.

### Example Usage

In Claude desktop, ask Claude:

- _Prepare a set to record a rock band_
- _Set the input routing channel of all tracks that have "voice" in their name
  to Ext. In 2_

## ⚙️ Configuration

By default, the server and daemon run on **localhost (127.0.0.1)** with the
following ports:

- **MCP Server Socket:** 65432
- **Ableton Live OSC Port (Send):** 11000
- **Ableton Live OSC Port (Receive):** 11001

To modify these, edit the `AbletonOSCDaemon` class in `osc_daemon.py`:

```python
self.socket_host = '127.0.0.1'
self.socket_port = 65432
self.ableton_host = '127.0.0.1'
self.ableton_port = 11000
self.receive_port = 11001
```

### Claude Desktop Configuration

To use this server with Claude Desktop, you need to configure it in your Claude
Desktop settings. The configuration file location varies by operating system:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`

Add the following configuration to your `mcpServers` section:

```json
{
  "mcpServers": {
    "Ableton Live Controller": {
      "command": "/path/to/your/project/.venv/bin/python",
      "args": ["/path/to/your/project/mcp_ableton_server.py"]
    }
  }
```

This configuration ensures that:

- The server runs with all dependencies properly managed
- The project remains portable and reproducible

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this
project.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for
details.

## Acknowledgments

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
- [python-osc](https://github.com/attwad/python-osc) for OSC handling
- Daniel John Jones for OSC implementation with
  [AbletonOSC](https://github.com/ideoforms/AbletonOSC)
- Ableton Third Party Remote Scripts
- Julien Bayle @[Structure Void](https://structure-void.com/) for endless
  inspirations and resources.

## TODO

- Explore _resources_ and _prompts_ primitives opportunities.
- Build a standalone Ableton Live MCP client.

---

# AbletonRemoteMcp
## AbletonMCP - Ableton Live Model Context Protocol Integration
[![smithery badge](https://smithery.ai/badge/@ahujasid/ableton-mcp)](https://smithery.ai/server/@ahujasid/ableton-mcp)

AbletonMCP connects Ableton Live to Claude AI through the Model Context Protocol (MCP), allowing Claude to directly interact with and control Ableton Live. This integration enables prompt-assisted music production, track creation, and Live session manipulation.

### Join the Community

Give feedback, get inspired, and build on top of the MCP: [Discord](https://discord.gg/3ZrMyGKnaU). Made by [Siddharth](https://x.com/sidahuj)

## Features

- **Two-way communication**: Connect Claude AI to Ableton Live through a socket-based server
- **Track manipulation**: Create, modify, and manipulate MIDI and audio tracks
- **Instrument and effect selection**: Claude can access and load the right instruments, effects and sounds from Ableton's library
- **Clip creation**: Create and edit MIDI clips with notes
- **Session control**: Start and stop playback, fire clips, and control transport

## Components

The system consists of two main components:

1. **Ableton Remote Script** (`Ableton_Remote_Script/__init__.py`): A MIDI Remote Script for Ableton Live that creates a socket server to receive and execute commands
2. **MCP Server** (`server.py`): A Python server that implements the Model Context Protocol and connects to the Ableton Remote Script

## Installation

### Installing via Smithery

To install Ableton Live Integration for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@ahujasid/ableton-mcp):

```bash
npx -y @smithery/cli install @ahujasid/ableton-mcp --client claude
```

### Prerequisites

- Ableton Live 10 or newer
- Python 3.8 or newer
- [uv package manager](https://astral.sh/uv)

If you're on Mac, please install uv as:
```
brew install uv
```

Otherwise, install from [uv's official website][https://docs.astral.sh/uv/getting-started/installation/]

⚠️ Do not proceed before installing UV

### Claude for Desktop Integration

[Follow along with the setup instructions video](https://youtu.be/iJWJqyVuPS8)

1. Go to Claude > Settings > Developer > Edit Config > claude_desktop_config.json to include the following:

```json
{
    "mcpServers": {
        "AbletonMCP": {
            "command": "uvx",
            "args": [
                "ableton-mcp"
            ]
        }
    }
}
```

### Cursor Integration

Run ableton-mcp without installing it permanently through uvx. Go to Cursor Settings > MCP and paste this as a command:

```
uvx ableton-mcp
```

⚠️ Only run one instance of the MCP server (either on Cursor or Claude Desktop), not both

### Installing the Ableton Remote Script

[Follow along with the setup instructions video](https://youtu.be/iJWJqyVuPS8)

1. Download the `AbletonMCP_Remote_Script/__init__.py` file from this repo

2. Copy the folder to Ableton's MIDI Remote Scripts directory. Different OS and versions have different locations. **One of these should work, you might have to look**:

   **For macOS:**
   - Method 1: Go to Applications > Right-click on Ableton Live app → Show Package Contents → Navigate to:
     `Contents/App-Resources/MIDI Remote Scripts/`
   - Method 2: If it's not there in the first method, use the direct path (replace XX with your version number):
     `/Users/[Username]/Library/Preferences/Ableton/Live XX/User Remote Scripts`
   
   **For Windows:**
   - Method 1:
     C:\Users\[Username]\AppData\Roaming\Ableton\Live x.x.x\Preferences\User Remote Scripts 
   - Method 2:
     `C:\ProgramData\Ableton\Live XX\Resources\MIDI Remote Scripts\`
   - Method 3:
     `C:\Program Files\Ableton\Live XX\Resources\MIDI Remote Scripts\`
   *Note: Replace XX with your Ableton version number (e.g., 10, 11, 12)*

4. Create a folder called 'AbletonMCP' in the Remote Scripts directory and paste the downloaded '\_\_init\_\_.py' file

3. Launch Ableton Live

4. Go to Settings/Preferences → Link, Tempo & MIDI

5. In the Control Surface dropdown, select "AbletonMCP"

6. Set Input and Output to "None"

## Usage

### Starting the Connection

1. Ensure the Ableton Remote Script is loaded in Ableton Live
2. Make sure the MCP server is configured in Claude Desktop or Cursor
3. The connection should be established automatically when you interact with Claude

### Using with Claude

Once the config file has been set on Claude, and the remote script is running in Ableton, you will see a hammer icon with tools for the Ableton MCP.

## Capabilities

- Get session and track information
- Create and modify MIDI and audio tracks
- Create, edit, and trigger clips
- Control playback
- Load instruments and effects from Ableton's browser
- Add notes to MIDI clips
- Change tempo and other session parameters

## Example Commands

Here are some examples of what you can ask Claude to do:

- "Create an 80s synthwave track" [Demo](https://youtu.be/VH9g66e42XA)
- "Create a Metro Boomin style hip-hop beat"
- "Create a new MIDI track with a synth bass instrument"
- "Add reverb to my drums"
- "Create a 4-bar MIDI clip with a simple melody"
- "Get information about the current Ableton session"
- "Load a 808 drum rack into the selected track"
- "Add a jazz chord progression to the clip in track 1"
- "Set the tempo to 120 BPM"
- "Play the clip in track 2"


## Troubleshooting

- **Connection issues**: Make sure the Ableton Remote Script is loaded, and the MCP server is configured on Claude
- **Timeout errors**: Try simplifying your requests or breaking them into smaller steps
- **Have you tried turning it off and on again?**: If you're still having connection errors, try restarting both Claude and Ableton Live

## Technical Details

### Communication Protocol

The system uses a simple JSON-based protocol over TCP sockets:

- Commands are sent as JSON objects with a `type` and optional `params`
- Responses are JSON objects with a `status` and `result` or `message`

### Limitations & Security Considerations

- Creating complex musical arrangements might need to be broken down into smaller steps
- The tool is designed to work with Ableton's default devices and browser items
- Always save your work before extensive experimentation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This is a third-party integration and not made by Ableton.
