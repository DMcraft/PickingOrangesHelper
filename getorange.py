import math
from PIL import ImageGrab
from loguru import logger as log

top_X, top_Y = 0, 0
bottom_X, bottom_Y = 640, 480
step_X, step_Y = 5, 5
centerX, centerY = 320, 240
mas_snake = None


def initial_module(t_x, t_y, b_x, b_y, s_x, s_y):
    global mas_snake
    global top_X, top_Y, bottom_X, bottom_Y, step_X, step_Y, centerX, centerY
    top_X, top_Y = t_x, t_y
    bottom_X, bottom_Y = b_x, b_y
    step_X, step_Y = s_x, s_y
    centerX, centerY = (bottom_X - top_X) // 2, (bottom_Y - top_Y) // 2
    mas_snake = list(generate_snake_list(bottom_X - top_X, bottom_Y - top_Y, step_X, step_Y))


def generate_snake_list(width, height, s_x, s_y):
    moveX = cX = width // 2
    moveY = cY = height // 2
    area = [
        (0, width, 0, height),
        (cX - 50, cX + 50, cY - 200, cY),
        (0, 250, 0, 150)
    ]
    rotor = ((1, 0), (0, 1), (-1, 0), (0, -1))
    rotate = 0
    move_step = 1
    move_step_double = False
    while moveX > 0 or moveY > 0:
        for _ in range(move_step):
            moveX += rotor[rotate][0] * s_x
            moveY += rotor[rotate][1] * s_y
            if width > moveX > 0 and height > moveY > 0:
                # todo add filter exclude area +
                if not (cX - 50 < moveX < cX + 50 and cY - 200 < moveY < cY):
                    if not (moveX < 250 and moveY < 150):
                        yield moveX, moveY

        if move_step_double:
            move_step_double = False
            move_step += 1
        else:
            move_step_double = True
        rotate = 0 if rotate == 3 else rotate + 1


def compare_pixels(pix_a: set, pix_b: set, conf=1) -> bool:
    for a, b in zip(pix_a, pix_b):
        if not b - conf < a < b + conf:
            return False
    else:
        return True


def search_block_in_screen(pixelRGB, dangerRGB=(103, 130, 72)):
    im = ImageGrab.grab().crop((top_X, top_Y, bottom_X, bottom_Y))
    # crop function crop_img = img[10:450, 300:750] -> this numpy object
    RADIUS_DANGER = 150
    # find danger zone, scan circle 24 hour
    for i in range(24):
        angle = (2 * math.pi / 24) * i
        x = int(RADIUS_DANGER * math.sin(angle))
        y = int(RADIUS_DANGER * math.cos(angle))
        if im.getpixel((x + centerX, y + centerY)) == dangerRGB:
            x = int(400 * math.sin(angle))
            y = int(400 * math.cos(angle))
            return centerX - x + top_X, centerY - y + top_Y

    for X, Y in mas_snake:
        if (pixelRGB == im.getpixel((X, Y)) and pixelRGB == im.getpixel((X + 1, Y)) and
                pixelRGB == im.getpixel((X, Y + 1)) and pixelRGB == im.getpixel((X + 1, Y + 1))):
            return X + top_X, Y + top_Y
    return None

if __name__ == '__main__':
    log.info('This module not start from main...')
