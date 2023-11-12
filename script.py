import os, sys
from PIL import Image


def open_directory(path):
    if sys.platform.startswith('darwin'):  # macOS
        os.system('open "{}"'.format(path))
    elif sys.platform.startswith('win'):  # Windows
        os.system('start "" "{}"'.format(path))
    elif sys.platform.startswith('linux'):  # Linux
        os.system('xdg-open "{}"'.format(path))
    else:
        print("Unsupported operating system.")


class WatermarkSetter:
    def __init__(self):
        super().__init__()
        self.__watermark = ''
        self.__opacity = 0.5
        self.__width = 150
        self.__height = 150
        self.__scale = 1
        self.__position = 'bottom right'
        self.__margin = 0
        self.__watermark_type = 'normal'

    def get_watermark(self):
        return self.__watermark

    def set_watermark(self, filename):
        # Load the watermark image
        self.__watermark = Image.open(filename)

    def apply_watermark_from_file(self, filename, dst_dirname):
        # Open the image
        image = Image.open(filename)

        # Define the position for the watermark (bottom right corner)
        image_width, image_height = image.size
        self.set_position(self.__position)
        position = self.__get_position(image_width, image_height)

        # TODO discriminate scale and width and height
        # self.resize_watermark(self.__width, self.__height)

        # Create a copy of the image to avoid modifying the original
        image_with_watermark = image.copy()

        cur_watermark = self.set_watermark_opacity(self.__opacity)

        # Paste the watermark onto the image
        if self.__watermark_type == 'tiled':
            # tiled
            for x in range(0, image_width, cur_watermark.width):
                for y in range(0, image_height, cur_watermark.height):
                    image_with_watermark.paste(cur_watermark, (x, y), cur_watermark)
        else:
            # normal
            image_with_watermark.paste(cur_watermark, position, cur_watermark)

        filename = os.path.join(dst_dirname, os.path.basename(filename))

        # Save the final image with the watermark
        image_with_watermark.save(filename)

    def apply_watermark_from_directory(self, src_dirname, dst_dirname):
        os.makedirs(dst_dirname, exist_ok=True)

        filenames = [os.path.join(src_dirname, filename) for filename in os.listdir(src_dirname)]

        for filename in filenames:
            self.apply_watermark_from_file(filename, dst_dirname)

    def __is_watermark_set(self):
        return self.__watermark is not None

    def __check_watermark_set(self):
        if not self.__is_watermark_set():
            raise ValueError("Watermark is not set. Use set_watermark() first.")

    def resize_watermark(self, width, height):
        self.__check_watermark_set()
        # Resize the watermark with the specified width and height
        self.__width = width
        self.__height = height
        self.__watermark = self.__watermark.resize((self.__width, self.__height))

    def set_margin(self, margin):
        self.__check_watermark_set()
        self.__margin = margin

    def set_type(self, watermark_type):
        """
        watermark_type should be one of this:
        normal, tiled
        """
        self.__check_watermark_set()
        if watermark_type not in ["normal", "tiled"]:
            raise ValueError("Invalid watermark_type. It should be 'normal' or 'tiled'.")
        self.__watermark_type = watermark_type

    def __check_position(self, position):
        if position not in ['bottom right', 'bottom left', 'top left', 'top right']:
            raise ValueError(
                "Invalid position. It should be 'top left', 'top right', 'bottom left', or 'bottom right'.")

    def set_position(self, position):
        """
        position should be one of this:
        top left, top right, bottom left, bottom right
        """
        self.__check_watermark_set()
        self.__check_position(position)
        self.__position = position

    def __get_position(self, image_width, image_height):
        self.__check_watermark_set()
        watermark_width, watermark_height = self.__watermark.size
        position = 0
        if self.__position == 'bottom right':
            position = (image_width - watermark_width - self.__margin, image_height - watermark_height - self.__margin)
        elif self.__position == 'bottom left':
            position = (self.__margin, image_height - watermark_height - self.__margin)
        elif self.__position == 'top left':
            position = (self.__margin, self.__margin)
        elif self.__position == 'top right':
            position = (image_width - watermark_width - self.__margin, self.__margin)
        return position

    def set_watermark_opacity(self, opacity):
        self.__check_watermark_set()
        # Make the watermark semi-transparent
        cur_watermark = self.__watermark.convert("RGBA")
        for x in range(cur_watermark.width):
            for y in range(cur_watermark.height):
                r, g, b, alpha = cur_watermark.getpixel((x, y))
                cur_watermark.putpixel((x, y), (r, g, b, int(alpha * opacity)))
        return cur_watermark

# import os
#
# src_dirname = 'example'
# dst_dirname = 'dst'
#
# setter = WatermarkSetter()
# setter.set_watermark('watermark.png')
# setter.apply_watermark_from_directory(src_dirname, 'dst2')