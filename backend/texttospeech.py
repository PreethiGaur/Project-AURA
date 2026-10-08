import os

import pyttsx3
import torch
from transformers import VitsModel, AutoTokenizer
from scipy.io.wavfile import write


# ============================================================
# KANNADA MMS TTS MODEL
# ============================================================

KANNADA_MODEL_NAME = "facebook/mms-tts-kan"

print("Loading Kannada MMS TTS model...")

kannada_tokenizer = AutoTokenizer.from_pretrained(
    KANNADA_MODEL_NAME
)

kannada_model = VitsModel.from_pretrained(
    KANNADA_MODEL_NAME
)

kannada_model.eval()

print("Kannada MMS TTS model loaded successfully.")


# ============================================================
# WINDOWS VOICE SELECTION
# Used for English and Hindi
# ============================================================

def find_windows_voice(voices, language):
    if language == "en":
        preferred_names = ["David", "Zira"]
        language_keywords = ["en-us", "en_us", "english"]

    elif language == "hi":
        preferred_names = ["Hemant", "Kalpana"]
        language_keywords = ["hi-in", "hi_in", "hindi"]

    else:
        raise ValueError(
            f"Windows voice selection does not support language: {language}"
        )

    # First try preferred voice names
    for voice in voices:
        voice_name = voice.name.lower()

        for preferred_name in preferred_names:
            if preferred_name.lower() in voice_name:
                return voice

    # Then try language identifiers
    for voice in voices:
        voice_name = voice.name.lower()
        voice_id = voice.id.lower()

        for keyword in language_keywords:
            if keyword in voice_name or keyword in voice_id:
                return voice

    return None


# ============================================================
# ENGLISH / HINDI TTS
# ============================================================

def generate_windows_audio(text, output_path, language):
    engine = pyttsx3.init()

    voices = engine.getProperty("voices")

    selected_voice = find_windows_voice(
        voices,
        language
    )

    if selected_voice is None:
        engine.stop()

        raise RuntimeError(
            f"No suitable Windows TTS voice was found for language: {language}"
        )

    print(
        f"TTS: Using Windows voice "
        f"'{selected_voice.name}' for language '{language}'"
    )

    engine.setProperty(
        "voice",
        selected_voice.id
    )

    engine.setProperty(
        "rate",
        150
    )

    engine.save_to_file(
        text,
        output_path
    )

    engine.runAndWait()

    engine.stop()

    print(
        f"TTS: Audio saved to {output_path}"
    )

    return output_path


# ============================================================
# KANNADA MMS TTS
# ============================================================

def generate_kannada_audio(text, output_path):
    print("TTS: Generating Kannada speech using MMS...")

    inputs = kannada_tokenizer(
        text,
        return_tensors="pt"
    )

    with torch.no_grad():
        output = kannada_model(
            **inputs
        ).waveform

    audio = (
        output.squeeze()
        .cpu()
        .numpy()
    )

    write(
        output_path,
        kannada_model.config.sampling_rate,
        audio
    )

    print(
        f"TTS: Kannada audio saved to {output_path}"
    )

    return output_path


# ============================================================
# MAIN TTS FUNCTION
# ============================================================

def generate_audio(text, output_path, language="en"):

    if language == "en":
        return generate_windows_audio(
            text,
            output_path,
            "en"
        )

    elif language == "hi":
        return generate_windows_audio(
            text,
            output_path,
            "hi"
        )

    elif language == "kn":
        return generate_kannada_audio(
            text,
            output_path
        )

    else:
        raise ValueError(
            f"Unsupported language: {language}"
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\nTesting Kannada TTS...\n")

    test_text = "ಇದು ಕನ್ನಡ ಪರೀಕ್ಷೆ."

    test_output = "kannada_tts_from_texttospeech.wav"

    generate_audio(
        test_text,
        test_output,
        language="kn"
    )

    print("\nKannada TTS test completed successfully.")