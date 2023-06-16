from PIL import Image
import matplotlib.pyplot as plt


def open_image(file_path):
    return Image.open(file_path)


def save_image(image, file_path):
    image.save(file_path)


def resize_image(image, scale_factor=2):
    new_size = (image.size[0] * scale_factor, image.size[1] * scale_factor)
    return image.resize(new_size)


def plot_image(image):
    plt.imshow(image)