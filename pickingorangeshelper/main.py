"""The script of picking an orange from a forest game.
URL original games: https://paperanimals.io
Need fo example:
1. Dominate the forest
2. Specify the boundaries of the game window
3. Start collecting
For end, fast move cursor in upper left corner of screen

"""

import pyautogui as pag
import tkinterweb
import tkinter as tk
import time
import getorange
from loguru import logger as log

ORANGE = (255, 133, 10)
DANGER = (48, 110, 155)
scrTopX, scrTopY = 0, 0
scrBottomX, scrBottomY = 1920, 1080
scrCenterX, scrCenterY = pag.center((scrTopX, scrTopY, scrBottomX, scrBottomY))


def set_coordinate_window():
    global scrTopX, scrTopY, scrBottomX, scrBottomY, scrCenterX, scrCenterY
    pos_mouse = 0
    while not pag.position() == pos_mouse:
        pos_mouse = pag.position()
        time.sleep(1)
    lbl_coordinate_ul['text'] = f'{pos_mouse}'
    scrTopX, scrTopY = pos_mouse
    pag.moveTo(scrCenterX, scrCenterY)
    while not pag.position() == pos_mouse:
        pos_mouse = pag.position()
        time.sleep(1)
    lbl_coordinate_dr['text'] = f'{pos_mouse}'
    scrBottomX, scrBottomY = pos_mouse
    scrCenterX, scrCenterY = ((scrBottomX - scrTopX) // 2 + scrTopX,
                              (scrBottomY - scrTopY) // 2 + scrTopY)
    pag.moveTo(scrCenterX, scrCenterY)
    lbl_coordinate_center['text'] = f'{scrCenterX, scrCenterY}'


def start_game():
    getorange.initial_module(scrTopX, scrTopY, scrBottomX, scrBottomY, 5, 5)
    t_back = t_push = time.time()
    while not pag.position() == (0, 0):
        try:
            x, y = getorange.search_block_in_screen(ORANGE)
            pag.moveTo(x, y)
            t_back = time.time()

            if time.time() - t_push > 11:
                log.debug(t_push - time.time())
                t_push = time.time()
                pag.leftClick(x, y)

        except TypeError:
            # log.info('Not find block')

            pass
        except Exception as err:
            log.debug(f"Unexpected {err=}, {type(err)=}")
        time.sleep(1 / 10)
        if time.time() - t_back > 1:
            t_back = time.time()
            pag.moveTo(scrCenterX * 2 - x, scrCenterY * 2 - y)


def main_external_browser():
    global lbl_coordinate_ul, lbl_coordinate_dr, lbl_coordinate_center
    window = tk.Tk()
    window.title("Автоматизация сбора лесного урожая")
    window.geometry('%dx%d+%d+%d' % (350, 180, 1400, 50))
    frame1 = tk.Frame()
    frame1.pack(fill=tk.X)
    tk.Label(text='Coordinate up-left:', width=20, justify='left', master=frame1).pack(side=tk.LEFT)
    lbl_coordinate_ul = tk.Label(frame1, text=f'{scrTopX, scrTopY}')
    lbl_coordinate_ul.pack(side=tk.LEFT)

    frame2 = tk.Frame()
    frame2.pack(fill=tk.X)
    tk.Label(text='Coordinate dn-right: ', width=20, justify='left', master=frame2).pack(side=tk.LEFT)
    lbl_coordinate_dr = tk.Label(frame2, text=f'{scrBottomX, scrBottomY}')
    lbl_coordinate_dr.pack(side=tk.LEFT)

    frame3 = tk.Frame()
    frame3.pack(fill=tk.X)
    tk.Label(text='Coordinate center: ', width=20, justify='left', master=frame3).pack(side=tk.LEFT)
    lbl_coordinate_center = tk.Label(frame3, text=f'{scrCenterX, scrCenterY}')
    lbl_coordinate_center.pack(side=tk.LEFT)

    tk.Button(text='Set coordinate', command=set_coordinate_window).pack(fill=tk.X)
    tk.Button(text='Start GAME', command=start_game, height=4, bg='green').pack(fill=tk.X)

    tk.Label(text='** for CANCEL, move cursor to upper left corner of the screen').pack()

    window.mainloop()


def main():
    YOUR_WEBSITE = 'https://yandex.ru/games/app/163861'
    root = tk.Tk()
    frame_com = tk.Frame()
    frame_com.pack(side=tk.LEFT, fill=tk.Y)
    tk.Button(frame_com, text='GET apples', command=start_game, width=10, height=4, bg='green').pack(fill=tk.X)

    frame = tkinterweb.HtmlFrame(root)
    frame.load_website(YOUR_WEBSITE)
    frame.pack(side=tk.LEFT, fill="both", expand=True)
    root.mainloop()


if __name__ == '__main__':
    main_external_browser()
else:
    log.info('Not start, module not main!')
