# Project AURA

## Multimodal Image-to-Text-to-Audio Describer for Visually Impaired People Using Digital Image Processing

Project AURA is an assistive application designed to help visually impaired users understand visual information from images through **image processing, AI-based image understanding, Natural Language Processing (NLP), translation, and text-to-speech (TTS)**.

The application accepts an image as input, processes the image using Digital Image Processing techniques, generates a detailed natural-language description using an AI vision model, processes the generated text using NLP, translates the description into Hindi and Kannada, and converts the descriptions into speech.

---

## Project Objective

The main objective of Project AURA is to provide an accessible way for visually impaired users to obtain meaningful information from images.

The system combines:

- Digital Image Processing
- Computer Vision
- Natural Language Processing
- Machine Learning / Deep Learning
- Machine Translation
- Text-to-Speech

into a single application.

---

## System Workflow

```text
                    IMAGE INPUT
                         |
                         v
                DIGITAL IMAGE PROCESSING
                         |
             +-----------+-----------+
             |                       |
             v                       v
       Enhanced Image        Grayscale / Edges
             |
             v
          FLORENCE-2
             |
             v
     English AI Description
             |
       +-----+------+----------------+
       |            |                |
       v            v                v
   English        Hindi           Kannada
      |              |                |
      v              v                v
  English NLP    Hindi NLP       Kannada NLP
      |              |                |
      +--------------+----------------+
                     |
                     v
                TEXT-TO-SPEECH
                     |
          +----------+----------+
          |          |          |
          v          v          v
       English     Hindi     Kannada
        Audio       Audio      Audio
