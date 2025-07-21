import os
import requests
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("POLLINATIONS_API_KEY")
WIDTH = 1920
HEIGHT = 1080
MODEL = "gptimage"
OUTPUT_DIR = "output"
PROMPTS_FILE = "promts.txt"

def generate_image(prompt, width, height, model):
    print(f"Генерация для: {prompt}")
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    params = {
        "width": width,
        "height": height,
        "model": model,
        "nologo": "true"
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=300)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Ошибка для '{prompt}': {e}")
        return None

def save_image(image_content, image_number, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = f"image_{image_number}.jpg"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "wb") as f:
        f.write(image_content)
    print(f"Сохранено: {filepath}")

def main():
    if not API_KEY:
        print("Ошибка: API ключ не найден в .env файле.")
        return
    try:
        with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
            prompts = f.readlines()
        image_number = 1
        for prompt_line in prompts:
            prompt = prompt_line.strip()
            if not prompt:
                continue
            image_data = generate_image(prompt, WIDTH, HEIGHT, MODEL)
            if image_data:
                save_image(image_data, image_number, OUTPUT_DIR)
                image_number += 1
    except FileNotFoundError:
        print(f"Ошибка: Файл '{PROMPTS_FILE}' не найден.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()