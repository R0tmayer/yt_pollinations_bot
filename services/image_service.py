import urllib.parse
import ssl
import random

API_KEY = None
API_TOKENS = []


async def generate_image(session, prompt, params):
    print("GENERATION_START")
    # Prefix prompt with a random number to avoid server-side caching for identical prompts
    random_prefix = str(random.randint(100000, 999999))
    prompt_with_noise = f"{random_prefix} {prompt}"
    encoded_prompt = urllib.parse.quote(prompt_with_noise)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    final_params = {}
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, bool):
            if v:
                final_params[k] = "true"
        else:
            final_params[k] = v
    # Choose token per request from provided list; assume list is present
    token = random.choice(API_TOKENS)
    headers = {"Authorization": f"Bearer {token}"}
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    try:
        async with session.get(
            url, params=final_params, headers=headers, ssl=ssl_context, timeout=300
        ) as response:
            response.raise_for_status()
            data = await response.read()
            return data
    except Exception as e:
        return None
