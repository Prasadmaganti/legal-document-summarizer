from transformers import MarianMTModel, MarianTokenizer

# Expanded language support for your project
MODELS = {
    "hi": "Helsinki-NLP/opus-mt-hi-en",    # Hindi
    "fr": "Helsinki-NLP/opus-mt-fr-en",    # French
    "de": "Helsinki-NLP/opus-mt-de-en",    # German
    "es": "Helsinki-NLP/opus-mt-es-en",    # Spanish
    "te": "Helsinki-NLP/opus-mt-mul-en"   # Multilingual model (supports Telugu)
}

def translate_to_english(text, lang_code):
    # If language is English or not in our list, return original text
    if lang_code == 'en' or lang_code not in MODELS:
        return text

    model_name = MODELS[lang_code]
    
    # Load model and tokenizer
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # Legal documents are long; use truncation and padding
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    
    # Generate translation
    translated_tokens = model.generate(**inputs)
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    
    return translated_text