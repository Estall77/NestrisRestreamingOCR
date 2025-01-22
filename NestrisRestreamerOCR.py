import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import joblib
import time

class OCR:
    def __init__(self, model=None):
        self.model = model if model else KNeighborsClassifier(n_neighbors=3)

    def load_dataset(self, data_dir):
        start_time = time.time()
        X, y = [], []
        for label in os.listdir(data_dir):
            label_dir = os.path.join(data_dir, label)
            for img_name in os.listdir(label_dir):
                img_path = os.path.join(label_dir, img_name)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                img = cv2.resize(img, (28, 28))  # Resize to 28x28
                X.append(img.flatten())         # Flatten image
                y.append(label)                 # Add label
        elapsed_time = time.time() - start_time
        print(f"load_dataset took {elapsed_time:.2f} seconds")
        return np.array(X), np.array(y)

    def train(self, X, y, test_size=0.2, random_state=42):
        start_time = time.time()
        # Normalize pixel values to [0, 1]
        X = X / 255.0
        # Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        # Train the model
        self.model.fit(X_train, y_train)
        # Evaluate the model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        elapsed_time = time.time() - start_time
        print(f"train took {elapsed_time:.2f} seconds. Accuracy on test set: {accuracy:.2f}")
        return accuracy

    def predict(self, imgs):
        
        # Ensure imgs is a list of images
        if not isinstance(imgs, list):
            imgs = [imgs]
        
        # Preprocess images: resize, flatten, and normalize
        processed_imgs = [cv2.resize(img, (28, 28)).flatten() / 255.0 for img in imgs]
        
        # Batch predict
        predictions = self.model.predict(processed_imgs)
                
        return predictions if len(imgs) > 1 else predictions[0]

    def save_model(self, path):
        start_time = time.time()
        joblib.dump(self.model, path)
        elapsed_time = time.time() - start_time
        print(f"save_model took {elapsed_time:.2f} seconds")

    def load_model(self, path):
        start_time = time.time()
        self.model = joblib.load(path)
        elapsed_time = time.time() - start_time
        print(f"load_model took {elapsed_time:.2f} seconds")

    def predict_number(self, img):
        
        # Segment digits from the input image
        digits = self.segment_digits(img)
        
        # Batch predict for all segmented digits
        predictions = self.predict(digits)  # `self.predict` now handles lists of images
        
        # Join predictions to form the result string
        if isinstance(predictions, list):  # Ensure compatibility with batch output
            result = ''.join(predictions)
        else:  # Handle single prediction case gracefully
            result = str(predictions)
        result = ''.join(map(str, predictions))

        
        return result


    def segment_digits(self, img):
        if len(img.shape) == 3 and img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Apply binary thresholding
        _, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Filter and sort contours from left to right
        digit_contours = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = h / w
            if 0.5 < aspect_ratio < 5:  # Aspect ratio filter for digits
                digit_contours.append((x, y, w, h))
        digit_contours = sorted(digit_contours, key=lambda b: b[0])  # Sort by x-coordinate

        # Extract each digit and save as an image
        digits = []
        for i, (x, y, w, h) in enumerate(digit_contours):
            digit = img[y-1:y+h+1, x:x+w]  # Crop the digit
            digit_resized = cv2.resize(digit, (28, 28))  # Resize to 28x28
            digits.append(digit_resized)

        return digits
