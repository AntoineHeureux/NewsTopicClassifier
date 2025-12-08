from transformers import AutoTokenizer, pipeline
import torch

OUT_DIR = "models/mDeBERTa"
device = 0 if torch.cuda.is_available() else -1

# Liste des topics pour la classification zéro-shot
zeroshot_topic_list = [
"Politique",
"Économie & finance",
"Santé publique & médecine",
"Sécurité & criminalité",
"Environnement & climat",
"Science & technologie",
"Société & culture",
]

# recharger le tokenizer en appliquant le fix
tokenizer = AutoTokenizer.from_pretrained(OUT_DIR, fix_mistral_regex=True)

classifier = pipeline(
    task="zero-shot-classification",
    model=OUT_DIR,
    tokenizer=tokenizer,
    device=device,
    multi_label=True,
    dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
def get_topic(text: str) -> str:
    result = classifier(
    sequences=text,
    candidate_labels=zeroshot_topic_list,
    hypothesis_template="Ce texte parle de {}."
    )
    print(result)
    return result['labels'][0]