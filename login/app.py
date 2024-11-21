from flask import Flask, request, jsonify
import requests
import io
from PIL import Image
import os

app = Flask(__name__)

# Set your Unsplash API key
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY", "1n7sSMtCh8Hs_MrBOjhQ1SygTDA-BJ550UdX3rwLYZQ")

@app.route('/generate-image', methods=['POST'])
def generate_image():
    category = request.json.get('category')
    if not category:
        return jsonify({"error": "No category provided"}), 400

    try:
        url = f"https://api.unsplash.com/photos/random?query={category}&orientation=landscape&client_id=1n7sSMtCh8Hs_MrBOjhQ1SygTDA-BJ550UdX3rwLYZQ"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        img_data = requests.get(data["urls"]["regular"]).content
        image = Image.open(io.BytesIO(img_data))
        image.save("output.jpg")  # Save image for display

        return jsonify({"image_url": "output.jpg"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Running on port 5000
