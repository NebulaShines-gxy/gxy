def calculate_wer(recognition_file, ground_truth_file):
    with open(recognition_file, 'r', encoding='utf-8') as f:
        recognitions = f.readlines()

    with open(ground_truth_file, 'r', encoding='utf-8') as f:
        ground_truths = f.readlines()

    total_errors = 0
    total_words = 0

    for recognition, ground_truth in zip(recognitions, ground_truths):
        recognition_words = recognition.strip().split()
        ground_truth_words = ground_truth.strip().split()

        # Calculate Levenshtein distance for each word pair
        errors = sum(1 for r, g in zip(recognition_words, ground_truth_words) if r != g)

        total_errors += errors
        total_words += len(ground_truth_words)

    # Calculate word error rate
    wer = total_errors / total_words
    return wer

# Example usage
recognition_file = "C:\\Users\\Nebula shines\\Desktop\\truth.txt"
ground_truth_file = "C:\\Users\\Nebula shines\\Desktop\\without_ultrasound.txt"
wer = calculate_wer(recognition_file, ground_truth_file)
print(f"Word Error Rate: {wer}")


