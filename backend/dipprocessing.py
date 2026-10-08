import cv2
import os


def process_image(image_path, output_folder):

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not load the image.")

    print("DIP: Image loaded successfully")
    print("DIP: Image shape:", image.shape)

    # Create output folder if it does not exist
    os.makedirs(output_folder, exist_ok=True)

    # Get image name without extension
    image_name = os.path.splitext(os.path.basename(image_path))[0]

    # -------------------------
    # 1. Image Enhancement
    # -------------------------

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced_l = clahe.apply(l_channel)

    enhanced_lab = cv2.merge(
        (enhanced_l, a_channel, b_channel)
    )

    enhanced = cv2.cvtColor(
        enhanced_lab,
        cv2.COLOR_LAB2BGR
    )

    # -------------------------
    # 2. Grayscale
    # -------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # -------------------------
    # 3. Edge Detection
    # -------------------------

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    edges = cv2.Canny(
        blur,
        100,
        200
    )

    # -------------------------
    # Save results
    # -------------------------

    enhanced_path = os.path.join(
        output_folder,
        image_name + "_enhanced.jpg"
    )

    gray_path = os.path.join(
        output_folder,
        image_name + "_gray.jpg"
    )

    edges_path = os.path.join(
        output_folder,
        image_name + "_edges.jpg"
    )

    cv2.imwrite(enhanced_path, enhanced)
    cv2.imwrite(gray_path, gray)
    cv2.imwrite(edges_path, edges)

    print("DIP: Enhanced image saved")
    print("DIP: Grayscale image saved")
    print("DIP: Edge image saved")

    return {
        "enhanced": enhanced_path,
        "gray": gray_path,
        "edges": edges_path
    }