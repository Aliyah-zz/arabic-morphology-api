from flask import Flask, request, jsonify
from flask_cors import CORS
from tashaphyne.stemming import ArabicLightStemmer
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app)

# Initialize the lightweight stemmer once
print("Initializing Tashaphyne...")
stemmer = ArabicLightStemmer()
print("Ready.")

@app.route('/analyze', methods=['GET'])
def analyze_word():
    word = request.args.get('word', '')
    
    if not word:
        return jsonify({"error": "No word provided"}), 400

    try:
        # 1. Clean the word (basic normalization)
        # Tashaphyne handles some of this, but good to be safe
        clean_word = word.strip()

        # 2. Get Root and Stem using Tashaphyne
        stemmer.light_stem(clean_word)
        root = stemmer.get_root()
        stem = stemmer.get_stem()

        # 3. Get Meaning using Google Translate
        # We translate to English ('en')
        gloss = GoogleTranslator(source='ar', target='en').translate(clean_word)

        # 4. Return Data (Matching the structure your Plugin expects)
        return jsonify({
            "found": True,
            "word": word,
            "root": root,       # The 3-letter root (e.g., k-t-b)
            "lemma": stem,      # The stem
            "gloss": gloss,     # The English meaning
            "pos": "Word"       # Tashaphyne doesn't do POS tagging, so we send a generic label
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"found": False, "error": str(e)})

if __name__ == '__main__':
    app.run(port=5000)
