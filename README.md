# News Topic Classifier

## 📌 Description
News Topic Classifier est un outil de classification thématique automatique basé sur le **Zero-Shot Learning**. Il utilise un modèle **mDeBERTa** (fine-tuné pour le *Natural Language Inference* en français) pour catégoriser des textes sans nécessiter de données d'entraînement spécifiques. 
Pour plus d'information sur la mise en place des modèles et leur évalution, veuillez consulter [notebook.ipynb](notebook.ipynb)
## 🛠 Fonctionnalités
- Scraper des articles de journaux par URL
- Obtenir un résumé de l'article
- Topic modeling de l'article
- Historique des requêtes stockées dans une base SQLite
- Interface React
## 🔧 Installation
1. Cloner le dépôt :
   ```bash
   git clone https://github.com/ton-utilisateur/TopicClassifier.git
   cd TopicClassifier
2. Lancer l'environnement virtuel:
    ```bash
   venv\Scripts\activate
3. Télécharger les modèles LLM:
   ```bash
   python download_models.py
4. Lancer l'API:
   ```bash
   python app.py
5. Lancer l'application React:
   ```bash
   cd frontend
   npm start
