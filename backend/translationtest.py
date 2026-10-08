import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from indicnlp.transliterate.unicode_transliterate import UnicodeIndicTransliterator


MODEL_NAME = "naklitechie/indictrans2-en-indic-dist-200M"


print("Loading IndicTrans2 tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

print("Tokenizer loaded successfully!")


print("Loading IndicTrans2 model...")

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

model.eval()

print("IndicTrans2 model loaded successfully!")


# --------------------------------------------------
# ENGLISH → HINDI
# --------------------------------------------------

def translate_to_hindi(text):

    tagged_text = f"eng_Latn hin_Deva {text}"

    inputs = tokenizer(
        [tagged_text],
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=256
    )

    with torch.no_grad():

        generated_tokens = model.generate(
            **inputs,
            max_length=256,
            num_beams=5,
            num_return_sequences=1
        )

    raw_translation = tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )[0]

    final_translation = raw_translation.replace(
        "▁", " "
    ).strip()

    return final_translation


# --------------------------------------------------
# ENGLISH → KANNADA
# --------------------------------------------------

def translate_to_kannada(text):

    tagged_text = f"eng_Latn kan_Knda {text}"

    inputs = tokenizer(
        [tagged_text],
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=256
    )

    with torch.no_grad():

        generated_tokens = model.generate(
            **inputs,
            max_length=256,
            num_beams=5,
            num_return_sequences=1
        )

    raw_translation = tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )[0]

    raw_translation = raw_translation.replace(
        "▁", " "
    ).strip()

    # IndicTrans2 internally represents Kannada
    # using Devanagari script.
    # Convert it to native Kannada script.
    final_translation = UnicodeIndicTransliterator.transliterate(
        raw_translation,
        "hi",
        "kn"
    )

    return final_translation


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    test_text = (
        "A young woman is sitting on a blue chair "
        "in an office and holding a book."
    )

    print("\n" + "=" * 60)
    print("ENGLISH:")
    print(test_text)

    print("\n" + "=" * 60)
    print("HINDI:")

    hindi_result = translate_to_hindi(test_text)
    print(hindi_result)

    print("\n" + "=" * 60)
    print("KANNADA:")

    kannada_result = translate_to_kannada(test_text)
    print(kannada_result)

    print("\n" + "=" * 60)