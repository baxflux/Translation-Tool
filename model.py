from transformers import MarianMTModel, MarianTokenizer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_name = "Helsinki-NLP/opus-mt-en-vi"
try:
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    logger.info(f"Successfully loaded model {model_name}")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise

def translate(texts):
    try:
        if isinstance(texts, str):
            texts = [texts]
        if not texts or any(not text.strip() for text in texts):
            logger.error("Empty or invalid input")
            return {"error": "Input text cannot be empty"}
        
        inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
        translated = model.generate(**inputs)
        translated_texts = tokenizer.batch_decode(translated, skip_special_tokens=True)
        
        logger.info(f"Successfully translated {len(texts)} sentences")
        return translated_texts
    except Exception as e:
        logger.error(f"Error during translation: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    sample_texts = [
        "The weather is nice today.",
        "The API endpoint is secure."
    ]
    results = translate(sample_texts)
    if isinstance(results, dict) and "error" in results:
        print(f"Error: {results['error']}")
    else:
        for original, translated in zip(sample_texts, results):
            print(f"Original: {original}")
            print(f"Translated: {translated}\n")
