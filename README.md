# TopicClassifier

**Classification thématique de textes par Zero-Shot Learning avec mDeBERTa**

---

## 📌 Description
TopicClassifier est un outil de classification thématique automatique basé sur le **Zero-Shot Learning**. Il utilise le modèle **mDeBERTa** (fine-tuné pour le *Natural Language Inference* en français) pour catégoriser des textes sans nécessiter de données d'entraînement spécifiques. L'application permet également de résumer l'article via le modèle BART. Le tout est présenté par une interface react et stocke les résultats dans une base de données.
Pour plus d'information sur la mise en place des modèles et leur évalution, veuillez consulter notebook.ipynb
---

## 🛠 Fonctionnalités
- Scraper des articles de journaux par URL
- Obtenir une résumé de l'article
- Topic modeling de l'article
- Historique des requêtes contenues dans une base SQLite

### Étapes
1. Cloner le dépôt :
   ```bash
   git clone https://github.com/ton-utilisateur/TopicClassifier.git
   cd TopicClassifier

2. Télécharger les modèles LLM:
   ```bash
   python download_models.py

2. Lancer l'API:
   ```bash
   python app.py

3. Lancer l'application React:
   ```bash
   cd frontend
   npm start
   
