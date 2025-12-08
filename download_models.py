from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForSequenceClassification
import torch

print("Téléchargement et sauvegarde des modèles...")
# Configuration du device
device = 0 if torch.cuda.is_available() else -1

# Téléchargement du modèle pour le topic modeling (Zero-Shot Classification)
MODEL_ID_ZERO_SHOT = "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
OUT_DIR_ZERO_SHOT = "models/mDeBERTa"

# Charger et sauvegarder le tokenizer et le modèle pour le Zero-Shot Classification
print("Téléchargement du modèle pour le Zero-Shot Classification...")
tokenizer_zero_shot = AutoTokenizer.from_pretrained(MODEL_ID_ZERO_SHOT, fix_mistral_regex=True)
model_zero_shot = AutoModelForSequenceClassification.from_pretrained(MODEL_ID_ZERO_SHOT)

# Sauvegarder le tokenizer et le modèle
tokenizer_zero_shot.save_pretrained(OUT_DIR_ZERO_SHOT)
model_zero_shot.save_pretrained(OUT_DIR_ZERO_SHOT)

# Créer un pipeline pour le Zero-Shot Classification
classifier = pipeline(
    task="zero-shot-classification",
    model=model_zero_shot,
    tokenizer=tokenizer_zero_shot,
    device=device
)

# Téléchargement du modèle pour le résumé de texte
MODEL_ID_SUMMARIZATION = "facebook/bart-large-cnn"
OUT_DIR_SUMMARIZATION = "models/bart-large-cnn"

# Charger et sauvegarder le tokenizer et le modèle pour le résumé
print("Téléchargement du modèle pour le résumé de texte...")
tokenizer_summarization = AutoTokenizer.from_pretrained(MODEL_ID_SUMMARIZATION)
model_summarization = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID_SUMMARIZATION)

# Sauvegarder le tokenizer et le modèle
tokenizer_summarization.save_pretrained(OUT_DIR_SUMMARIZATION)
model_summarization.save_pretrained(OUT_DIR_SUMMARIZATION)

# Créer un pipeline pour le résumé
summarizer = pipeline(
    task="summarization",
    model=model_summarization,
    tokenizer=tokenizer_summarization,
    device=device
)

print("Modèles téléchargés et sauvegardés avec succès.")
