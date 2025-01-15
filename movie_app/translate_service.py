import requests
from django.core.cache import cache

API_KEY = 'AIzaSyCXAjqoTv7w2jCJO2Gb7AwAjmYRviAl3bU'



def translate_text(target_language, text):

    cache_key = f"translation_{text}_{target_language}"
    cached_translation = cache.get(cache_key)


    if cached_translation:
        return cached_translation

    url = f'https://translation.googleapis.com/language/translate/v2?key={API_KEY}'


    chunks = [text[i:i + 5000] for i in range(0, len(text), 5000)]
    translated_chunks = []

    for chunk in chunks:
        params = {
            'q': chunk,
            'target': target_language,
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            result = response.json()
            translated_text = result['data']['translations'][0]['translatedText']
            translated_chunks.append(translated_text)
        else:
            print("Błąd tłumaczenia:", response.json())  # Debug: Wyświetl błąd z API
            return text  # Jeśli wystąpił błąd, zwróć oryginalny tekst


    full_translation = ''.join(translated_chunks)


    cache.set(cache_key, full_translation, timeout=86400)

    return full_translation