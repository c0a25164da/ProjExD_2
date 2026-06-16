import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP : (0, -5),
    pg.K_DOWN : (0, +5),
    pg.K_LEFT : (-5, 0),
    pg.K_RIGHT : (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：判定結果タプル（横判定結果, 縦判定結果）
    True : 画面内 / False : 画面外
    """
    yoko, tate, = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def game_over(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する
    引数：screen
    戻り値：なし
    """
    bg_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bg_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    bg_img.set_alpha(200)

    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = (WIDTH // 2, HEIGHT // 2)
    bg_img.blit(txt, txt_rct)
    kk_img = pg.image.load("fig/8.png")
    kk_rct = kk_img.get_rect()
    
    
    kk_rct.center = WIDTH // 4, HEIGHT // 2
    bg_img.blit(kk_img, kk_rct)
    kk_rct.center = (WIDTH // 4)*3, HEIGHT // 2
    bg_img.blit(kk_img, kk_rct)

    screen.blit(bg_img, (0, 0))
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    時間と共に爆弾が拡大、加速する
    引数；なし
    戻り値：タプル(リスト[画像], リスト[加速度])
    """
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0)) 
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    
    bb_accs = [a for a in range(1, 11)]

    return (bb_imgs, bb_accs)


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    飛ぶ方向に従ってこうかとん画像を切り替える
    引数：なし
    戻り値：dict{向き: 画像}
    """
    kk_img = pg.image.load("fig/3.png")
    kk_flip = pg.transform.flip(kk_img, True, False)
    kk_dict = {
        (0, 0): pg.transform.rotozoom(kk_img, 0, 1),
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 1),
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1),
        (0, -5): pg.transform.rotozoom(kk_img, -90, 1),
        (+5, -5): pg.transform.rotozoom(kk_flip, 45, 1),
        (+5, 0): pg.transform.rotozoom(kk_flip, 0, 1),
        (+5, +5): pg.transform.rotozoom(kk_flip, -45, 1),
        (0, +5): pg.transform.rotozoom(kk_img, 90, 1),
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 1),
    }

    return kk_dict


def preparation(screen: pg.Surface) -> bool:
    """
    ロード画面を表示するもの
    引数：screen
    戻り値：True
    """
    count = 3
    fonto = pg.font.Font(None, 100)

    bg_copy = screen.copy()

    clock = pg.time.Clock()

    while True:

        screen.blit(bg_copy, [0, 0])

        if count <= 0:
            count = "GO!!!"

        txt = fonto.render(f"{count}", True, (0, 0, 0))
        txt_rect = txt.get_rect()
        txt_rect.center = (WIDTH // 2, HEIGHT // 2)

        screen.blit(txt, txt_rect) 

        pg.display.update()
        
        start_time = pg.time.get_ticks()
        while pg.time.get_ticks() - start_time < 1000:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False

            clock.tick(60)


        if type(count) == int:
            count -= 1
        else:
            break
    return True

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")  
    kk_dict = get_kk_imgs()  
    kk_img = kk_dict[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    tmr = 0
    score = 0
    judge_pre = False
    bb_imgs, bb_accs = init_bb_imgs()
    vx, vy = +5, +5
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
            
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            print("爆！")
            return
        screen.blit(bg_img, [0, 0])

        if not judge_pre:
            pg.display.update()
            judge_pre = preparation(screen)
            if not judge_pre:
                return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横方向移動
                sum_mv[1] += mv[1]  # 縦方向移動
        kk_img = kk_dict[tuple(sum_mv)]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bb_rct.move_ip(vx*bb_accs[min(tmr // 500, 9)], vy*bb_accs[min(tmr // 500, 9)])
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_imgs[min(tmr // 500, 9)], bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
