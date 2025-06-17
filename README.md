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
