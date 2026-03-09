import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Use BART specifically for legal/long-form text
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def summarize_text(text):
    # Split text into manageable chunks for the model (max 1024 tokens)
    # 3000 characters is a safe chunk size for BART
    max_chunk = 3000 
    chunks = [text[i:i + max_chunk] for i in range(0, len(text), max_chunk)]
    
    full_summary = []
    
    for chunk in chunks:
        if len(chunk) < 100:
            continue
            
        # Tokenize and generate
        inputs = tokenizer([chunk], max_length=1024, return_tensors="pt", truncation=True)
        
        # Generate summary IDs
        summary_ids = model.generate(
            inputs["input_ids"], 
            num_beams=4, 
            max_length=150, 
            min_length=50, 
            early_stopping=True
        )
        
        # Decode back to text
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        full_summary.append(summary)
    
    return " ".join(full_summary)