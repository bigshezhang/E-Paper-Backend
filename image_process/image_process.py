from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont

from common.unit import Unit

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

    def image_driver(self, image):
        image = self.resize_and_crop(image, 480, 800)

        image = ImageRender.add_blur_container(ImageRender, image)
        image = ImageRender.add_description_text(ImageRender, image)

        dithered_image = self.dither_img(self, image)

        file_name = './uploads/byte_stream.txt'
        with open(file_name, 'wb') as file:
            file.write(self.buffImg(self, dithered_image))
        file.close()

        file_name = './uploads/currently_showing.jpg'
        img = dithered_image.convert("RGB")
        img = img.transpose(Image.Transpose.ROTATE_90)
        img.save(file_name)
        
        Unit.mqttServer.publish_file()
        # dithered_image.show()
        return(self.buffImg(self, dithered_image))

class ImageRender:
    def get_addon_color(image):
        # 获取图片的宽度和高度
        width, height = image.size

        # 计算取样范围的左上角和右下角坐标
        left = 0
        top = 600
        right = 480
        bottom = 800

        # 获取取样范围内的像素颜色列表
        pixel_colors = []
        for x in range(left, right):
            for y in range(top, bottom):
                pixel_colors.append(image.getpixel((x, y)))

        # 计算平均背景颜色
        total_color = [0, 0, 0]
        for color in pixel_colors:
            total_color[0] += color[0]
            total_color[1] += color[1]
            total_color[2] += color[2]

        num_pixels = len(pixel_colors)
        background_color = (
            total_color[0] // num_pixels,
            total_color[1] // num_pixels,
            total_color[2] // num_pixels,
        )

        # 计算背景颜色的亮度
        brightness = (0.299 * background_color[0] + 0.587 * background_color[1] + 0.114 * background_color[2]) / 255

        # 根据背景亮度选择文字颜色
        if brightness > 0.5:
            text_color = (64, 64, 64, 255)  # 选择黑色文字
        else:
            text_color = (200, 200, 200, 255)  # 选择白色文字
        return text_color
    
    #本类的渲染都是基于宽 480px，高 800px 的图片，渲染完再经过 ImageDriver 的旋转方法
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

        #使用遮罩将高斯模糊的图层加到原图中
        mask = Image.new('L', image.size, 255)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle(xy=[[16, height - 16 - 200], [width - 16, height - 16]],radius=16,fill=0)
        draw_blur_outline = ImageDraw.Draw(blur_image)
        draw_blur_outline.rounded_rectangle(xy=[[16, height - 16 - 200], [width - 16, height - 16]],radius=16,outline= self.get_addon_color(image), width=4)
        output = Image.composite(image ,blur_image, mask)
        return output
    
    def add_description_text(self, image:Image.Image):
        # 在图片底部高为 200px, 左右 padding 为 16 px 的框中进行渲染
        draw_description = ImageDraw.Draw(image)
        draw_description.multiline_text(xy= [40, 600], text= "你好呀，有何贵干！",fill=self.get_addon_color(image),font=ImageFont.truetype('./src/pingfang.ttf',size=18))
        return image
        



