import cv2
import numpy as np

def add_watermark(src, dest, watermark):
    image = cv2.imdecode(np.fromfile(src, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    watermark = cv2.imread(watermark, cv2.IMREAD_UNCHANGED)

    # 调整水印大小与位置
    scale_percent = 10  # 缩放百分比
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    resized_watermark = cv2.resize(watermark, (width, height), interpolation=cv2.INTER_LINEAR)
    x = image.shape[1] - resized_watermark.shape[1] - 10  # 水印位置在右下角
    y = image.shape[0] - resized_watermark.shape[0] - 10

    # 将水印图像叠加到原始图像上
    for c in range(0, 3):
        image[y:y+resized_watermark.shape[0], x:x+resized_watermark.shape[1], c] = \
            resized_watermark[:, :, c] * (resized_watermark[:, :, 3] / 255.0) + \
            image[y:y+resized_watermark.shape[0], x:x+resized_watermark.shape[1], c] * \
            (1.0 - resized_watermark[:, :, 3] / 255.0)

    # 显示带水印的图像
    # cv2.imshow('Watermarked Image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite(dest, image)

    # 保存到中文路径
    cv2.imencode('.jpg', image)[1].tofile(dest)