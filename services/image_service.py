import urllib.parse
import ssl

API_KEY = None

async def generate_image(session, prompt, params):
    encoded_prompt = urllib.parse.quote(prompt)
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
    headers = {"Authorization": f"Bearer {API_KEY}"}
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    try:
        async with session.get(url, params=final_params, headers=headers, ssl=ssl_context, timeout=300) as response:
            response.raise_for_status()
            return await response.read()
    except Exception as e:
        print(f"Ошибка генерации для промта '{prompt}': {e}")
        return None 