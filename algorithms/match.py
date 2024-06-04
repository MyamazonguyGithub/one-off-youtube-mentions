from thefuzz import fuzz, process
import re

def preprocess_text(text: str):
    """
    Preprocess the text by removing special characters, apostrophes, and extra spaces, and normalizing case.

    Args:
        text (str): The input text to be preprocessed.
    """
    text = re.sub(r"'s\b|’s\b", "", text)  # Remove 's
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
    return text.lower()

def dynamic_threshold(variation: str):
    """
    Calculate a dynamic threshold based on the length of the variation.

    Args:
        variation (str): The word variation for which the threshold is calculated.

    Returns:
        int: The dynamic threshold based on the length of the variation.
    """
    length = len(variation)
    if length <= 5:
        return 80  # Lower threshold for very short names
    elif length <= 10:
        return 85  # Medium threshold for medium-length names
    else:
        return 90  # Higher threshold for longer names

def count_mentions(transcript: str, competitors=None):
    """
    Count the mentions of each competitor in the transcript.

    Args:
        transcript (str): The transcript text containing mentions of competitors.
        competitors (dict): A dictionary containing competitors and their variations.

    Returns:
        dict: A dictionary with the count of mentions for each competitor in the transcript.
    """
    if competitors is None:
        competitors = {
            "Seller Interactive": ["cellar interactive", "seller inter active", "seller interactive"],
            "Canopy": ["canopy", "canapoy"],
            "Tinuiti": ["tenuity", "tinutty", "tinuiti", "tinuity", "tinutai", "tinuity", "tinuitti", "tinuitie"],
            "Teika": ["teka", "teaka", "teika", "taika", "teikah", "teeka", "teikaa"]
        }

    results = {}
    sentences = transcript.split('\n')  # Split transcript into sentences
    preprocessed_sentences = [preprocess_text(sentence) for sentence in sentences if sentence.strip()]

    for competitor, variations in competitors.items():
        count = 0
        for variation in variations:
            preprocessed_variation = preprocess_text(variation)
            threshold = dynamic_threshold(preprocessed_variation)

            matches = process.extract(preprocessed_variation, preprocessed_sentences, scorer=fuzz.token_set_ratio)
            for match in matches:
                if match[1] >= threshold:
                    count += 1
                    preprocessed_sentences.remove(match[0])  # Remove matched sentence
        results[competitor] = count

    return results

if __name__ == "__main__":
    # Sample transcript text
    sample_transcript = """
    During our recent call with a prospective client, they mentioned that they had previously worked with cellar interactive. They appreciated the detailed reports provided but felt the customer service could be improved.

    Later in the conversation, the client brought up another competitor, canopy, and praised their innovative marketing strategies. However, they were not satisfied with the pricing plans offered by canapoy.

    Towards the end of the call, another competitor was mentioned, tenuity. The client highlighted that they found tinutty’s approach to be very aggressive but effective in driving sales. teaka

    Finally, the client discussed their experience with teka, noting that teaka had a very user-friendly platform but faced some issues with data synchronization. 

    seller interactive
    seller interactive
    tinuiti
    tenuity
    tinutty
    """

    # Count mentions in the sample transcript
    mentions = count_mentions(sample_transcript)

    # Print results
    for competitor, count in mentions.items():
        print(f"{competitor}: {count} mentions")
