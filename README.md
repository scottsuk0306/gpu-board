# 🖥️ GPU Monitor Board

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)

## 📋 Description

GPU Monitor Board is a cutting-edge web application that provides real-time monitoring of NVIDIA GPUs across multiple servers. With its intuitive interface, you can effortlessly track GPU utilization, memory usage, temperature, and user information for each GPU on connected servers.

## ✨ Features

- 🔄 Real-time monitoring of multiple servers
- 📊 Comprehensive GPU information display:
  - GPU index and name
  - Temperature
  - Utilization percentage
  - Memory usage and total memory
  - Current user (if available)
- 🎨 Color-coded utilization for quick status identification
- ⏱️ Automatic updates every 60 seconds
- 📑 Tabbed interface for seamless navigation between servers

## 🛠️ Prerequisites

- Python 3.9+
- FastAPI
- Uvicorn
- Paramiko
- NVIDIA GPU drivers installed on monitored servers

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/scottsuk0306/gpu-board.git
   cd gpu-board
   ```

2. Install the required Python packages:
   ```bash
   pip install fastapi uvicorn paramiko
   ```

3. Create a `config.json` file based on the provided template:
   ```bash
   cp config.json.example config.json
   ```
   Edit `config.json` with your server details.

## ⚙️ Configuration

Edit the `config.json` file to include your server details:

```json
{
  "servers": [
    {"hostname": "server1.example.com", "username": "user1", "password": "pass1", "port": 22},
    {"hostname": "server2.example.com", "username": "user2", "port": 22, "key_filename": "path/to/key.pem"}
  ]
}
```

## 🖱️ Usage

1. Start the server:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

2. Open a web browser and navigate to `http://localhost:8000`

## 🔒 Security Notes

- Ensure that `config.json` is not exposed to public access.
- For production use, consider using environment variables or a secure secrets management system for sensitive information.
- Ensure that the SSH keys have appropriate permissions (typically 600).

## 🤝 Contributing

Contributions to the GPU Monitor Board project are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- This project uses [Bootstrap](https://getbootstrap.com/) for styling.
- [NVIDIA-SMI](https://developer.nvidia.com/nvidia-system-management-interface) is used for gathering GPU information.

## 📞 Support

If you encounter any issues or have questions, please [open an issue](https://github.com/scottsuk0306/gpu-board/issues) on our GitHub repository.

## 🚀 Roadmap

- [ ] Support installation through pip
