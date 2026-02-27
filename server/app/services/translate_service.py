import requests


def translate_text(text, target_lang):
    """Translate text using Google Translate API."""
    url = (
        f'https://translate.googleapis.com/translate_a/single'
        f'?client=gtx&sl=auto&tl={target_lang}&dt=t&q={requests.utils.quote(text)}'
    )

    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        raise ValueError('Translation API error')

    data = resp.json()
    if isinstance(data, list) and isinstance(data[0], list) and isinstance(data[0][0], list):
        return data[0][0][0]

    raise ValueError('Unexpected translation API response')
