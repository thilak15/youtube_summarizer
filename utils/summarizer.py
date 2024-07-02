from transformers import PegasusForConditionalGeneration, PegasusTokenizer

model_name = "google/pegasus-xsum"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

def summarize_text(text, max_length=150, min_length=50, chunk_size=1024):
    try:
        # Ensure text is not too short for summarization
        if len(text) < 20:
            raise ValueError("Input text is too short for summarization.")
        
        # Split text into manageable chunks
        def chunk_text(text, size):
            return [text[i:i + size] for i in range(0, len(text), size)]
        
        text_chunks = chunk_text(text, chunk_size)
        summaries = []

        for chunk in text_chunks:
            inputs = tokenizer(chunk, return_tensors="pt", max_length=chunk_size, truncation=True)
            summary_ids = model.generate(inputs.input_ids, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(summary)

        # Combine summaries
        combined_summary = " ".join(summaries)
        return combined_summary
    except Exception as e:
        print(f"Error in summarization: {str(e)}")
        raise Exception(f"Error summarizing text: {e}")
