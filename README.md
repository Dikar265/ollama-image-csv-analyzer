This project provides an API powered by FastAPI and Ollama for analyzing images and CSV files using LLMs.  
It supports optional GPU acceleration with NVIDIA cards for faster inference.

---

## Requirements

- Docker Desktop: https://www.docker.com/products/docker-desktop/
- WSL2 (for Windows users): https://learn.microsoft.com/en-us/windows/wsl/install
- At least 8 GB RAM recommended
- (Optional) NVIDIA GPU for acceleration

---

## Running the Project

### 1. Clone the Repository

git clone https://github.com/your-user/image-lecture-seo-api.git
cd image-lecture-seo-api

### 2. Start the Services

With Docker Compose:

docker compose up -d

- The Ollama service will run on port 11434
- The FastAPI backend will run on port 8000

Visit the API docs at:
http://localhost:8000/docs

---

## Using GPU (optional but recommended)

If you have an NVIDIA GPU (e.g., RTX 4070), you can enable GPU acceleration so the model runs much faster.

### Step 1: Install NVIDIA Container Toolkit in WSL2

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

### Step 2: Verify that Docker detects your GPU

docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi

If successful, you should see a table with your GPU information (name, memory, usage, temperature, etc.).

---

## Example Endpoints

### Analyze an Image

POST /analyze-image/
Content-Type: multipart/form-data
file: <upload your image>

### Analyze a CSV File

POST /analyze-csv/
Content-Type: multipart/form-data
file: <upload your CSV>

---

## Notes

- If no GPU is available, the project will automatically fall back to CPU.
- Running on CPU is slower, especially for large models.
- Make sure your WSL2 distribution has Docker integration enabled in Docker Desktop settings.
