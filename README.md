# 🧠 AI Memory & Personality Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-personality-engine.streamlit.app/)

A modular **Compound AI System** that solves the "Stateless AI" problem. This engine extracts long-term memory from raw conversation logs and injects dynamic personalities (from a "Stoic Sage" to an "Overprotective Indian Mom") into the AI's responses.

**[🚀 View Live Demo](https://ai-personality-engine.streamlit.app/)**

---

## 🏗️ System Architecture

Most LLM applications are stateless—they forget context instantly. This project implements a **2-Stage Pipeline** to create a persistent, character-driven experience:

### Stage 1: The "Miner" (Memory Extraction)
* **Input:** Raw, unstructured chat logs (30+ messages).
* **Process:** Uses **Google Gemini 1.5 Flash** with strict JSON output formatting to mine data.
* **Output:** A structured `UserProfile` object containing:
    * **Facts:** Hard data (Names, dates, job roles).
    * **Preferences:** Likes/Dislikes (Food, work style).
    * **Psych Profile:** Emotional triggers and stress indicators.

### Stage 2: The "Actor" (Personality Engine)
* **Input:** The `UserProfile` (Memory) + Active Persona + New User Message.
* **Process:** A RAG-style context injection system dynamically assembles a System Prompt.
* **Output:** A highly personalized response that references past context in a specific voice.

---

## ✨ Key Features

* **🧠 Automated Fact Extraction:** Turns chaotic chat history into structured JSON automatically.
* **🎭 Dynamic Persona Switching:** Instantly swap between radically different personalities:
    * **Witty Friend:** Gen-Z slang, sarcasm, and emojis.
    * **Stoic Mentor:** Marcus Aurelius-style wisdom and discipline.
    * **Indian Mom:** Aggressively loving, food-obsessed, and health-conscious.
* **🛡️ Type Safety:** Uses **Pydantic** models to strictly validate data structure, preventing AI hallucinations.
* **🔐 Secure Architecture:** Environment variable management using `.env` (Local) and `st.secrets` (Cloud).

---

## 🛠️ Tech Stack

* **Core Logic:** Python 3.11+
* **LLM Provider:** Google Gemini 1.5 Flash (via `google-generativeai`)
* **Interface:** Streamlit
* **Data Validation:** Pydantic
* **Environment:** Python-Dotenv

---

## 📂 Project Structure

```bash
/ai-personality-engine
├── app.py             # Main Streamlit Application (The Interface)
├── memory.py          # Memory Module (Extracts facts using Gemini)
├── persona.py         # Personality Engine (Injects character & context)
├── models.py          # Data Contracts (Pydantic Class Definitions)
├── requirements.txt   # Dependencies
├── .env               # API Keys (Not pushed to GitHub)
└── README.md          # Documentation
