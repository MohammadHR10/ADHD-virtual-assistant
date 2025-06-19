# ADHD Virtual Assistant

![License](https://img.shields.io/github/license/MohammadHR10/ADHD-virtual-assistant)

An AI-powered virtual assistant designed specifically to support individuals with ADHD. This tool helps with routine management, time awareness, task organization, and provides ADHD-friendly advice.

## ✨ Features

- 💬 **Natural Conversation**: Chat naturally with an AI assistant trained to understand ADHD challenges
- ⏰ **Routine Tracking**: Log and get assistance with daily routines
- 🍔 **Meal Planning**: Get ADHD-friendly meal suggestions based on preferences
- 🎯 **Task Management**: Break down complex tasks into manageable steps
- 🎤 **Voice Input** (Local version only): Speak to your assistant using speech recognition

## 🚀 Quick Start

### Prerequisites

- Python
- pip package manager

### Installation

1. Clone the repository

   ```bash
   git clone https://github.com/MohammadHR10/ADHD-virtual-assistant.git
   cd ADHD-virtual-assistant
   ```

2. Set up a virtual environment

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies

   ```bash
   pip install -r hi/requirements.txt
   ```

4. Set up environment variables
   - Create a `.env` file in the project root
   ```
   GROQ_API_KEY=your_groq_api_key_here
   BACKEND_URL=http://localhost:5001/chat
   ```

## 🏃‍♀️ Running the Application

1. Start the backend server

   ```bash
   python hi/backend.py
   ```

2. Start the frontend (in a new terminal window)

   ```bash
   streamlit run hi/frontend2.py
   ```

3. Open your browser and navigate to:
   - http://localhost:8501

## 🐳 Running with Docker

You can run the application using Docker and Docker Compose for an isolated and reproducible environment.

### Quick Start with Docker Compose

1. **Prerequisites**

   - [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed

2. **Set up environment variables**

   - Create a `.env` file in the project root:

   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Build and run containers**

   ```bash
   docker compose build
   docker compose up -d
   ```

4. **Access the application**

   - Open [http://localhost:8501](http://localhost:8501) in your browser

5. **Stop the application**
   ```bash
   docker compose down
   ```

### Docker Environment Configuration

#### Required Environment Variables

- `GROQ_API_KEY`: Your API key for Groq LLM access

#### Setting Environment Variables

1. **Using .env file (recommended)**

   - Create a `.env` file in the project root (this will not be committed to git)

   ```
   GROQ_API_KEY=sk-your-real-key
   ```

2. **At runtime**

   ```bash
   GROQ_API_KEY=sk-your-real-key docker compose up -d
   ```

3. **In docker-compose.yml** (not recommended for secrets)
   ```yaml
   services:
     backend:
       environment:
         - GROQ_API_KEY=sk-your-real-key
   ```

#### Optional Environment Variables

- `BACKEND_URL`: Override the backend API endpoint
  - Default: `http://backend:5001/chat` (when using Docker Compose)
  - Example override in docker-compose.yml:
    ```yaml
    frontend:
      environment:
        - BACKEND_URL=http://custom-backend:5001/chat
    ```

### Docker Troubleshooting

- **View logs**

  ```bash
  docker compose logs backend
  docker compose logs frontend
  ```

- **Rebuild after code changes**

  ```bash
  docker compose build
  docker compose up -d
  ```

- **Test backend health**
  ```bash
  curl http://localhost:5001/health
  ```

### Advanced: Manual Docker Setup

For more control over container networking and configuration:

1. **Create a custom network**

   ```bash
   docker network create adhd-assistant
   ```

2. **Run backend container**

   ```bash
   docker run --name adhd-backend \
     --network adhd-assistant \
     -p 5001:5001 \
     -e GROQ_API_KEY=sk-your-real-key \
     -d adhd-virtual-assistant-backend
   ```

3. **Run frontend container**

   ```bash
   docker run --name adhd-frontend \
     --network adhd-assistant \
     -p 8501:10000 \
     -e BACKEND_URL=http://adhd-backend:5001/chat \
     -d adhd-virtual-assistant-frontend
   ```

4. **Stop and remove containers**
   ```bash
   docker stop adhd-frontend adhd-backend
   docker rm adhd-frontend adhd-backend
   ```

---

## 🧠 How It Works

The ADHD Virtual Assistant uses LLM technology to provide personalized support:

1. **Input Analysis**: Your messages are analyzed for ADHD-related concerns
2. **Contextual Response**: Responses are tailored to be ADHD-friendly (clear, concise, supportive)
3. **Memory**: The system remembers your routines and challenges to provide consistent support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b Branch_Name`)
3. Commit your changes (`git commit -m "Describe what you changed"`)
4. Push to the branch (`git push origin Branch_Name`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
