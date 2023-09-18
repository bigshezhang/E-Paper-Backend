from PIL import Image, ImageFilter, ImageEnhance, ImageDraw

from unit import Unit

class ImageProcess:
    class ImageDriver:
        def dither_img(self, image: Image.Image, selfwidth=800, selfheight=480):
        # Crop the image to the specified width and height

            # image.thumbnail((selfwidth, selfheight))

            image = self.resize_and_crop(image, 480, 800)
            image = image.convert("RGB")
            image.save('./temp.jpg', format='JPEG', quality=100)

            pal_image = Image.new("P", (1, 1))

            pal_image.putpalette((0, 0, 0,
            255, 255, 255,
            67, 138, 28,
            50, 43, 88,
            191, 0, 0,
            255, 243, 56,
            232, 126, 0,
            194 ,164 , 244))

            # pal_image.putpalette( (20, 28, 45,  152, 166, 147, 26, 94, 54, 32, 53, 90,  112, 43, 50,  176, 167, 29, 107, 61, 54) + (0,0,0)*249)
            # pal_image.putpalette( (30, 31, 26,  185, 199, 147, 51, 111, 26, 50, 62, 66,  130, 50, 25,  188, 179, 14, 124, 73, 28) + (0,0,0)*249)
            
            # pal_image.putpalette((37, 26, 50,  186, 173, 166, 48, 81, 63,  50, 43, 88, 129, 32, 57,  178, 146, 49, 141, 54, 65, 170, 132, 114) + (0,0,0)*248)
            
            # pal_image.putpalette( (16,14,27,  255, 255, 255,  47, 80, 61,   51, 44, 89, 128, 32, 57, 178, 146, 52, 138, 51, 62, 170, 132, 114) + (0,0,0)*248)
                
            
            #last
            # pal_image.putpalette( (34, 25, 48,  184, 170, 165,  49, 82, 63,   51, 44, 89,  128, 32, 55,  178, 146, 52,  141, 54,65, 170, 132, 114) + (0,0,0)*248)
            # pal_image.putpalette((45, 57, 77, 185, 200, 182, 55, 115, 87, 60, 86, 125, 54, 78, 120, 168, 165, 66,  97, 46, 43, 131, 123, 89) + (0,0,0)*248)
            
            
            pal_image.putpalette((51, 38, 45, 177, 174, 162, 70, 98, 62, 64, 57, 82, 118, 46, 48, 176, 147, 49, 135, 62, 59, 164, 131, 107) + (0,0,0)*248)

            image = ImageProcess.ImageRender.add_blur_container(ImageProcess.ImageRender, image)
            # Convert the source image to the 7 colors, dithering if needed
            image_7color = image.convert("RGB").quantize(palette=pal_image)
            image_7color = self.rotate_to_portrait(image_7color)
            # image_7color.show()

            return image_7color

        def resize_and_crop(image: Image.Image, width, height):
            # Calculate the aspect ratio of the target size
            aspect_ratio = width / height

            # Calculate the aspect ratio of the source image
            img_width, img_height = image.size
            img_aspect_ratio = img_width / img_height

            if img_aspect_ratio > aspect_ratio:
                # Crop the width of the image to match the target aspect ratio
                new_width = int(img_height * aspect_ratio)
                left = (img_width - new_width) / 2
                top = 0
                right = (img_width + new_width) / 2
                bottom = img_height
            else:
                # Crop the height of the image to match the target aspect ratio
                new_height = int(img_width / aspect_ratio)
                left = 0
                top = (img_height - new_height) / 2
                right = img_width
                bottom = (img_height + new_height) / 2

            # Crop and resize the image
            cropped_resized_image = image.crop((left, top, right, bottom)).resize((width, height))

            return cropped_resized_image

        def rotate_to_portrait(image: Image.Image):
            # Check if the image is in portrait mode (height > width)

            if image.size[1] < image.size[0]:   # if height > width
                return image  # No need to rotate

            # Rotate the image 90 degrees clockwise
            rotated_image = image.transpose(Image.Transpose.ROTATE_90)
            # rotated_image.show()
            return rotated_image

        def buffImg(self, image):
            image_temp = image
            buf_7color = bytearray(image_temp.tobytes('raw'))
            # PIL does not support 4 bit color, so pack the 4 bits of color
            # into a single byte to transfer to the panel
            buf = [0x00] * int(image_temp.width * image_temp.height / 2)
            idx = 0
            for i in range(0, len(buf_7color), 2):
                buf[idx] = (buf_7color[i] << 4) + buf_7color[i+1]
                idx += 1
            
            # Convert each byte in buf to a hexadecimal string
            hex_buf = bytes(buf)
            
            return hex_buf

        def image_driver(self, image):
            dithered_image = self.dither_img(self, image)
            return(self.buffImg(self, dithered_image))
    
    class ImageRender:
        def get_dominant_color(self, pil_img: Image.Image):        
            img = pil_img.copy()
            img = img.convert("RGB")
            img = img.resize((5, 5), resample=0)
            dominant_color = img.getpixel((2, 2))
            return dominant_color
        
        def add_blur_container(self, image: Image.Image):
            width, height = 480, 800

            blur_image = image.copy()
            blur_image = blur_image.filter(ImageFilter.GaussianBlur(radius=8))

            mask = Image.new('L', image.size, 255)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.rounded_rectangle(xy=[[16, height - 16 - 200], [width - 16, height - 16]],radius=16,fill=0)
            # mask.show()

            draw_blur_outline = ImageDraw.Draw(blur_image)
            draw_blur_outline.rounded_rectangle(xy=[[16, height - 16 - 200], [width - 16, height - 16]],radius=16,outline= "white", width=4)

            output = Image.composite(image ,blur_image, mask)
            # output.show()
            return output



