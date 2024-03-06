from PIL import Image
import os
import glob


def vertical_concatenate_images(images, first_image=0, first_image_crop_height=None, other_images_crop_range=None):
    """
    将一组图像垂直拼接成一张长图。

    Args:
        images (str or list): 图像文件夹路径或图像文件路径列表。
        first_image (int or str, optional): 第一张图像的索引或文件名。默认为 0。
        first_image_crop_height (int, optional): 第一张图像的裁剪高度。默认为 None。
        other_images_crop_range (tuple, optional): 其他图像的裁剪范围 (start, end)。默认为 None。

    Returns:
        Image: 拼接后的图像对象。
    """
    image_list = []

    if isinstance(images, str):
        # 如果输入是文件夹路径，则加载所有图像文件
        image_list = [Image.open(image_path) for image_path in glob.glob(
            os.path.join(images, '*.png')) + glob.glob(os.path.join(images, '*.jpg'))]
    elif isinstance(images, list):
        # 如果输入是图像文件路径列表，则直接加载这些图像
        image_list = [Image.open(image_path) for image_path in images]
    else:
        raise ValueError('images must be a folder path or a list of image paths')

    if first_image is not None:
        if isinstance(first_image, int):
            # 如果 first_image 是索引，将第一张图像移到指定位置
            if first_image < 0 or first_image >= len(image_list):
                raise ValueError('first_image index out of range')
        else:
            # 如果 first_image 是文件名，将对应的图像移到第一位
            first_image = Image.open(first_image)
            image_list.insert(0, first_image)

    if first_image_crop_height is not None:
        # 裁剪第一张图像的高度
        image_list[0] = image_list[0].crop((0, 0, image_list[0].width, first_image_crop_height))

    if other_images_crop_range:
        # 裁剪其他图像的范围
        for i in range(1, len(image_list)):
            image_list[i] = image_list[i].crop(
                (0, other_images_crop_range[0], image_list[i].width, other_images_crop_range[1]))

    total_height = sum(image.height for image in image_list)
    max_width = max(image.width for image in image_list)
    new_im = Image.new('RGB', (max_width, total_height))

    y_offset = 0
    for image in image_list:
        new_im.paste(image, (0, y_offset))
        y_offset += image.height

    return new_im


# 示例用法：
result_image = vertical_concatenate_images(images='图片目录', first_image=0, other_images_crop_range=(600, 700))
result_image.show()
