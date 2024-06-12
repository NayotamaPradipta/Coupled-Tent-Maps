from PIL import Image
def compare_images(image_path1, image_path2, tolerance=1):
    img1 = Image.open(image_path1).convert('L')
    img2 = Image.open(image_path2)

    if img1.size != img2.size:
        print("Images have different sizes.")
        return

    pixels1 = img1.load()
    pixels2 = img2.load()

    total_pixels = img1.width * img1.height
    print(f"Total pixels in each image: {total_pixels}")

    diff_count = 0
    for x in range(img1.width):
        for y in range(img1.height):
            if abs(pixels1[x, y] - pixels2[x, y]) > tolerance:
                diff_count += 1

    print(f"The images differ by {diff_count} significant pixels with a tolerance of {tolerance}.")

# Example usage
compare_images("../images/sample/PII.png", "../images/encrypted/PII_encrypted.png")
