import asyncio
import json
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, List, Union

import paramiko
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


class GPUData(BaseModel):
    index: str
    name: str
    temperature: str
    utilization: str
    memory_used: str
    memory_total: str
    user: str = "N/A"  # Default to "N/A" if no user is found


class ServerData(BaseModel):
    hostname: str
    username: str
    password: str = None
    port: int = 22
    key_filename: str = None


def load_server_config():
    config_path = Path("config.json")
    if not config_path.exists():
        raise FileNotFoundError("config.json not found")

    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    return [ServerData(**server) for server in config["servers"]]


# Use this function to load the servers
servers = load_server_config()

gpu_data: Dict[str, Union[List[GPUData], Dict[str, str]]] = {}


async def get_nvidia_smi(server: ServerData):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        connect_kwargs = {
            "hostname": server.hostname,
            "port": server.port,
            "username": server.username,
        }

        if server.password:
            connect_kwargs["password"] = server.password
        elif server.key_filename:
            connect_kwargs["key_filename"] = os.path.expanduser(server.key_filename)

        client.connect(**connect_kwargs)

        # First, get the GPU information
        stdin, stdout, stderr = client.exec_command(
            "nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits"
        )
        gpu_output = stdout.read().decode("utf-8").strip()
        gpu_error = stderr.read().decode("utf-8").strip()

        if gpu_error:
            return {"error": gpu_error}

        # Now, get the user information
        stdin, stdout, stderr = client.exec_command(
            "nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader,nounits"
        )
        user_output = stdout.read().decode("utf-8").strip()

        # Create a dictionary to store PID to user mappings
        pid_to_user = {}
        for line in user_output.split("\n"):
            if line:
                pid, _ = line.split(", ")
                stdin, stdout, stderr = client.exec_command(f"ps -o user= -p {pid}")
                user = stdout.read().decode("utf-8").strip()
                pid_to_user[pid] = user

        gpu_data = []
        for line in gpu_output.split("\n"):
            parts = line.split(", ")
            if len(parts) != 6:
                continue  # Skip this line if it doesn't have the expected number of fields

            # Find the user for this GPU
            stdin, stdout, stderr = client.exec_command(
                f"nvidia-smi --id={parts[0]} --query-compute-apps=pid --format=csv,noheader,nounits"
            )
            gpu_pid = stdout.read().decode("utf-8").strip()
            user = pid_to_user.get(gpu_pid, "N/A")

            gpu_data.append(
                GPUData(
                    index=parts[0],
                    name=parts[1],
                    temperature=parts[2],
                    utilization=parts[3],
                    memory_used=parts[4],
                    memory_total=parts[5],
                    user=user,
                )
            )

        if not gpu_data:
            return {"error": "No valid GPU data found"}

        return gpu_data

    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

    finally:
        client.close()


async def update_gpu_data():
    while True:
        for server in servers:
            gpu_data[server.hostname] = await get_nvidia_smi(server)
        await asyncio.sleep(60)  # Update every 60 seconds


def startup():
    asyncio.create_task(update_gpu_data())


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r") as f:
        return f.read()


@app.get("/gpu_data")
async def read_gpu_data():
    if not gpu_data:
        raise HTTPException(status_code=503, detail="Data not available yet")
    return gpu_data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
