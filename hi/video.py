import cv2
import requests
import time

def capture_image(filename="frame.jpg"):
    print("Starting webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        raise Exception("❌ Could not open webcam.")
    
    print("📷 Align your face and wait...")
    time.sleep(2)  # Let the camera adjust
    
    # Capture a single frame
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise Exception("❌ Failed to capture image.")
    
    # Show preview for 2 seconds
    cv2.imshow("📷 Captured Image (close to continue)", frame)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    
    # Save frame
    cv2.imwrite(filename, frame)
    print("✅ Image saved:", filename)
    return filename

def analyze_emotion(image_path, api_key, api_secret):
    url = "https://api-us.faceplusplus.com/facepp/v3/detect"
    
    payload = {
        'api_key': api_key,
        'api_secret': api_secret,
        'return_attributes': 'emotion'
    }
    
    files = {'image_file': open(image_path, 'rb')}
    
    print("📡 Sending image to Face++ API...")
    response = requests.post(url, data=payload, files=files)
    result = response.json()
    
    # Debug output
    print("🔍 API response:", result)

    if 'faces' not in result or len(result['faces']) == 0:
        return "No face detected"

    emotion_data = result['faces'][0]['attributes']['emotion']
    top_emotion = max(emotion_data, key=emotion_data.get)
    
    return top_emotion

if __name__ == "__main__":
    # 🛠️ Replace with your actual Face++ API keys
    API_KEY = "your_faceplusplus_api_key"
    API_SECRET = "your_faceplusplus_api_secret"

    try:
        image_file = capture_image()
        emotion = analyze_emotion(image_file, API_KEY, API_SECRET)
        print("🎭 Detected Emotion:", emotion)
    except Exception as e:
        print("❌ Error:", str(e))
