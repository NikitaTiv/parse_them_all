import io

from flask import Flask, request, jsonify
from PIL import Image
import pytesseract


app = Flask(__name__)


@app.route('/ocr', methods=['POST'])
def ocr():
    image = Image.open(io.BytesIO(request.data))
    text = pytesseract.image_to_string(image)
    return jsonify({'text': text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
