from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os

from dipprocessing import process_image
from captioning import generate_caption
from nlpprocessing import process_caption
from texttospeech import generate_audio
from translationtest import translate_to_hindi, translate_to_kannada


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# IMAGE ANALYSIS
# =========================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    # -----------------------------------------------------
    # 1. RECEIVE IMAGE
    # -----------------------------------------------------

    if "image" not in request.files:
        return jsonify({
            "error": "No image was uploaded."
        }), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({
            "error": "No image was selected."
        }), 400

    print("\n" + "=" * 70)
    print("PROJECT AURA - IMAGE ANALYSIS STARTED")
    print("=" * 70)

    print("Image received:", image.filename)

    # Secure the uploaded filename
    safe_filename = secure_filename(image.filename)

    if safe_filename == "":
        return jsonify({
            "error": "Invalid image filename."
        }), 400

    image_path = os.path.join(
        UPLOAD_FOLDER,
        safe_filename
    )

    image.save(image_path)

    print("Image saved at:", image_path)


    # -----------------------------------------------------
    # 2. DIGITAL IMAGE PROCESSING
    # -----------------------------------------------------

    processed_image = process_image(
        image_path,
        OUTPUT_FOLDER
    )

    print("DIP processing completed.")


    # -----------------------------------------------------
    # 3. FLORENCE-2 AI DESCRIPTION
    # -----------------------------------------------------

    caption = generate_caption(image_path)

    print("\nAI Generated English Description:")
    print(caption)


    # -----------------------------------------------------
    # 4. ENGLISH NLP
    # -----------------------------------------------------

    english_nlp_result = process_caption(
        caption
    )

    print("\nEnglish NLP:")
    print(
        "Processed:",
        english_nlp_result["cleaned_caption"]
    )
    print(
        "Word Count:",
        english_nlp_result["word_count"]
    )


    # -----------------------------------------------------
    # 5. HINDI TRANSLATION
    # -----------------------------------------------------

    hindi_caption = translate_to_hindi(
        english_nlp_result["cleaned_caption"]
    )

    print("\nHindi Translation:")
    print(hindi_caption)


    # -----------------------------------------------------
    # 6. HINDI NLP
    # -----------------------------------------------------

    hindi_nlp_result = process_caption(
        hindi_caption
    )

    print("\nHindi NLP:")
    print(
        "Processed:",
        hindi_nlp_result["cleaned_caption"]
    )
    print(
        "Word Count:",
        hindi_nlp_result["word_count"]
    )


    # -----------------------------------------------------
    # 7. KANNADA TRANSLATION
    # -----------------------------------------------------

    kannada_caption = translate_to_kannada(
        english_nlp_result["cleaned_caption"]
    )

    print("\nKannada Translation:")
    print(kannada_caption)


    # -----------------------------------------------------
    # 8. KANNADA NLP
    # -----------------------------------------------------

    kannada_nlp_result = process_caption(
        kannada_caption
    )

    print("\nKannada NLP:")
    print(
        "Processed:",
        kannada_nlp_result["cleaned_caption"]
    )
    print(
        "Word Count:",
        kannada_nlp_result["word_count"]
    )


    # =====================================================
    # 9. ENGLISH AUDIO
    # =====================================================

    english_audio_filename = "description.wav"

    english_audio_path = os.path.join(
        OUTPUT_FOLDER,
        english_audio_filename
    )

    generate_audio(
        english_nlp_result["cleaned_caption"],
        english_audio_path,
        language="en"
    )

    print(
        "English TTS: Audio generated successfully."
    )


    # =====================================================
    # 10. HINDI AUDIO
    # =====================================================

    hindi_audio_filename = "description_hindi.wav"

    hindi_audio_path = os.path.join(
        OUTPUT_FOLDER,
        hindi_audio_filename
    )

    generate_audio(
        hindi_nlp_result["cleaned_caption"],
        hindi_audio_path,
        language="hi"
    )

    print(
        "Hindi TTS: Audio generated successfully."
    )


    # =====================================================
    # 11. KANNADA AUDIO
    # =====================================================

    kannada_audio_filename = "description_kannada.wav"

    kannada_audio_path = os.path.join(
        OUTPUT_FOLDER,
        kannada_audio_filename
    )

    generate_audio(
        kannada_nlp_result["cleaned_caption"],
        kannada_audio_path,
        language="kn"
    )

    print(
        "Kannada TTS: Audio generated successfully."
    )


    # =====================================================
    # 12. SEND ALL RESULTS TO FRONTEND
    # =====================================================

    response_data = {

        # -------------------------------------------------
        # BASIC INFORMATION
        # -------------------------------------------------

        "message": "Image processed successfully!",

        "filename": safe_filename,


        # -------------------------------------------------
        # DIP OUTPUTS
        # -------------------------------------------------

        "enhanced":
            "/outputs/" +
            os.path.basename(
                processed_image["enhanced"]
            ),

        "gray":
            "/outputs/" +
            os.path.basename(
                processed_image["gray"]
            ),

        "edges":
            "/outputs/" +
            os.path.basename(
                processed_image["edges"]
            ),


        # -------------------------------------------------
        # ENGLISH
        # -------------------------------------------------

        "caption":
            caption,

        "cleaned_caption":
            english_nlp_result["cleaned_caption"],

        "word_count":
            english_nlp_result["word_count"],

        "audio":
            "/outputs/" +
            english_audio_filename,


        # -------------------------------------------------
        # HINDI
        # -------------------------------------------------

        "hindi_caption":
            hindi_caption,

        "hindi_cleaned_caption":
            hindi_nlp_result["cleaned_caption"],

        "hindi_word_count":
            hindi_nlp_result["word_count"],

        "hindi_audio":
            "/outputs/" +
            hindi_audio_filename,


        # -------------------------------------------------
        # KANNADA
        # -------------------------------------------------

        "kannada_caption":
            kannada_caption,

        "kannada_cleaned_caption":
            kannada_nlp_result["cleaned_caption"],

        "kannada_word_count":
            kannada_nlp_result["word_count"],

        "kannada_audio":
            "/outputs/" +
            kannada_audio_filename
    }


    # =====================================================
    # COMPLETION MESSAGE
    # =====================================================

    print("\n" + "=" * 70)
    print("PROJECT AURA - IMAGE ANALYSIS COMPLETED")
    print("=" * 70 + "\n")


    return jsonify(response_data)


# =========================================================
# OUTPUT FILES
# =========================================================

@app.route("/outputs/<filename>")
def output_file(filename):

    return send_from_directory(
        OUTPUT_FOLDER,
        filename
    )


# =========================================================
# RUN FLASK APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )