from NestrisRestreamerOCR import OCR
from PIL import ImageGrab
import numpy as np
import time

PLAYER_ONE_SCORE_BBOX = (787, 160, 930, 191)
PLAYER_TWO_SCORE_BBOX = (1090, 160, 1233, 191)
SCORE_DIFF_FILE_1 = "score_difference_1.txt"
SCORE_DIFF_FILE_2 = "score_difference_2.txt"

# Initialize the OCR
ocr = OCR() 
ocr.load_model('knn_model.pkl')  # Load the pre-trained model

# A function to read and process the score image, then convert it
def read_score(bbox):
    start_time = time.time()
    try:
        im = ImageGrab.grab(bbox=bbox, include_layered_windows=False, all_screens=False)
        im = np.array(im)
        score_str = ocr.predict_number(im).strip()
        print(f"Read value: {score_str}")
        elapsed_time = time.time() - start_time
        print(f"read_score took {elapsed_time:.2f} seconds")
        return convert_hex_number(score_str)
    except Exception as e:
        print(f"Error reading score: {e}")
        elapsed_time = time.time() - start_time
        print(f"read_score (with error) took {elapsed_time:.2f} seconds")
        return None

# A function to convert hex values to integers
def convert_hex_number(hex_number):
    # Handle the first digit (hexadecimal)
    first_digit = hex_number[0].upper()
    try:
        first_digit_value = int(first_digit, 16)  # Convert the first digit to decimal
    except ValueError:
        print(f"Invalid first digit: {first_digit}")
        return None
    
    # Handle the remaining five digits (base 10)
    remaining_digits = hex_number[1:]
    sanitized_digits = ""
    for i in range(len(remaining_digits)):
        char = remaining_digits[i]
        if char == 'D':
            sanitized_digits += '0'
        elif i > 0 and (remaining_digits[i - 1:i + 1] == 'C3' or remaining_digits[i - 1:i + 1] == 'C5'):  # Check for 'C3'
            sanitized_digits = sanitized_digits[:-1] + '0'
        elif char == 'B':
            sanitized_digits += '8'
        else:
            sanitized_digits += char

    try:
        remaining_value = int(sanitized_digits)  # Convert the sanitized remaining digits to an integer
    except ValueError:
        print(f"Invalid remaining digits: {sanitized_digits}")
        return None

    # Combine the two parts into a single value
    result = first_digit_value * 100000 + remaining_value

    print(result)
    return result

# Function to calculate and save the score differences
def calculate_and_save_score_difference(player_one_score, player_two_score):
    start_time = time.time()
    if player_one_score is not None and player_two_score is not None:
        if player_one_score > player_two_score:
            score_difference_1 = f"+{player_one_score - player_two_score}"
            score_difference_2 = f"{player_two_score - player_one_score}"
        elif player_two_score == player_one_score:
            score_difference_1 = "0"
            score_difference_2 = "0"
        else:
            score_difference_1 = f"{player_one_score - player_two_score}"
            score_difference_2 = f"+{player_two_score - player_one_score}"

        # Writing the score difference only if it has changed
        with open(SCORE_DIFF_FILE_1, "w") as file_1:
            file_1.write(f"Score Difference: {score_difference_1}\n")
        with open(SCORE_DIFF_FILE_2, "w") as file_2:
            file_2.write(f"Score Difference: {score_difference_2}\n")
    elapsed_time = time.time() - start_time
    print(f"calculate_and_save_score_difference took {elapsed_time:.2f} seconds")

# Main function for continuous monitoring
def main():
    prev_player_one_score = None
    prev_player_two_score = None

    while True:
        # Read player scores
        player_one_score = read_score(PLAYER_ONE_SCORE_BBOX)
        player_two_score = read_score(PLAYER_TWO_SCORE_BBOX)

        # Check if the score has changed before saving
        if player_one_score != prev_player_one_score or player_two_score != prev_player_two_score:
            calculate_and_save_score_difference(player_one_score, player_two_score)
            prev_player_one_score = player_one_score
            prev_player_two_score = player_two_score

if __name__ == "__main__":
    main()
