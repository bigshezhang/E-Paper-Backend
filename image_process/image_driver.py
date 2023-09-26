from PIL import Image
from common.database import Database
from common.unit import Unit
from image_process.description_render import DescriptionRender

class ImageDriver:     
    def dither_img(self, image: Image.Image, selfwidth=800, selfheight=480):
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
        194 ,164 , 244)+ (0,0,0)*248)

        # pal_image.putpalette( (20, 28, 45,  152, 166, 147, 26, 94, 54, 32, 53, 90,  112, 43, 50,  176, 167, 29, 107, 61, 54) + (0,0,0)*249)
        # pal_image.putpalette( (30, 31, 26,  185, 199, 147, 51, 111, 26, 50, 62, 66,  130, 50, 25,  188, 179, 14, 124, 73, 28) + (0,0,0)*249)
        
        # pal_image.putpalette((37, 26, 50,  186, 173, 166, 48, 81, 63,  50, 43, 88, 129, 32, 57,  178, 146, 49, 141, 54, 65, 170, 132, 114) + (0,0,0)*248)
        
        # pal_image.putpalette( (16,14,27,  255, 255, 255,  47, 80, 61,   51, 44, 89, 128, 32, 57, 178, 146, 52, 138, 51, 62, 170, 132, 114) + (0,0,0)*248)
            
        #last
        # pal_image.putpalette( (34, 25, 48,  184, 170, 165,  49, 82, 63,   51, 44, 89,  128, 32, 55,  178, 146, 52,  141, 54,65, 170, 132, 114) + (0,0,0)*248)
        # pal_image.putpalette((45, 57, 77, 185, 200, 182, 55, 115, 87, 60, 86, 125, 54, 78, 120, 168, 165, 66,  97, 46, 43, 131, 123, 89) + (0,0,0)*248)

        # pal_image.putpalette((51, 38, 45, 177, 174, 162, 70, 98, 62, 64, 57, 82, 118, 46, 48, 176, 147, 49, 135, 62, 59, 164, 131, 107) + (0,0,0)*248)
        image_7color = image.convert("RGB").quantize(palette=pal_image)
        image_7color = self.rotate_to_portrait(image_7color)
        return image_7color

    def resize_and_crop(image: Image.Image, width, height):
        aspect_ratio = width / height
        img_width, img_height = image.size
        img_aspect_ratio = img_width / img_height
        
        if img_aspect_ratio > aspect_ratio:
            new_width = int(img_height * aspect_ratio)
            left = (img_width - new_width) / 2
            top = 0
            right = (img_width + new_width) / 2
            bottom = img_height
        else:
            new_height = int(img_width / aspect_ratio)
            left = 0
            top = (img_height - new_height) / 2
            right = img_width
            bottom = (img_height + new_height) / 2

        cropped_resized_image = image.crop((left, top, right, bottom)).resize((width, height))

        return cropped_resized_image

    def rotate_to_portrait(image: Image.Image):

        if image.size[1] < image.size[0]:   # if height > width
            return image  # No need to rotate
        rotated_image = image.transpose(Image.Transpose.ROTATE_270)
        return rotated_image

    def buffImg(self, image):
        image_temp = image
        buf_7color = bytearray(image_temp.tobytes('raw'))
        buf = [0x00] * int(image_temp.width * image_temp.height / 2)
        idx = 0
        for i in range(0, len(buf_7color), 2):
            buf[idx] = (buf_7color[i] << 4) + buf_7color[i+1]
            idx += 1
        
        hex_buf = bytes(buf)
        return hex_buf

    def image_driver(self, image, filename: str):
        image = self.resize_and_crop(image, 480, 800)
        image = DescriptionRender.add_blur_container(DescriptionRender, image)
        image = DescriptionRender.add_description_text(DescriptionRender, image, Database.get_photo_description(Database, filename))
        dithered_image = self.dither_img(self, image)
        return(self.buffImg(self, dithered_image))
    
    def publish_image(self, image, filename):
        bytes_file_name = './uploads/byte_stream.txt'
        with open(bytes_file_name, 'wb') as file:
            file.write(self.image_driver(self, image, filename))
        file.close()

        pic_file_name = './uploads/currently_showing.jpg'
        img = image.convert("RGB")
        img = img.transpose(Image.Transpose.ROTATE_90)
        img.save(pic_file_name)
        Unit.mqttServer.publish_file()