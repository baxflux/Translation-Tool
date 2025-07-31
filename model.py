from transformers import MarianMTModel, MarianTokenizer
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    with open('it_glossary.json', 'r', encoding='utf-8') as f:
        it_glossary = json.load(f)
    logger.info("Loaded IT glossary")
except FileNotFoundError:
    it_glossary = {}
    logger.warning("IT glossary not found, using default translation")

model_name = "Helsinki-NLP/opus-mt-en-vi"
try:
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    logger.info(f"Successfully loaded model {model_name}")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise

def apply_glossary(text, glossary):
    for en_term, vi_term in glossary.items():
        text = text.replace(en_term, vi_term)
    return text

def translate(texts):
    try:
        if isinstance(texts, str):
            texts = [texts]
        if not texts or any(not text.strip() for text in texts):
            logger.error("Empty or invalid input")
            return {"error": "Input text cannot be empty"}
        
        texts = [apply_glossary(text, it_glossary) for text in texts]
        
        inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
        translated = model.generate(**inputs)
        translated_texts = tokenizer.batch_decode(translated, skip_special_tokens=True)
        
        logger.info(f"Successfully translated {len(texts)} sentences")
        return translated_texts
    except Exception as e:
        logger.error(f"Error during translation: {e}")
        return {"error": str(e)}