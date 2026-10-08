// =========================================================
// PROJECT AURA - FRONTEND JAVASCRIPT
// =========================================================


// =========================================================
// 1. GET HTML ELEMENTS
// =========================================================

const imageInput = document.getElementById("imageInput");

const previewText = document.getElementById("previewText");
const imagePreview = document.getElementById("imagePreview");

const analyzeButton = document.getElementById("analyzeButton");


// DIP images
const originalImage = document.getElementById("originalImage");
const enhancedImage = document.getElementById("enhancedImage");
const grayImage = document.getElementById("grayImage");
const edgesImage = document.getElementById("edgesImage");


// AI descriptions
const caption = document.getElementById("caption");
const hindiCaption = document.getElementById("hindiCaption");
const kannadaCaption = document.getElementById("kannadaCaption");


// NLP
const cleanedCaption = document.getElementById("cleanedCaption");
const wordCount = document.getElementById("wordCount");


// Audio
const audioButton = document.getElementById("audioButton");
const audioPlayer = document.getElementById("audioPlayer");


// =========================================================
// 2. STORE RESULTS
// =========================================================

// English
let englishAudioPath = "";
let englishNlpData = null;


// Hindi
let hindiAudioPath = "";
let hindiNlpData = null;


// Kannada
let kannadaAudioPath = "";
let kannadaNlpData = null;


// =========================================================
// 3. IMAGE SELECTION
// =========================================================

imageInput.addEventListener("change", function () {

    const file = imageInput.files[0];

    if (!file) {
        return;
    }


    // Show selected filename
    previewText.textContent =
        "Selected image: " + file.name;


    // Create preview
    const imageURL = URL.createObjectURL(file);

    imagePreview.src = imageURL;

    imagePreview.style.display = "block";


    // Show original image immediately
    originalImage.src = imageURL;

    originalImage.style.display = "block";

});


// =========================================================
// 4. NLP DISPLAY FUNCTION
// =========================================================

function updateNlpDisplay(language) {

    // -----------------------------------------------------
    // English
    // -----------------------------------------------------

    if (language === "english") {

        if (!englishNlpData) {

            cleanedCaption.textContent = "-";
            wordCount.textContent = "-";

            return;
        }


        cleanedCaption.textContent =
            englishNlpData.cleaned_caption;

        wordCount.textContent =
            englishNlpData.word_count;

    }


    // -----------------------------------------------------
    // Hindi
    // -----------------------------------------------------

    else if (language === "hindi") {

        if (!hindiNlpData) {

            cleanedCaption.textContent = "-";
            wordCount.textContent = "-";

            return;
        }


        cleanedCaption.textContent =
            hindiNlpData.cleaned_caption;

        wordCount.textContent =
            hindiNlpData.word_count;

    }


    // -----------------------------------------------------
    // Kannada
    // -----------------------------------------------------

    else if (language === "kannada") {

        if (!kannadaNlpData) {

            cleanedCaption.textContent = "-";
            wordCount.textContent = "-";

            return;
        }


        cleanedCaption.textContent =
            kannadaNlpData.cleaned_caption;

        wordCount.textContent =
            kannadaNlpData.word_count;

    }

}


// =========================================================
// 5. NLP LANGUAGE SELECTION
// =========================================================

const nlpLanguageOptions =
    document.querySelectorAll(
        'input[name="nlpLanguage"]'
    );


nlpLanguageOptions.forEach(function (radio) {

    radio.addEventListener("change", function () {

        updateNlpDisplay(this.value);

    });

});


// =========================================================
// 6. ANALYZE IMAGE
// =========================================================

analyzeButton.addEventListener("click", async function () {

    const file = imageInput.files[0];


    // -----------------------------------------------------
    // Check whether image was selected
    // -----------------------------------------------------

    if (!file) {

        alert("Please choose an image first.");

        return;
    }


    // -----------------------------------------------------
    // Disable button while processing
    // -----------------------------------------------------

    analyzeButton.disabled = true;

    analyzeButton.textContent =
        "Analyzing Image...";


    try {

        // -------------------------------------------------
        // Create form data
        // -------------------------------------------------

        const formData = new FormData();

        formData.append(
            "image",
            file
        );


        // -------------------------------------------------
        // Send image to Flask
        // -------------------------------------------------

        const response = await fetch(
            "/analyze",
            {
                method: "POST",
                body: formData
            }
        );


        // -------------------------------------------------
        // Convert response to JSON
        // -------------------------------------------------

        const data = await response.json();


        // -------------------------------------------------
        // Check backend error
        // -------------------------------------------------

        if (!response.ok) {

            throw new Error(
                data.error ||
                "Image analysis failed."
            );
        }


        // =================================================
        // 7. DISPLAY DIP RESULTS
        // =================================================

        originalImage.src =
            imagePreview.src;

        originalImage.style.display =
            "block";


        enhancedImage.src =
            data.enhanced;

        enhancedImage.style.display =
            "block";


        grayImage.src =
            data.gray;

        grayImage.style.display =
            "block";


        edgesImage.src =
            data.edges;

        edgesImage.style.display =
            "block";


        // =================================================
        // 8. DISPLAY AI DESCRIPTIONS
        // =================================================

        caption.textContent =
            data.caption;


        hindiCaption.textContent =
            data.hindi_caption;


        kannadaCaption.textContent =
            data.kannada_caption;


        // =================================================
        // 9. STORE NLP RESULTS
        // =================================================

        englishNlpData = {

            cleaned_caption:
                data.cleaned_caption,

            word_count:
                data.word_count

        };


        hindiNlpData = {

            cleaned_caption:
                data.hindi_cleaned_caption,

            word_count:
                data.hindi_word_count

        };


        kannadaNlpData = {

            cleaned_caption:
                data.kannada_cleaned_caption,

            word_count:
                data.kannada_word_count

        };


        // =================================================
        // 10. STORE AUDIO PATHS
        // =================================================

        englishAudioPath =
            data.audio;


        hindiAudioPath =
            data.hindi_audio;


        kannadaAudioPath =
            data.kannada_audio;


        // =================================================
        // 11. DEFAULT NLP LANGUAGE
        // =================================================

        const selectedNlpLanguage =
            document.querySelector(
                'input[name="nlpLanguage"]:checked'
            );


        if (selectedNlpLanguage) {

            updateNlpDisplay(
                selectedNlpLanguage.value
            );

        }


        // =================================================
        // 12. DEFAULT AUDIO
        // =================================================

        audioPlayer.src =
            englishAudioPath;

        audioPlayer.style.display =
            "block";


        console.log(
            "Project AURA analysis completed successfully."
        );


    } catch (error) {

        console.error(
            "Analysis error:",
            error
        );


        alert(
            "Something went wrong while analyzing the image.\n\n" +
            error.message
        );

    }


    // -----------------------------------------------------
    // Enable button again
    // -----------------------------------------------------

    analyzeButton.disabled = false;

    analyzeButton.textContent =
        "Analyze Image";

});


// =========================================================
// 13. AUDIO LANGUAGE SELECTION
// =========================================================

const audioLanguageOptions =
    document.querySelectorAll(
        'input[name="language"]'
    );


audioLanguageOptions.forEach(function (radio) {

    radio.addEventListener("change", function () {

        const selectedLanguage =
            this.value;


        // -------------------------------------------------
        // English
        // -------------------------------------------------

        if (selectedLanguage === "english") {

            if (!englishAudioPath) {

                alert(
                    "Please analyze an image first."
                );

                return;
            }


            audioPlayer.src =
                englishAudioPath;

        }


        // -------------------------------------------------
        // Hindi
        // -------------------------------------------------

        else if (selectedLanguage === "hindi") {

            if (!hindiAudioPath) {

                alert(
                    "Please analyze an image first."
                );

                return;
            }


            audioPlayer.src =
                hindiAudioPath;

        }


        // -------------------------------------------------
        // Kannada
        // -------------------------------------------------

        else if (selectedLanguage === "kannada") {

            if (!kannadaAudioPath) {

                alert(
                    "Please analyze an image first."
                );

                return;
            }


            audioPlayer.src =
                kannadaAudioPath;

        }


        // Make sure audio player is visible
        audioPlayer.style.display =
            "block";


        // Load newly selected audio
        audioPlayer.load();

    });

});


// =========================================================
// 14. PLAY SELECTED AUDIO
// =========================================================

audioButton.addEventListener("click", function () {

    const selectedLanguage =
        document.querySelector(
            'input[name="language"]:checked'
        );


    if (!selectedLanguage) {

        alert(
            "Please select a language."
        );

        return;
    }


    // -----------------------------------------------------
    // English
    // -----------------------------------------------------

    if (selectedLanguage.value === "english") {

        if (!englishAudioPath) {

            alert(
                "Please analyze an image first."
            );

            return;
        }


        audioPlayer.src =
            englishAudioPath;

    }


    // -----------------------------------------------------
    // Hindi
    // -----------------------------------------------------

    else if (selectedLanguage.value === "hindi") {

        if (!hindiAudioPath) {

            alert(
                "Please analyze an image first."
            );

            return;
        }


        audioPlayer.src =
            hindiAudioPath;

    }


    // -----------------------------------------------------
    // Kannada
    // -----------------------------------------------------

    else if (selectedLanguage.value === "kannada") {

        if (!kannadaAudioPath) {

            alert(
                "Please analyze an image first."
            );

            return;
        }


        audioPlayer.src =
            kannadaAudioPath;

    }


    // -----------------------------------------------------
    // Play
    // -----------------------------------------------------

    audioPlayer.style.display =
        "block";

    audioPlayer.load();

    audioPlayer.play().catch(function (error) {

        console.error(
            "Audio playback error:",
            error
        );

    });

});