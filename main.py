import sys
import pygame

player_id = sys.argv[1:5]

WIDTH, HEIGHT = 1920, 1080
SCALE_SIZE = 144, 100
BG_COLOR = (30, 30, 30)

MAP_FILES = []
INFO_FILES = []
for i in range(96):
    MAP_FILES.append("map/"+str((i+1)//10)+str((i+1)%10)+".png")
    INFO_FILES.append("info/"+str((i+1)//10)+str((i+1)%10)+".png")


POSITIONS = []

for i in range(8):
    for j in range(12):
        POSITIONS.append((63 + j * 150, 30 + i * 105))

PLAYER_COLORS = [(255, 0, 0, 100), (255, 255, 0, 100), (0, 0, 255, 100), (0, 255, 0, 100)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CSMK 2025 Ban/Pick")
clock = pygame.time.Clock()

background_image = pygame.image.load("background.png").convert_alpha()
image = pygame.image.load("banned.png").convert_alpha()
banned_image = pygame.transform.scale(image, SCALE_SIZE)
image = pygame.image.load("picked.png").convert_alpha()
picked_image = pygame.transform.scale(image, SCALE_SIZE)

class BanMask(pygame.sprite.Sprite):
    def __init__(self, pos=(0,0)):
        super().__init__()
        raw_img = pygame.image.load("banned.png").convert_alpha()
        self.image = pygame.transform.scale(raw_img, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect(topleft=pos)

class PickMask(pygame.sprite.Sprite):
    def __init__(self, pos=(0,0)):
        super().__init__()
        raw_img = pygame.image.load("picked.png").convert_alpha()
        self.image = pygame.transform.scale(raw_img, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect(topleft=pos)

class MapSprite(pygame.sprite.Sprite):
    def __init__(self, map_path, info_path, pos):
        super().__init__()
        raw_img = pygame.image.load(map_path).convert_alpha()
        self.map_path = pygame.transform.smoothscale(raw_img, SCALE_SIZE)
        self.info_path = pygame.image.load(info_path).convert_alpha()
        self.image = self.map_path.copy()
        self.rect = self.image.get_rect(topleft=pos)
        self.selected_by = None

    def apply_mask(self, color):
        mask = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        mask.fill(color)
        self.image = self.map_path.copy()
        self.image.blit(mask, (0, 0))
        if stage == 0:
            self.image.blit(banned_image, (0,0))
        if stage == 1:
            self.image.blit(picked_image, (0,0))

def play_animation(screen, image):
    duration = 1000
    start = pygame.time.get_ticks()
    center = screen.get_rect().center
    frame, frame_rect = 0,0
    while True:
        now = pygame.time.get_ticks()
        progress = (now - start) / duration
        if progress > 1:
            break
        scale = 0.2 + 0.8 * progress
        frame = pygame.transform.scale(image, (int(1920 * scale), int(1080 * scale)))
        frame_rect = frame.get_rect(center=center)
        screen.blit(background_image, (0, 0))
        screen.blit(frame, frame_rect)
        pygame.display.flip()

    if stage == 0:
        duration = 1000
        start = pygame.time.get_ticks()
        progress = 0

        banned = True

        while banned:
            now = pygame.time.get_ticks()
            progress = (now - start) / duration
            if progress > 1:
                progress = 1
            bg.rect.y = -540 + progress * 540
            screen.blit(frame, frame_rect)
            bgs.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    banned = False
                    break           
            pygame.display.flip()
    if stage == 1:
        duration = 1000
        start = pygame.time.get_ticks()
        progress = 0

        banned = True

        while banned:
            now = pygame.time.get_ticks()
            progress = (now - start) / duration
            if progress > 1:
                progress = 1
            bg2.rect.y = -540 + progress * 540
            screen.blit(frame, frame_rect)
            bgs2.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    banned = False
                    break
            
            pygame.display.flip()
    screen.blit(background_image, (0, 0))
    maps.draw(screen)
    pygame.display.flip()

maps = pygame.sprite.Group()
for i, file in enumerate(zip(MAP_FILES,INFO_FILES)):
    sprite = MapSprite(file[0], file[1], POSITIONS[i])
    maps.add(sprite)

current_player = 3
running = True

bg = BanMask()
bgs = pygame.sprite.Group()
bgs.add(bg)

bg2 = PickMask()
bgs2 = pygame.sprite.Group()
bgs2.add(bg2)

stage = 0

screen.blit(background_image, (0, 0))
maps.draw(screen)
pygame.display.flip()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and stage == 0:
            mouse_pos = pygame.mouse.get_pos()
            for m in maps:
                if m.rect.collidepoint(mouse_pos) and m.selected_by is None:
                    m.selected_by = current_player
                    m.apply_mask(PLAYER_COLORS[current_player])
                    play_animation(screen, m.info_path)
                    current_player -= 1
                    if current_player == -1:
                        current_player = 4
                        stage = 1
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and stage == 1:
            mouse_pos = pygame.mouse.get_pos()
            for m in maps:
                if m.rect.collidepoint(mouse_pos) and m.selected_by is None:
                    m.selected_by = current_player % 4
                    m.apply_mask(PLAYER_COLORS[current_player % 4])
                    play_animation(screen, m.info_path)
                    current_player += 1
                    break
    
    if stage == 0:
        font = pygame.font.SysFont("simhei", 96)
        text = font.render(" Player "+player_id[current_player % 4]+" Ban ", True, (0,0,0), PLAYER_COLORS[current_player % 4])
        screen.blit(text, (63,1010))
        pygame.display.flip()
    if stage == 1:
        font = pygame.font.SysFont("simhei", 96)
        text = font.render(" Player "+player_id[current_player % 4]+" Round "+str(current_player // 4)+" Pick ", True, (0,0,0), PLAYER_COLORS[current_player % 4])
        screen.blit(text, (63,1010))
        pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()