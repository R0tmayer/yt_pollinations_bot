# PollinationsAI Image Generator Bot

This repository contains a simple Python script for generating images using the [Pollinations.ai](https://pollinations.ai/) API. The project is designed as a foundation for a future Telegram bot that will generate images from text prompts.

## Features
- Reads prompts from a text file
- Generates images using Pollinations.ai API
- Saves images to the `output` directory, numbered in order
- Uses environment variables for API key management

## How to Use

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Add your Pollinations API key:**
   - Create a file named `.env` in the project root:
     ```
     POLLINATIONS_API_KEY=your_api_key_here
     ```
4. **Add prompts:**
   - Create a file named `promts.txt` in the project root. Each line should be a separate prompt.
5. **Run the script:**
   ```bash
   python main.py
   ```
6. **Find your images:**
   - Generated images will be saved in the `output` directory as `image_1.jpg`, `image_2.jpg`, etc.

## Project Structure
- `main.py` — Main script for image generation
- `requirements.txt` — Python dependencies
- `.env` — Your API key (not tracked by git)
- `output/` — Generated images (not tracked by git)
- `promts.txt` — Prompts for image generation (not tracked by git)

## About
This project is a starting point for a Telegram bot that will generate images from user prompts using Pollinations.ai. The bot functionality will be added soon. 