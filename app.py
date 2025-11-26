from flask import Flask, request, jsonify
from flask_cors import CORS
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

app = Flask(__name__)
CORS(app)  # Allow your WordPress site to talk to this API

# 1. Initialize CAMeL Tools (Load Database once at startup)
print("Loading CAMeL Tools Database...")
db = MorphologyDB.builtin_db()
analyzer = Analyzer(db)
print("Database Loaded!")

@app.route('/analyze', methods=['GET'])
def analyze_word():
    word = request.args.get('word', '')
    
    if not word:
        return jsonify({"error": "No word provided"}), 400

    # 2. Analyze the word
    # CAMeL returns many possibilities; we take the most likely (top) one for simplicity
    analyses = analyzer.analyze(word)
    
    if not analyses:
        return jsonify({"found": False})

    # 3. Extract Best Match Data
    # In a real app, you might use a Disambiguator to pick the best one.
    # Here we pick the first result that is a "lexical" match.
    best_match = analyses[0] 
    
    result = {
        "found": True,
        "word": word,
        "root": best_match.get('root', 'N/A'),
        "pos": best_match.get('pos', 'N/A'),
        "gloss": best_match.get('gloss', 'N/A'), # English meaning
        "lemma": best_match.get('lex', 'N/A'),   # Dictionary form
        "pattern": best_match.get('pattern', 'N/A')
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)
