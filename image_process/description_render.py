from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont

from common.unit import Unit

class DescriptionRender:
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
    
    def add_description_text(self, image:Image.Image, description: str):
        # 在图片底部高为 200px, 左右 padding 为 16 px 的框中进行渲染
        draw_description = ImageDraw.Draw(image)
        draw_description.multiline_text(xy= [40, 600], text= description ,fill=self.get_addon_color(image),font=ImageFont.truetype('./src/pingfang.ttf',size=18))
        return image
        



