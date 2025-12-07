from transformers import BartForConditionalGeneration, BartTokenizer, pipeline

path = 'models/bart-large-cnn'

summarizer = pipeline("summarization", 
                      model= BartForConditionalGeneration.from_pretrained(path),
                      tokenizer=BartTokenizer.from_pretrained(path))

def get_summary(text:str) -> str:
    summary = summarizer(text, max_length=200, min_length=30, do_sample=False)
    return summary[0]['summary_text']