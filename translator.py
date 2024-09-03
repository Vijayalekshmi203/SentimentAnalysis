#pip install langdetect
#pip install deep-translator

from deep_translator import MyMemoryTranslator
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0

LANGUAGE_CODE_MAP = {
    'en': 'en-GB',  # English (UK)
    'ta': 'ta-IN',  # Tamil (India)
    'hi': 'hi-IN',  # Hindi (India)
    'es': 'es-ES',  # Spanish (Spain)
    'fr': 'fr-FR',  # French (France)
    'de': 'de-DE',  # German (Germany)
    'zh-cn': 'zh-CN',  # Chinese Simplified (China)
    'ar': 'ar-SA',  # Arabic (Saudi Arabia)
    'ru': 'ru-RU',  # Russian (Russia)
    'ja': 'ja-JP',  # Japanese (Japan)
    'ko': 'ko-KR',  # Korean (South Korea)
    'pt': 'pt-PT',  # Portuguese (Portugal)
    'pt-br': 'pt-BR',  # Portuguese (Brazil)
    'it': 'it-IT',  # Italian (Italy)
    'nl': 'nl-NL',  # Dutch (Netherlands)
    'pl': 'pl-PL',  # Polish (Poland)
    'sv': 'sv-SE',  # Swedish (Sweden)
    'fi': 'fi-FI',  # Finnish (Finland)
    'el': 'el-GR',  # Greek (Greece)
    'tr': 'tr-TR',  # Turkish (Turkey)
    'th': 'th-TH',  # Thai (Thailand)
    'vi': 'vi-VN',  # Vietnamese (Vietnam)
    'ms': 'ms-MY',  # Malay (Malaysia)
    'id': 'id-ID',  # Indonesian (Indonesia)
    'he': 'he-IL',  # Hebrew (Israel)
    'uk': 'uk-UA',  # Ukrainian (Ukraine)
    'cs': 'cs-CZ',  # Czech (Czech Republic)
    'hu': 'hu-HU',  # Hungarian (Hungary)
    'ro': 'ro-RO',  # Romanian (Romania)
    'bg': 'bg-BG',  # Bulgarian (Bulgaria)
    'hr': 'hr-HR',  # Croatian (Croatia)
    'sk': 'sk-SK',  # Slovak (Slovakia)
    'sl': 'sl-SI',  # Slovenian (Slovenia)
    'lt': 'lt-LT',  # Lithuanian (Lithuania)
    'lv': 'lv-LV',  # Latvian (Latvia)
    'et': 'et-EE',  # Estonian (Estonia)
    'bn': 'bn-IN',  # Bengali (India)
    'pa': 'pa-IN',  # Punjabi (India)
    'gu': 'gu-IN',  # Gujarati (India)
    'kn': 'kn-IN',  # Kannada (India)
    'ml': 'ml-IN',  # Malayalam (India)
    'mr': 'mr-IN',  # Marathi (India)
    'te': 'te-IN',  # Telugu (India)
    'ur': 'ur-PK',  # Urdu (Pakistan)
    'fa': 'fa-IR',  # Persian (Iran)
    'sw': 'sw-KE',  # Swahili (Kenya)
    'zu': 'zu-ZA',  # Zulu (South Africa)
    'xh': 'xh-ZA',  # Xhosa (South Africa)
    'af': 'af-ZA',  # Afrikaans (South Africa)
    'cy': 'cy-GB',  # Welsh (United Kingdom)
    'az': 'az-AZ',  # Azerbaijani (Azerbaijan)
    'ps': 'ps-AF',  # Pashto (Afghanistan)
    'ne': 'ne-NP',  # Nepali (Nepal)
    'jv': 'jv-ID',  # Javanese (Indonesia)
    'tl': 'tl-PH',  # Tagalog (Philippines)
    'sq': 'sq-AL',  # Albanian (Albania)
    'bs': 'bs-BA',  # Bosnian (Bosnia and Herzegovina)
    'mk': 'mk-MK',  # Macedonian (North Macedonia)
    'sr': 'sr-RS',  # Serbian (Serbia)
    'ca': 'ca-ES',  # Catalan (Spain)
    'sa': 'sa-IN',  # Sanskrit (India)
    'rw': 'rw-RW',  # Kinyarwanda (Rwanda)
}

def validate_text_length(text):
    """Validate text length for translation."""
    max_length=499
    if len(text) > max_length:
        return text[:max_length]
    return text

def translate_text(text):
    if not text:
        raise ValueError('No text provided')

    try:
        # Detect the language
        detected_language = detect(text)
    except LangDetectException:
        raise ValueError('Could not detect language')

    # Map the detected language to MyMemoryTranslator supported code
    source_language = LANGUAGE_CODE_MAP.get(detected_language, detected_language)
    
    if source_language not in LANGUAGE_CODE_MAP.values():
        raise ValueError(f'Unsupported language: {detected_language}')

    # Translate the text to English
    translator = MyMemoryTranslator(source=source_language, target='en-GB')
    translation = translator.translate(text)
    return translation


'''
def detect_lang(text):
    detected_language = detect(text)
    if detected_language == "en-GB":
        
'''