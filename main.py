from PIL import Image


# 图像加密
def ImageEncrypt(image_path, output_path, data):
    # 打开图像并获取像素数据
    img = Image.open(image_path)
    img_data = list(img.getdata())

    # 将密码转换为二进制格式
    binary_data = ''.join(format(ord(i), '08b') for i in data)

    # 确保数据不会溢出
    if len(binary_data) > len(img_data) * 8:
        raise ValueError("Insufficient space in the image to embed the data")

    data_index = 0
    new_data = []

    for pixel in img_data:
        pixel = list(pixel)
        for color_channel in range(3):  # 对于每个 RGB 颜色通道
            if data_index < len(binary_data):
                # 修改像素颜色通道的最低有效位
                pixel[color_channel] = pixel[color_channel] & ~1 | int(binary_data[data_index])
                data_index += 1
            else:
                break
        new_data.append(tuple(pixel))

    # 创建一个新图像并保存修改后的数据
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_data)
    new_img.save(output_path)


# 图像解密
def ImageDecrypt(image_path, data_length):
    img = Image.open(image_path)
    img_data = list(img.getdata())

    binary_data = ""

    # 提取位图数据区中的二进制数据
    for i in range(data_length * 8):
        pixel = img_data[i // 3]
        color_channel = i % 3
        binary_data += str(pixel[color_channel] & 1)

    # 将二进制数据转换回原始字符串
    extracted_data = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))
    return extracted_data


if __name__ == "__main__":
    bmp_file = "/Users/wangjian/code/python/Bmp/img.bmp"
    output_file = "/Users/wangjian/code/python/Bmp/encrypt.bmp"
    secret_data = "This is my secret message"
    ImageEncrypt(bmp_file, output_file, secret_data)
    print(ImageDecrypt(output_file, len(secret_data)))
