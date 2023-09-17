import cv2
import numpy as np
import matplotlib.pyplot as plt


def cartoonize_image(
    input_image_path,
    output_image_path,
    num_down=2,
    num_bilateral=7,
    brightness_factor=1.2,
):
    # Step 1: Load the image
    img = cv2.imread(input_image_path)

    # Step 2: Resize the image
    img_color = img
    for _ in range(num_down):
        img_color = cv2.pyrDown(img_color)

    # Step 3: Apply bilateral filter multiple times for a stronger cartoon effect
    for _ in range(num_bilateral):
        img_color = cv2.bilateralFilter(
            img_color, d=9, sigmaColor=75, sigmaSpace=75
        )  # Adjust these values

    # Step 4: Upscale the image back to its original size
    for _ in range(num_down):
        img_color = cv2.pyrUp(img_color)

    # Step 5: Convert the image to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 6: Reduce blurriness by applying a smaller median blur
    img_blur = cv2.medianBlur(img_gray, 3)  # Adjust the kernel size (e.g., 3)

    # Step 7: Create an edge mask using adaptive thresholding
    img_edge = cv2.adaptiveThreshold(
        img_blur,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        blockSize=9,  # Adjust this
        C=2,
    )  # Adjust this

    # Step 8: Combine the color and edge mask to get the cartoon effect
    img_cartoon = cv2.bitwise_and(img_color, img_color, mask=img_edge)

    # Step 9: Increase the brightness of the cartoonized image
    img_cartoon = cv2.convertScaleAbs(img_cartoon, alpha=brightness_factor, beta=0)

    # Step 10: Save the cartoonized image
    cv2.imwrite(output_image_path, img_cartoon)
    print("Cartoonized image saved as", output_image_path)

    # Display two grids: one for all steps and another for initial and final images
    original_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cartoonized_img = cv2.cvtColor(img_cartoon, cv2.COLOR_BGR2RGB)

    # Grid 1: All steps
    plt.figure(figsize=(20, 10))
    plt.subplot(2, 3, 1)
    plt.imshow(original_img)
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(2, 3, 2)
    plt.imshow(img_color)
    plt.title("Simplified Color")
    plt.axis("off")

    plt.subplot(2, 3, 3)
    plt.imshow(img_gray, cmap="gray")
    plt.title("Grayscale Image")
    plt.axis("off")

    plt.subplot(2, 3, 4)
    plt.imshow(img_edge, cmap="gray")
    plt.title("Edge Mask")
    plt.axis("off")

    plt.subplot(2, 3, 5)
    plt.imshow(cartoonized_img)
    plt.title("Cartoonized Image")
    plt.axis("off")

    # Grid 2: Initial and final
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(original_img)
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(cartoonized_img)
    plt.title("Cartoonized Image")
    plt.axis("off")

    # Save both grid images
    all_steps_output_path = (
        "all_steps_grid.jpg"  # Define the path for the all steps grid
    )
    initial_final_output_path = (
        "initial_final_grid.jpg"  # Define the path for the initial and final grid
    )

    plt.figure(1)
    plt.savefig(all_steps_output_path, bbox_inches="tight")

    plt.figure(2)
    plt.savefig(initial_final_output_path, bbox_inches="tight")

    plt.show()


if __name__ == "__main__":
    input_image_path = "input.jpg"  # Replace with the path to your input image
    output_image_path = "cartoonized_output.jpg"  # Replace with the desired output path
    cartoonize_image(
        input_image_path, output_image_path, brightness_factor=1.25
    )  # Adjust brightness_factor as needed
