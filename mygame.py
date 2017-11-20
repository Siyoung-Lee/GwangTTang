import game_framework
from pico2d import*
# fill here
import pygame

import hwatwo_solitaire
import solitaire

open_canvas()
game_framework.run(solitaire) # start_state의 enter가 제일 먼저 실행(함수를 차근차근 실행)
close_canvas()