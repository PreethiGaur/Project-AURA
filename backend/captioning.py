import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM


# -------------------------
# Florence-2 setup
# -------------------------

device = "cpu"
torch_dtype = torch.float32

print("Loading Florence-2 processor...")

processor = AutoProcessor.from_pretrained(
    "microsoft/Florence-2-base",
    trust_remote_code=True
)

print("Processor loaded successfully.")

print("Loading Florence-2 model...")

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Florence-2-base",
    torch_dtype=torch_dtype,
    trust_remote_code=True
).to(device)

model.eval()

print("Florence-2 model loaded successfully.")


# -------------------------
# Generate detailed description
# -------------------------

def generate_caption(image_path):

    image = Image.open(image_path).convert("RGB")

    prompt = "<MORE_DETAILED_CAPTION>"

    inputs = processor(
        text=prompt,
        images=image,
        return_tensors="pt"
    )

    inputs = {
        key: value.to(device) if hasattr(value, "to") else value
        for key, value in inputs.items()
    }

    with torch.no_grad():

        generated_ids = model.generate(
            **inputs,
            max_new_tokens=200,
            num_beams=3
        )

    generated_text = processor.batch_decode(
        generated_ids,
        skip_special_tokens=False
    )[0]

    parsed_answer = processor.post_process_generation(
        generated_text,
        task=prompt,
        image_size=image.size
    )

    # Florence returns the result in a dictionary
    caption = parsed_answer[prompt]

    return caption


# -------------------------
# Test
# -------------------------

if __name__ == "__main__":

    caption = generate_caption(
        "uploads/flower.jpg"
    )

    print("\nGenerated Detailed Description:")
    print(caption)