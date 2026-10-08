import re
import unicodedata


def process_caption(caption):

    # --------------------------------------------------
    # 1. Normalize Unicode text
    # --------------------------------------------------

    cleaned_caption = unicodedata.normalize(
        "NFC",
        caption
    )


    # --------------------------------------------------
    # 2. Convert English characters to lowercase
    # --------------------------------------------------

    cleaned_caption = cleaned_caption.lower()


    # --------------------------------------------------
    # 3. Remove punctuation
    #    while preserving Hindi/English characters
    #    and Unicode combining marks
    # --------------------------------------------------

    cleaned_caption = "".join(
        character
        for character in cleaned_caption
        if not unicodedata.category(character).startswith("P")
    )


    # --------------------------------------------------
    # 4. Remove extra spaces
    # --------------------------------------------------

    cleaned_caption = re.sub(
        r"\s+",
        " ",
        cleaned_caption
    ).strip()


    # --------------------------------------------------
    # 5. Tokenize into words
    # --------------------------------------------------

    tokens = cleaned_caption.split()


    # --------------------------------------------------
    # 6. Count words
    # --------------------------------------------------

    word_count = len(tokens)


    # --------------------------------------------------
    # 7. Return NLP results
    # --------------------------------------------------

    return {
        "cleaned_caption": cleaned_caption,
        "word_count": word_count
    }