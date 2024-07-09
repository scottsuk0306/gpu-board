# GPU Monitor Board

## Description

GPU Monitor Board is a web-based application that provides real-time monitoring of NVIDIA GPUs across multiple servers. It offers a user-friendly interface to track GPU utilization, memory usage, temperature, and user information for each GPU on connected servers.

## Features

- Real-time monitoring of multiple servers
- Display of GPU information including:
  - GPU index
  - GPU name
  - Temperature
  - Utilization percentage
  - Memory usage
  - Total memory
  - Current user (if available)
- Color-coded utilization for easy status identification
- Automatic updates every 60 seconds
- Tabbed interface for easy navigation between servers

## Prerequisites

- Python 3.6+
- FastAPI
- Uvicorn
- Paramiko
- NVIDIA GPU drivers installed on monitored servers

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/scottsuk0306/gpu-board.git
   cd gpu-board
   ```

2. Install the required Python packages:
   ```
   pip install fastapi uvicorn paramiko
   ```

3. Create a `config.json` file based on the `config.json.example` template:
   ```
   cp config.json.example config.json
   ```
   Edit `config.json` with your server details.

## Configuration

Edit the `config.json` file to include your server details:

```json
{
  "servers": [
    {"hostname": "server1.example.com", "username": "user1", "password": "pass1", "port": 22},
    {"hostname": "server2.example.com", "username": "user2", "port": 22, "key_filename": "path/to/key.pem"}
  ]
}
```

## Usage

1. Start the server:
   ```
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

2. Open a web browser and navigate to `http://localhost:8000`

## Security Notes

- Ensure that `config.json` is not exposed to public access.
- For production use, consider using environment variables or a secure secrets management system for sensitive information.
- Ensure that the SSH keys have appropriate permissions (typically 600).

## Contributing

Contributions to the GPU Board project are welcome. Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

MIT

## Acknowledgements

- This project uses Bootstrap for styling.
- NVIDIA-SMI is used for gathering GPU information.
