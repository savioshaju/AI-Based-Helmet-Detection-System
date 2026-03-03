import os
import cv2
import base64
import tempfile
import numpy as np
from flask import Flask, render_template, request, Response, jsonify
from ultralytics import YOLO

app = Flask(__name__)

MODEL_PATH = r"D:\Savio Shaju\AI-Based Helmet Detection System\runs\detect\train2\weights\best.pt"
model = YOLO(MODEL_PATH)

webcam_active = False

def process_frame(frame):
    results = model(frame)
    return results[0].plot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    np_img = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({'error': 'Invalid image format'}), 400

    annotated_img = process_frame(img)
    _, buffer = cv2.imencode('.jpg', annotated_img)
    encoded_img = base64.b64encode(buffer).decode('utf-8')

    return jsonify({'image': encoded_img})

def generate_video_frames(filepath):
    cap = cv2.VideoCapture(filepath)
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            annotated_frame = process_frame(frame)
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' +
                   buffer.tobytes() + b'\r\n')
    finally:
        cap.release()
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No video provided", 400

    file = request.files['video']
    if file.filename == '':
        return "No selected file", 400

    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    file.save(temp.name)
    temp.close()

    return Response(generate_video_frames(temp.name),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_webcam_frames():
    global webcam_active
    cap = cv2.VideoCapture(0)
    try:
        while webcam_active:
            success, frame = cap.read()
            if not success:
                break
            annotated_frame = process_frame(frame)
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' +
                   buffer.tobytes() + b'\r\n')
    finally:
        cap.release()
        webcam_active = False

@app.route('/webcam_feed')
def webcam_feed():
    global webcam_active
    webcam_active = True
    return Response(generate_webcam_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_webcam', methods=['POST'])
def stop_webcam():
    global webcam_active
    webcam_active = False
    return jsonify({'status': 'stopped'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')