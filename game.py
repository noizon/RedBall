import pygame
import sys
import math
import random
import json
import os

# =============================================
# НАСТРОЙКИ
# =============================================
WIDTH, HEIGHT = 900, 600
FPS = 60
GRAVITY = 0.8
JUMP_POWER = -14
DOUBLE_JUMP_POWER = -12
PLAYER_SPEED = 6
FRICTION = 0.85
MAX_FALL_SPEED = 15

# =============================================
# ЦВЕТА
# =============================================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
DARK_RED = (180, 20, 20)
GREEN = (50, 255, 50)
DARK_GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
SKY_BLUE = (135, 206, 235)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (160, 100, 40)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
DARK_BLUE = (25, 25, 112)
HEALTH_GREEN = (0, 255, 0)
HEALTH_YELLOW = (255, 255, 0)
HEALTH_RED = (255, 0, 0)
HEALTH_BG = (40, 40, 40)
CYAN = (0, 255, 255)
BLUE = (50, 150, 255)
NEON_GREEN = (0, 255, 100)
DARK_PURPLE = (50, 0, 80)
LAVA = (200, 80, 0)
ICE_BLUE = (150, 220, 255)
PINK = (255, 150, 200)
WATER_BLUE = (0, 100, 200)
SHADOW_PURPLE = (80, 0, 120)
NEON_ORANGE = (255, 150, 0)
FOREST_GREEN = (34, 139, 34)
DARK_FOREST = (20, 80, 20)
ICE_WHITE = (220, 240, 255)
VOLCANO_RED = (200, 60, 20)
CASTLE_PURPLE = (40, 20, 60)

# =============================================
# ТЕМЫ УРОВНЕЙ
# =============================================
LEVEL_THEMES = {
    1: {"name": "🌿 Лесная опушка", "bg": (34, 139, 34), "platform": (139, 69, 19), "enemy": (255, 80, 80)},
    2: {"name": "🌳 Густой лес", "bg": (30, 120, 30), "platform": (160, 80, 30), "enemy": (255, 70, 70)},
    3: {"name": "🌲 Лесная чаща", "bg": (25, 110, 25), "platform": (120, 60, 20), "enemy": (200, 60, 60)},
    4: {"name": "🌄 Лесной хребет", "bg": (40, 130, 40), "platform": (140, 70, 25), "enemy": (220, 80, 80)},
    5: {"name": "🍄 Логово грибного босса", "bg": (20, 80, 20), "platform": (100, 50, 15), "enemy": (200, 50, 50)},
    6: {"name": "❄️ Ледяная пещера", "bg": (200, 230, 255), "platform": (180, 220, 255), "enemy": (100, 200, 255)},
    7: {"name": "🧊 Ледяной лабиринт", "bg": (190, 220, 250), "platform": (170, 210, 250), "enemy": (80, 190, 255)},
    8: {"name": "🌨️ Заснеженные пики", "bg": (210, 235, 255), "platform": (200, 230, 255), "enemy": (120, 210, 255)},
    9: {"name": "🧊 Ледяные сталактиты", "bg": (180, 210, 245), "platform": (160, 200, 245), "enemy": (90, 180, 255)},
    10: {"name": "👹 Логово ледяного голема", "bg": (160, 200, 240), "platform": (140, 190, 240), "enemy": (70, 170, 255)},
    11: {"name": "🌋 Вулканический склон", "bg": (180, 60, 20), "platform": (120, 50, 20), "enemy": (255, 150, 50)},
    12: {"name": "🔥 Лавовые реки", "bg": (200, 70, 30), "platform": (140, 55, 25), "enemy": (255, 160, 60)},
    13: {"name": "🌋 Кратер вулкана", "bg": (220, 80, 40), "platform": (160, 60, 30), "enemy": (255, 170, 70)},
    14: {"name": "🔥 Огненные каньоны", "bg": (190, 65, 25), "platform": (130, 50, 20), "enemy": (255, 140, 40)},
    15: {"name": "👹 Логово огненного демона", "bg": (210, 75, 35), "platform": (150, 55, 25), "enemy": (255, 180, 80)},
    16: {"name": "🏰 Темный замок", "bg": (40, 20, 60), "platform": (80, 50, 100), "enemy": (200, 100, 255)},
    17: {"name": "🌑 Замковые подземелья", "bg": (30, 15, 50), "platform": (70, 40, 90), "enemy": (180, 80, 255)},
    18: {"name": "🕯️ Тронный зал", "bg": (50, 25, 70), "platform": (90, 55, 110), "enemy": (220, 120, 255)},
    19: {"name": "🌙 Башня мага", "bg": (35, 20, 55), "platform": (75, 45, 95), "enemy": (190, 90, 255)},
    20: {"name": "👑 Финальный босс", "bg": (60, 30, 80), "platform": (100, 60, 120), "enemy": (255, 150, 255)},
}

# =============================================
# ИНИЦИАЛИЗАЦИЯ
# =============================================
pygame.init()
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    audio_available = True
except:
    audio_available = False

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Red Ball Adventure")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 60)
huge_font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 24)

fullscreen = False
cutscene_played = False

# =============================================
# ЗВУКИ (программная генерация)
# =============================================
import array

def generate_sound(frequency, duration, volume=0.3):
    """Генерирует звук программно, без файлов"""
    if not audio_available:
        return None
    try:
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        buf = array.array('h')
        for i in range(n_samples):
            t = i / sample_rate
            amp = int(32767 * volume * (1 - i / n_samples))
            sample = int(amp * math.sin(2 * math.pi * frequency * t))
            buf.append(sample)
            buf.append(sample)
        return pygame.mixer.Sound(buffer=buf.tobytes())
    except:
        return None

SOUND_JUMP = generate_sound(600, 0.1, 0.15)
SOUND_DOUBLE_JUMP = generate_sound(900, 0.12, 0.2)
SOUND_COIN = generate_sound(1200, 0.08, 0.15)
SOUND_HIT = generate_sound(200, 0.15, 0.2)
SOUND_DEATH = generate_sound(150, 0.5, 0.3)
SOUND_WIN = generate_sound(1500, 0.3, 0.2)
SOUND_POWERUP = generate_sound(1800, 0.2, 0.2)
SOUND_BOSS_HIT = generate_sound(400, 0.1, 0.2)

def play_sound(sound):
    if sound:
        try:
            sound.play()
        except:
            pass

# =============================================
# ЗАГРУЗКА/СОХРАНЕНИЕ ПРОГРЕССА
# =============================================
SAVE_FILE = "save_data.json"

def load_progress():
    global unlocked_levels, max_unlocked, deaths, current_level, cutscene_played
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                data = json.load(f)
                unlocked_levels = data.get('unlocked_levels', [1])
                max_unlocked = data.get('max_unlocked', 1)
                deaths = data.get('deaths', 0)
                current_level = data.get('current_level', 1)
                cutscene_played = data.get('cutscene_played', False)
        except:
            unlocked_levels = [1]
            max_unlocked = 1
            deaths = 0
            current_level = 1
            cutscene_played = False
    else:
        unlocked_levels = [1]
        max_unlocked = 1
        deaths = 0
        current_level = 1
        cutscene_played = False

def save_progress():
    data = {
        'unlocked_levels': unlocked_levels,
        'max_unlocked': max_unlocked,
        'deaths': deaths,
        'current_level': current_level,
        'cutscene_played': cutscene_played
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)

# =============================================
# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
# =============================================
unlocked_levels = [1]
max_unlocked = 1
deaths = 0
current_level = 1
load_progress()

# =============================================
# НОВЫЕ СИСТЕМЫ: ЦИФРЫ УРОНА, КОМБО, БОНУСЫ
# =============================================
damage_numbers = []
combo = 0
combo_timer = 0
level_start_time = 0
total_kills = 0
total_jumps = 0
paused = False

class DamageNumber:
    def __init__(self, x, y, value, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.value = str(value)
        self.color = color
        self.life = 60
        self.vy = -1.5

    def update(self):
        self.y += self.vy
        self.vy *= 0.95
        self.life -= 1
        return self.life > 0

    def draw(self, screen, ox, oy):
        alpha = min(1, self.life / 30)
        f = pygame.font.Font(None, 32)
        text = f.render(self.value, True, self.color)
        text.set_alpha(int(255 * alpha))
        screen.blit(text, (self.x - ox - text.get_width()//2, self.y - oy))

# =============================================
# КАТ-СЦЕНА
# =============================================
def play_cutscene():
    global cutscene_played, menu_state, current_level
    if cutscene_played:
        return
    cutscene_running = True
    frame = 0
    dialogue_index = 0
    char_index = 0
    text_display = ""
    timer = 0
    dialogue_stage = 0
    hero_x = 50
    hero_y = 450
    hero_radius = 20
    hero_speed = 2.5
    friend_colors = [GREEN, YELLOW, ORANGE, PURPLE, CYAN, PINK, BLUE, GOLD]
    friends = []
    for i in range(8):
        friends.append({
            'x': 150 + i * 85,
            'y': 450 + random.randint(-15, 15),
            'radius': 14,
            'color': random.choice(friend_colors),
            'alive': True,
            'death_timer': 0
        })
    boss_x = 850
    boss_y = 440
    boss_radius = 40
    boss_visible = False
    dialogues = [
        {"speaker": "Главный герой", "text": "Что здесь происходит?!", "delay": 120},
        {"speaker": "Босс", "text": "Ха-ха! Смотри, как я уничтожаю твоих друзей!", "delay": 150},
        {"speaker": "Главный герой", "text": "Как ты смеешь! Я отомщу за них!", "delay": 130},
        {"speaker": "Босс", "text": "Посмотрим, что ты сможешь сделать, маленький шарик!", "delay": 140},
        {"speaker": "Главный герой", "text": "Ты пожалеешь! Я уничтожу всех боссов!", "delay": 130},
        {"speaker": "Босс", "text": "Ха-ха-ха! Попробуй! Иди за мной, если посмеешь!", "delay": 150},
    ]
    def draw_cutscene_background(scroll_x):
        for i in range(HEIGHT):
            ratio = i / HEIGHT
            r = int(135 - ratio * 40)
            g = int(206 - ratio * 50)
            b = int(235 - ratio * 40)
            pygame.draw.line(screen, (r, g, b), (0, i), (WIDTH, i))
        sx, sy = 780 - scroll_x * 0.02, 60
        for i in range(25, 0, -2):
            alpha = 255 - i * 8
            if alpha > 0:
                pygame.draw.circle(screen, (255, 200, 50, alpha), (int(sx), int(sy)), 45 + i)
        pygame.draw.circle(screen, (255, 230, 100), (int(sx), int(sy)), 45)
        pygame.draw.circle(screen, (255, 255, 200), (int(sx - 6), int(sy - 10)), 18)
        mountains = [
            (0, 160, 220, (70, 110, 150)),
            (220, 110, 260, (90, 130, 170)),
            (480, 130, 200, (60, 100, 140)),
            (700, 190, 240, (80, 120, 160)),
        ]
        for mx, mh, mw, mc in mountains:
            x = mx - scroll_x * 0.1
            if x > -mw and x < WIDTH + mw:
                points = [(x, HEIGHT), (x + mw//2, HEIGHT - mh), (x + mw, HEIGHT)]
                pygame.draw.polygon(screen, mc, points)
        for i in range(3):
            pygame.draw.ellipse(screen, (80 - i*10, 200 - i*15, 80 - i*10), (-50 + i*100, 490 + i*10, WIDTH + 200 - i*150, 100 - i*10))
        for i in range(0, WIDTH + 100, 30):
            x = (i - scroll_x * 0.2) % (WIDTH + 200) - 100
            y = 500 + math.sin(i * 0.1 + scroll_x * 0.01) * 8
            flower_color = random.choice([(255, 100, 100), (255, 200, 100), (200, 100, 255)])
            pygame.draw.circle(screen, flower_color, (int(x), int(y)), 3)
            pygame.draw.circle(screen, YELLOW, (int(x), int(y)), 1)
        clouds = [(100, 50, 140), (350, 30, 170), (600, 60, 120), (850, 40, 150)]
        for cx, cy, cw in clouds:
            x = (cx - scroll_x * 0.02) % (WIDTH + 400) - 200
            y = cy + math.sin(pygame.time.get_ticks() / 5000 + cx) * 6
            for i in range(4):
                px = x + i * cw // 4
                py = y + math.sin(i * 1.5 + pygame.time.get_ticks() / 3000) * 4
                r = cw // 5 + 4
                pygame.draw.circle(screen, (255, 255, 255, 160), (int(px), int(py)), r)
    while cutscene_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    cutscene_running = False
                    break
        frame += 1
        if hero_x < 350:
            hero_x += hero_speed
        else:
            hero_x += 0.5
        if frame > 80 and not boss_visible:
            boss_visible = True
        if boss_visible and boss_x > 500:
            boss_x -= 2
        elif boss_visible:
            boss_x = 500
        for i, friend in enumerate(friends):
            if friend['alive'] and frame > 120 + i * 50:
                friend['alive'] = False
                friend['death_timer'] = 30
        for friend in friends:
            if not friend['alive'] and friend['death_timer'] > 0:
                friend['death_timer'] -= 1
        if frame > 160 and dialogue_index < len(dialogues):
            current = dialogues[dialogue_index]
            if dialogue_stage == 0:
                if timer == 0:
                    text_display = ""
                    char_index = 0
                    timer = 2
                if char_index < len(current["text"]):
                    text_display += current["text"][char_index]
                    char_index += 1
                    pygame.time.delay(20)
                else:
                    dialogue_stage = 1
                    timer = current["delay"]
            else:
                timer -= 1
                if timer <= 0:
                    dialogue_index += 1
                    dialogue_stage = 0
                    timer = 0
                    char_index = 0
                    text_display = ""
        scroll_x = hero_x - 150 if hero_x > 150 else 0
        draw_cutscene_background(scroll_x)
        for friend in friends:
            if friend['alive']:
                pygame.draw.ellipse(screen, (0, 0, 0, 50), (int(friend['x'] - 18), int(friend['y'] + 12), 36, 10))
        pygame.draw.ellipse(screen, (0, 0, 0, 60), (int(hero_x - 25), int(hero_y + 15), 50, 12))
        if boss_visible:
            pygame.draw.ellipse(screen, (0, 0, 0, 70), (int(boss_x - 45), int(boss_y + 20), 90, 18))
        for friend in friends:
            if friend['alive']:
                pygame.draw.circle(screen, friend['color'], (int(friend['x']), int(friend['y'])), friend['radius'])
                pygame.draw.circle(screen, (255, 255, 255, 80), (int(friend['x'] - 3), int(friend['y'] - 4)), friend['radius'] - 3)
                pygame.draw.circle(screen, WHITE, (int(friend['x'] - 4), int(friend['y'] - 2)), 3)
                pygame.draw.circle(screen, WHITE, (int(friend['x'] + 4), int(friend['y'] - 2)), 3)
                pygame.draw.circle(screen, BLACK, (int(friend['x'] - 3), int(friend['y'] - 1)), 2)
                pygame.draw.circle(screen, BLACK, (int(friend['x'] + 5), int(friend['y'] - 1)), 2)
            else:
                if friend['death_timer'] > 0:
                    for _ in range(5):
                        pygame.draw.circle(screen, friend['color'], (int(friend['x'] + random.randint(-15, 15)), int(friend['y'] + random.randint(-15, 15))), random.randint(2, 5))
        if boss_visible:
            pygame.draw.circle(screen, DARK_BLUE, (int(boss_x), int(boss_y)), boss_radius)
            pygame.draw.circle(screen, (80, 80, 200), (int(boss_x - 5), int(boss_y - 5)), boss_radius - 5)
            pygame.draw.circle(screen, RED, (int(boss_x - 18), int(boss_y - 8)), 10)
            pygame.draw.circle(screen, RED, (int(boss_x + 18), int(boss_y - 8)), 10)
            pygame.draw.circle(screen, BLACK, (int(boss_x - 16), int(boss_y - 6)), 5)
            pygame.draw.circle(screen, BLACK, (int(boss_x + 20), int(boss_y - 6)), 5)
            pygame.draw.arc(screen, BLACK, (int(boss_x - 18), int(boss_y + 6), 36, 18), 0.1, 3.0, 3)
            boss_text = big_font.render("БОСС", True, DARK_RED)
            screen.blit(boss_text, (int(boss_x - boss_text.get_width()//2), int(boss_y - 65)))
        pygame.draw.circle(screen, RED, (int(hero_x), int(hero_y)), hero_radius)
        pygame.draw.circle(screen, (255, 80, 80), (int(hero_x - 4), int(hero_y - 5)), hero_radius - 3)
        pygame.draw.circle(screen, (255, 255, 255, 100), (int(hero_x - 6), int(hero_y - 10)), 8)
        pygame.draw.ellipse(screen, WHITE, (int(hero_x - 10), int(hero_y - 10), 12, 14))
        pygame.draw.ellipse(screen, WHITE, (int(hero_x + 4), int(hero_y - 10), 12, 14))
        pygame.draw.circle(screen, BLACK, (int(hero_x - 6), int(hero_y - 4)), 4)
        pygame.draw.circle(screen, BLACK, (int(hero_x + 8), int(hero_y - 4)), 4)
        pygame.draw.circle(screen, WHITE, (int(hero_x - 8), int(hero_y - 6)), 2)
        pygame.draw.circle(screen, WHITE, (int(hero_x + 6), int(hero_y - 6)), 2)
        pygame.draw.arc(screen, BLACK, (int(hero_x - 10), int(hero_y + 2), 20, 12), 0.1, 3.0, 2)
        if dialogue_index < len(dialogues) and frame > 160:
            dialogue_y = HEIGHT - 170
            panel = pygame.Surface((WIDTH - 60, 140), pygame.SRCALPHA)
            panel.fill((0, 0, 0, 210))
            screen.blit(panel, (30, dialogue_y))
            pygame.draw.rect(screen, GOLD, (30, dialogue_y, WIDTH - 60, 140), 3, border_radius=10)
            current = dialogues[dialogue_index]
            speaker_color = RED if "Главный герой" in current["speaker"] else DARK_RED
            speaker_text = font.render(f"{current['speaker']}:", True, speaker_color)
            screen.blit(speaker_text, (50, dialogue_y + 15))
            dialogue_text = font.render(text_display, True, WHITE)
            screen.blit(dialogue_text, (50, dialogue_y + 60))
        if len(dialogues) > 0:
            progress = (dialogue_index + (1 if dialogue_stage == 1 else 0)) / len(dialogues)
            pygame.draw.rect(screen, (40, 40, 40), (WIDTH//2 - 150, HEIGHT - 15, 300, 6), border_radius=3)
            pygame.draw.rect(screen, GOLD, (WIDTH//2 - 150, HEIGHT - 15, int(300 * progress), 6), border_radius=3)
        skip_text = small_font.render("[ПРОБЕЛ] - пропустить", True, LIGHT_GRAY)
        screen.blit(skip_text, (WIDTH - 180, HEIGHT - 25))
        if dialogue_index >= len(dialogues):
            end_text = big_font.render("Нажми ПРОБЕЛ", True, GREEN)
            screen.blit(end_text, (WIDTH//2 - end_text.get_width()//2, HEIGHT//2 + 80))
            if frame > 300:
                cutscene_running = False
        pygame.display.update()
        clock.tick(60)
    cutscene_played = True
    save_progress()
    menu_state = "playing"
    reset_level()

# =============================================
# КЛАССЫ
# =============================================

class Particle:
    def __init__(self, x, y, color, vx, vy, size, life=30):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx
        self.vy = vy
        self.size = size
        self.life = life
        self.max_life = life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.life -= 1
        return self.life > 0

    def draw(self, screen):
        alpha = self.life / self.max_life
        size = int(self.size * alpha)
        if size > 0:
            color = (int(self.color[0] * alpha), int(self.color[1] * alpha), int(self.color[2] * alpha))
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), size)

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, target_x, target_y, world_w, world_h):
        self.x += (target_x - self.x - WIDTH // 2) * 0.08
        self.y += (target_y - self.y - HEIGHT // 2) * 0.08
        self.x = max(0, min(self.x, world_w - WIDTH))
        self.y = max(0, min(self.y, world_h - HEIGHT))

# === БОНУСЫ ===
class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.type = power_type
        self.radius = 14
        self.anim = 0
        self.collected = False
        colors = {
            'speed': (255, 255, 0),
            'shield': (100, 200, 255),
            'magnet': (255, 100, 255),
        }
        self.color = colors.get(power_type, YELLOW)

    def update(self):
        self.anim += 0.08

    def draw(self, screen, ox, oy):
        if self.collected:
            return
        x, y = int(self.x - ox), int(self.y + math.sin(self.anim) * 4 - oy)
        r = self.radius
        glow = pygame.Surface((r*2+14, r*2+14), pygame.SRCALPHA)
        for i in range(3, 0, -1):
            pygame.draw.circle(glow, (*self.color, 50), (r+7, r+7), r + i*3)
        screen.blit(glow, (x - r - 7, y - r - 7))
        pygame.draw.circle(screen, self.color, (x, y), r)
        pygame.draw.circle(screen, WHITE, (x, y), r, 2)
        letters = {'speed': 'S', 'shield': 'D', 'magnet': 'M'}
        text = small_font.render(letters.get(self.type, '?'), True, BLACK)
        screen.blit(text, (x - text.get_width()//2, y - text.get_height()//2))

    def get_rect(self):
        if self.collected:
            return pygame.Rect(0, 0, 0, 0)
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = 18
        self.on_ground = False
        self.rotation = 0
        self.squash = 1.0
        self.particles = []
        self.jump_buffer = 0
        self.hp = 100
        self.max_hp = 100
        self.invincible = 0
        self.can_jump = True
        self.can_double_jump = False
        self.trail = []
        self.powerups = {}

    def update(self):
        self.vy += GRAVITY
        if self.vy > MAX_FALL_SPEED:
            self.vy = MAX_FALL_SPEED
        self.x += self.vx
        self.y += self.vy
        self.vx *= FRICTION
        if self.invincible > 0:
            self.invincible -= 1
        if abs(self.vx) > 0.5:
            self.rotation += self.vx * 0.06
        else:
            self.rotation *= 0.95
        if self.on_ground:
            self.squash = min(1.0, self.squash + 0.03)
            self.can_jump = True
            self.can_double_jump = False
        else:
            self.squash = max(0.7, self.squash - 0.03)
        if self.jump_buffer > 0:
            self.jump_buffer -= 1
        if self.hp < 0:
            self.hp = 0
        if self.hp > self.max_hp:
            self.hp = self.max_hp

        # След за игроком
        if abs(self.vx) > 1 or abs(self.vy) > 1:
            self.trail.append({'x': self.x, 'y': self.y, 'life': 15, 'max_life': 15})
        for t in self.trail[:]:
            t['life'] -= 1
            if t['life'] <= 0:
                self.trail.remove(t)

        # Бонусы
        for key in list(self.powerups.keys()):
            self.powerups[key] -= 1
            if self.powerups[key] <= 0:
                del self.powerups[key]

    def jump(self):
        if self.on_ground and self.can_jump:
            self.vy = JUMP_POWER
            self.on_ground = False
            self.can_jump = False
            self.can_double_jump = True
            self.squash = 0.7
            play_sound(SOUND_JUMP)
            for _ in range(15):
                self.particles.append(Particle(
                    self.x, self.y + self.radius,
                    (200, 200, 255),
                    random.uniform(-3, 3), random.uniform(0, 4),
                    random.randint(3, 6), life=25
                ))
            return True
        elif self.can_double_jump and not self.on_ground:
            self.vy = DOUBLE_JUMP_POWER
            self.can_double_jump = False
            play_sound(SOUND_DOUBLE_JUMP)
            for _ in range(25):
                self.particles.append(Particle(
                    self.x, self.y,
                    (255, 255, 100),
                    random.uniform(-5, 5), random.uniform(-2, 3),
                    random.randint(4, 8), life=30
                ))
            return True
        return False

    def take_damage(self, damage):
        if self.invincible > 0:
            return False
        if 'shield' in self.powerups:
            for _ in range(20):
                self.particles.append(Particle(
                    self.x, self.y, CYAN,
                    random.uniform(-5, 5), random.uniform(-5, 5),
                    random.randint(3, 6), life=20
                ))
            return False
        self.hp -= damage
        self.invincible = 30
        play_sound(SOUND_HIT)
        damage_numbers.append(DamageNumber(self.x, self.y, f"-{damage}", RED))
        if self.hp < 0:
            self.hp = 0
        for _ in range(20):
            self.particles.append(Particle(
                self.x, self.y,
                RED,
                random.uniform(-5, 5), random.uniform(-5, 5),
                random.randint(3, 7), life=25
            ))
        return self.hp <= 0

    def heal(self, amount):
        old = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        healed = int(self.hp - old)
        if healed > 0:
            damage_numbers.append(DamageNumber(self.x, self.y, f"+{healed}", GREEN))
        for _ in range(15):
            self.particles.append(Particle(
                self.x, self.y,
                (100, 255, 100),
                random.uniform(-4, 4), random.uniform(-4, 4),
                random.randint(3, 6), life=20
            ))

    def draw(self, screen, ox, oy):
        # След
        for t in self.trail:
            alpha = t['life'] / t['max_life'] * 0.4
            size = int(self.radius * alpha)
            if size > 0:
                s = pygame.Surface((size * 2 + 4, size * 2 + 4), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 100, 100, int(alpha * 100)), (size + 2, size + 2), size)
                screen.blit(s, (int(t['x'] - ox - size - 2), int(t['y'] - oy - size - 2)))

        if self.invincible > 0 and self.invincible % 6 < 3:
            pass
        if abs(self.vx) > 0.5:
            for i in range(4):
                alpha = 0.3 - i * 0.07
                if alpha > 0:
                    pygame.draw.circle(screen, (255, 80, 80, int(alpha * 80)),
                                     (int(self.x - ox - self.vx * i * 2.5),
                                      int(self.y - oy + self.vy * i * 0.3)),
                                     max(1, self.radius - i * 3))
        surf = pygame.Surface((self.radius * 2 + 10, self.radius * 2 + 10), pygame.SRCALPHA)
        cx, cy = self.radius + 5, self.radius + 5
        r = self.radius

        # Щит
        if 'shield' in self.powerups:
            shield_alpha = 100 + int(80 * math.sin(pygame.time.get_ticks() / 150))
            pygame.draw.circle(surf, (100, 200, 255, shield_alpha), (cx, cy), r + 6, 3)

        pygame.draw.ellipse(surf, (0, 0, 0, 60), (cx - r + 5, cy + r - 2, r * 2 - 10, 10))
        if self.hp < 30:
            glow_alpha = 50 + int(30 * math.sin(pygame.time.get_ticks() / 200))
            pygame.draw.circle(surf, (255, 0, 0, glow_alpha), (cx, cy), r + 5)
        color = RED if self.hp > 30 else (200, 50, 50)
        pygame.draw.circle(surf, color, (cx, cy), r)
        pygame.draw.circle(surf, (min(255, color[0] + 80), min(255, color[1] + 30), min(255, color[2] + 30)),
                          (cx - 4, cy - 5), r - 3)
        pygame.draw.circle(surf, (255, 255, 255, 100), (cx - 6, cy - 10), 8)
        pygame.draw.circle(surf, (255, 255, 255, 50), (cx - 10, cy - 14), 5)
        eye_offset = 3 if self.vx > 0 else -3 if self.vx < 0 else 0
        ex = cx + eye_offset * 0.3
        pygame.draw.ellipse(surf, WHITE, (ex - 10, cy - 10, 12, 14))
        pygame.draw.ellipse(surf, WHITE, (ex + 4, cy - 10, 12, 14))
        pupil_off = 2 if self.vx > 0 else -2 if self.vx < 0 else 0
        pygame.draw.circle(surf, BLACK, (int(ex - 7 + pupil_off), cy - 4), 4)
        pygame.draw.circle(surf, BLACK, (int(ex + 7 + pupil_off), cy - 4), 4)
        pygame.draw.circle(surf, WHITE, (int(ex - 8 + pupil_off), cy - 6), 2)
        pygame.draw.circle(surf, WHITE, (int(ex + 6 + pupil_off), cy - 6), 2)
        if abs(self.vx) > 1:
            pygame.draw.arc(surf, BLACK, (cx - 10, cy + 2, 20, 12), 0.1, 3.0, 2)
        else:
            if self.hp > 50:
                pygame.draw.arc(surf, BLACK, (cx - 10, cy + 1, 20, 14), 0.2, 3.0, 2)
            else:
                pygame.draw.arc(surf, BLACK, (cx - 8, cy + 8, 16, 10), 3.2, 0.0, 2)
        pygame.draw.circle(surf, (255, 100, 100, 60), (cx - 16, cy + 6), 6)
        pygame.draw.circle(surf, (255, 100, 100, 60), (cx + 16, cy + 6), 6)
        rotated = pygame.transform.rotate(surf, self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, (rect.x - ox, rect.y - oy))
        for p in self.particles[:]:
            if not p.update():
                self.particles.remove(p)
            else:
                p.draw(screen)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

# === ВРАГИ (с новыми типами) ===
class Enemy:
    def __init__(self, x, y, move_type="horizontal", enemy_type=None):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.type = move_type
        self.dir = 1
        self.speed = 2
        self.start_x = x
        self.start_y = y
        self.range = 120
        self.alive = True
        self.hit_timer = 0

        # Новые типы врагов
        self.enemy_type = enemy_type or ("tank" if move_type == "tank" else
                                          "ghost" if move_type == "ghost" else
                                          "runner" if move_type == "runner" else "goblin")
        if self.enemy_type == "tank":
            self.hp = 3
            self.speed = 1
            self.color = (150, 50, 150)
        elif self.enemy_type == "ghost":
            self.hp = 1
            self.speed = 1.5
            self.color = (100, 100, 200)
        elif self.enemy_type == "runner":
            self.hp = 1
            self.speed = 4
            self.color = (255, 150, 50)
        else:
            self.hp = 1
            self.speed = 2
            self.color = (200, 50, 50)

    def update(self, player=None):
        if not self.alive:
            return
        if self.hit_timer > 0:
            self.hit_timer -= 1

        if self.enemy_type == "ghost" and player:
            self.x += self.speed * self.dir
            if abs(self.x - self.start_x) > self.range * 2:
                self.dir *= -1
        elif self.enemy_type == "runner" and player:
            dx = player.x - self.x
            self.x += self.speed * (1 if dx > 0 else -1) * 0.5
        else:
            if self.type == "horizontal":
                self.x += self.speed * self.dir
                if abs(self.x - self.start_x) > self.range:
                    self.dir *= -1
            elif self.type == "vertical":
                self.y += self.speed * self.dir
                if abs(self.y - self.start_y) > self.range:
                    self.dir *= -1

    def draw(self, screen, ox, oy):
        if not self.alive:
            return
        x, y = self.x - ox, self.y - oy
        color = self.color
        if self.hit_timer > 0 and self.hit_timer % 4 < 2:
            color = WHITE
        pygame.draw.ellipse(screen, (0, 0, 0, 50), (x - 20, y + 14, 40, 10))
        pygame.draw.rect(screen, color, (x - self.width//2, y - self.height//2, self.width, self.height), border_radius=5)
        light_color = (min(255, color[0] + 60), min(255, color[1] + 60), min(255, color[2] + 60))
        pygame.draw.rect(screen, light_color, (x - self.width//2 + 4, y - self.height//2 + 4, self.width - 8, self.height//2 - 4))
        pygame.draw.rect(screen, WHITE, (x - 11, y - 6, 8, 8))
        pygame.draw.rect(screen, WHITE, (x + 3, y - 6, 8, 8))
        pygame.draw.circle(screen, BLACK, (x - 8, y - 2), 3)
        pygame.draw.circle(screen, BLACK, (x + 6, y - 2), 3)
        pygame.draw.arc(screen, BLACK, (x - 9, y + 2, 18, 10), 0.1, 3.0, 2)
        # HP-точки для танка
        if self.enemy_type == "tank":
            for i in range(self.hp):
                pygame.draw.circle(screen, RED, (x - 8 + i * 8, y - self.height//2 - 10), 3)

    def get_rect(self):
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.anim = 0
        self.collected = False

    def update(self):
        self.anim += 0.06

    def draw(self, screen, ox, oy):
        if self.collected:
            return
        x, y = int(self.x - ox), int(self.y + math.sin(self.anim) * 4 - oy)
        r = self.radius
        glow = pygame.Surface((r*2+12, r*2+12), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 215, 0, 40), (r+6, r+6), r+6)
        screen.blit(glow, (x - r - 6, y - r - 6))
        pygame.draw.circle(screen, (180, 140, 0), (x, y + 2), r)
        pygame.draw.circle(screen, YELLOW, (x, y), r)
        pygame.draw.circle(screen, (255, 240, 150), (x - 3, y - 4), r - 3)
        pygame.draw.circle(screen, (180, 140, 0), (x, y), r, 2)
        points = []
        for i in range(5):
            angle = math.radians(-90 + i * 72)
            px = x + math.cos(angle) * (r - 4)
            py = y + math.sin(angle) * (r - 4)
            points.append((px, py))
        pygame.draw.polygon(screen, (200, 160, 0), points)

    def get_rect(self):
        if self.collected:
            return pygame.Rect(0, 0, 0, 0)
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class HealthPack:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 14
        self.anim = 0
        self.collected = False

    def update(self):
        self.anim += 0.04

    def draw(self, screen, ox, oy):
        if self.collected:
            return
        x, y = int(self.x - ox), int(self.y + math.sin(self.anim) * 4 - oy)
        r = self.radius
        glow = pygame.Surface((r*2+14, r*2+14), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 50, 50, 40), (r+7, r+7), r+7)
        screen.blit(glow, (x - r - 7, y - r - 7))
        pygame.draw.circle(screen, (180, 30, 30), (x, y + 2), r)
        pygame.draw.circle(screen, RED, (x, y), r)
        pygame.draw.circle(screen, (255, 100, 100), (x - 3, y - 3), r - 3)
        cross_w, cross_h = 14, 4
        pygame.draw.rect(screen, WHITE, (x - cross_w//2, y - cross_h//2, cross_w, cross_h))
        pygame.draw.rect(screen, WHITE, (x - cross_h//2, y - cross_w//2, cross_h, cross_w))
        pygame.draw.circle(screen, (255, 255, 255, 60), (x - 4, y - 5), 4)
        heal_text = small_font.render("+25 HP", True, WHITE)
        heal_text.set_alpha(150)
        screen.blit(heal_text, (x - heal_text.get_width()//2, y + r + 10))

    def get_rect(self):
        if self.collected:
            return pygame.Rect(0, 0, 0, 0)
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

# === БОСС с ФАЗАМИ ===
class Boss:
    def __init__(self, x, y, boss_type="fire"):
        self.x = x
        self.y = y
        self.width = 70
        self.height = 70
        self.hp = 40
        self.max_hp = 40
        self.dir = 1
        self.speed = 1.2
        self.start_x = x
        self.range = 150
        self.alive = True
        self.hit_timer = 0
        self.boss_type = boss_type
        self.attack_cooldown = 0
        self.attacks = []
        self.shield_active = False
        self.start_y = y
        self.vy = 0
        self.on_ground = False
        self.phase = 1
        if boss_type == "fire":
            self.color = (255, 100, 0)
            self.particles_color = ORANGE
            self.room_color = (40, 20, 10)
            self.floor_color = LAVA
            self.attack_pattern = "fireball"
            self.boss_name = "🔥 Огненный"
        elif boss_type == "ice":
            self.color = (0, 200, 255)
            self.particles_color = CYAN
            self.room_color = (10, 20, 40)
            self.floor_color = ICE_BLUE
            self.attack_pattern = "iceshard"
            self.boss_name = "❄️ Ледяной"
        elif boss_type == "water":
            self.color = (0, 100, 200)
            self.particles_color = WATER_BLUE
            self.room_color = (0, 20, 40)
            self.floor_color = (0, 80, 160)
            self.attack_pattern = "waterwave"
            self.boss_name = "💧 Водяной"
        elif boss_type == "shadow":
            self.color = (100, 0, 150)
            self.particles_color = PURPLE
            self.room_color = (20, 10, 30)
            self.floor_color = DARK_PURPLE
            self.attack_pattern = "darkwave"
            self.boss_name = "🌑 Теневой"
        else:
            self.color = DARK_BLUE
            self.particles_color = BLUE
            self.room_color = (10, 10, 30)
            self.floor_color = DARK_BLUE
            self.attack_pattern = "normal"
            self.boss_name = "БОСС"

    def update(self):
        if not self.alive:
            return
        if self.hit_timer > 0:
            self.hit_timer -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Фазы
        hp_ratio = self.hp / self.max_hp
        if hp_ratio < 0.3:
            self.phase = 3
            self.speed = 2.5
        elif hp_ratio < 0.6:
            self.phase = 2
            self.speed = 1.8
        else:
            self.phase = 1
            self.speed = 1.2

        self.x += self.speed * self.dir
        if abs(self.x - self.start_x) > self.range:
            self.dir *= -1
        self.y = self.start_y + math.sin(pygame.time.get_ticks() / 500) * 10

        if self.attack_cooldown == 0 and self.alive:
            self.attack_cooldown = max(20, 60 - self.phase * 15)
            count = 3 + self.phase
            for i in range(count):
                angle = random.uniform(-math.pi/2, math.pi/2)
                speed = random.uniform(2, 4) + self.phase * 0.3
                self.attacks.append(BossAttack(
                    self.x, self.y - 20,
                    math.cos(angle) * speed,
                    math.sin(angle) * speed - 2,
                    self.boss_type.replace("fire", "fire").replace("ice", "ice").replace("water", "water").replace("shadow", "shadow"),
                    10 + self.phase * 2
                ))
        for attack in self.attacks[:]:
            if not attack.update():
                self.attacks.remove(attack)

    def take_damage(self, damage):
        if self.hit_timer > 0:
            return False
        if self.shield_active:
            return False
        self.hp -= damage
        self.hit_timer = 8
        if self.hp < 0:
            self.hp = 0
        play_sound(SOUND_BOSS_HIT)
        damage_numbers.append(DamageNumber(self.x, self.y - 30, f"-{damage}", ORANGE))
        return self.hp <= 0

    def draw(self, screen, ox, oy):
        if not self.alive:
            return
        x, y = self.x - ox, self.y - oy
        color = self.color if self.hit_timer == 0 or self.hit_timer % 4 < 2 else WHITE

        # Аура в 3-й фазе
        if self.phase == 3:
            s = pygame.Surface((220, 220), pygame.SRCALPHA)
            for i in range(3):
                pygame.draw.circle(s, (255, 0, 0, 30), (110, 110), 60 + i * 15)
            screen.blit(s, (x - 110, y - 110))

        pygame.draw.ellipse(screen, (0, 0, 0, 60), (x - 40, y + 30, 80, 15))
        if self.shield_active:
            shield_alpha = 100 + int(50 * math.sin(pygame.time.get_ticks() / 200))
            pygame.draw.circle(screen, (0, 200, 255, shield_alpha), (x, y), 50, 5)
        pygame.draw.rect(screen, color, (x - self.width//2, y - self.height//2, self.width, self.height), border_radius=8)
        light_color = (min(255, color[0] + 60), min(255, color[1] + 60), min(255, color[2] + 60))
        pygame.draw.rect(screen, light_color, (x - self.width//2 + 6, y - self.height//2 + 6, self.width - 12, self.height//2 - 6))
        eye_color = RED
        if self.boss_type == "ice":
            eye_color = CYAN
        elif self.boss_type == "water":
            eye_color = WATER_BLUE
        elif self.boss_type == "shadow":
            eye_color = PURPLE
        pygame.draw.circle(screen, eye_color, (x - 18, y - 6), 10)
        pygame.draw.circle(screen, eye_color, (x + 18, y - 6), 10)
        pygame.draw.circle(screen, BLACK, (x - 16, y - 4), 5)
        pygame.draw.circle(screen, BLACK, (x + 20, y - 4), 5)
        pygame.draw.circle(screen, WHITE, (x - 18, y - 8), 2)
        pygame.draw.circle(screen, WHITE, (x + 18, y - 8), 2)
        pygame.draw.arc(screen, BLACK, (x - 18, y + 6, 36, 18), 0.1, 3.0, 3)
        pygame.draw.polygon(screen, WHITE, [(x - 12, y + 14), (x - 7, y + 24), (x - 2, y + 14)])
        pygame.draw.polygon(screen, WHITE, [(x + 12, y + 14), (x + 7, y + 24), (x + 2, y + 14)])
        bar_w = 80
        bar_h = 10
        bar_x = x - bar_w//2
        bar_y = y - self.height//2 - 25
        pygame.draw.rect(screen, HEALTH_BG, (bar_x, bar_y, bar_w, bar_h), border_radius=5)
        hp_ratio = self.hp / self.max_hp
        color_hp = HEALTH_GREEN if hp_ratio > 0.5 else HEALTH_YELLOW if hp_ratio > 0.25 else HEALTH_RED
        pygame.draw.rect(screen, color_hp, (bar_x, bar_y, int(bar_w * hp_ratio), bar_h), border_radius=5)
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=5)
        name_text = small_font.render(f"{self.boss_name} (Фаза {self.phase})", True, WHITE)
        screen.blit(name_text, (x - name_text.get_width()//2, bar_y - 20))
        for attack in self.attacks:
            attack.draw(screen, ox, oy)

    def get_rect(self):
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

class BossAttack:
    def __init__(self, x, y, vx, vy, attack_type, size=10):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.attack_type = attack_type
        self.size = size
        self.life = 60
        self.trail = []

    def update(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05
        self.life -= 1
        return self.life > 0 and 0 < self.x < 3000 and 0 < self.y < 2000

    def draw(self, screen, ox, oy):
        x, y = self.x - ox, self.y - oy
        colors = {
            "fire": ORANGE,
            "ice": CYAN,
            "water": WATER_BLUE,
            "shadow": PURPLE
        }
        color = colors.get(self.attack_type, RED)
        for i, (tx, ty) in enumerate(self.trail):
            alpha = i / len(self.trail) * 0.5
            size = int(self.size * (0.3 + 0.7 * (i / len(self.trail))))
            pygame.draw.circle(screen, (color[0], color[1], color[2], int(alpha * 255)),
                             (int(tx - ox), int(ty - oy)), size)
        glow = pygame.Surface((self.size*4, self.size*4), pygame.SRCALPHA)
        for i in range(3, 0, -1):
            alpha = 100 - i * 25
            pygame.draw.circle(glow, (*color, alpha), (self.size*2, self.size*2), self.size*i)
        screen.blit(glow, (x - self.size*2, y - self.size*2))
        pygame.draw.circle(screen, color, (int(x), int(y)), self.size)
        pygame.draw.circle(screen, (255, 255, 200), (int(x-2), int(y-2)), self.size-2)

    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

# === КЛАСС LEVEL  ===
class Level:
    def __init__(self, number):
        self.number = number
        self.platforms = []
        self.enemies = []
        self.coins = []
        self.health_packs = []
        self.powerups = []
        self.boss = None
        self.exit_x = 0
        self.exit_y = 0
        self.start_x = 50
        self.start_y = 300
        self.world_w = 1200
        self.world_h = 600
        self.is_boss_level = (number == 5 or number == 10 or number == 15 or number == 20)
        self.boss_room_color = None
        self.theme = LEVEL_THEMES.get(number, {})
        self.build()

    def build(self):
        # ============= ГЛАВА 1: ЛЕС (1-4) =============
        if self.number == 1:
            self.world_w = 2400
            self.world_h = 700
            self.platforms = [
                pygame.Rect(0, 580, 2400, 20),
                pygame.Rect(100, 520, 80, 15),
                pygame.Rect(220, 470, 80, 15),
                pygame.Rect(340, 430, 80, 15),
                pygame.Rect(460, 470, 80, 15),
                pygame.Rect(580, 520, 80, 15),
                pygame.Rect(700, 480, 60, 15),
                pygame.Rect(800, 440, 60, 15),
                pygame.Rect(900, 400, 60, 15),
                pygame.Rect(1000, 440, 60, 15),
                pygame.Rect(1100, 480, 60, 15),
                pygame.Rect(1200, 480, 120, 15),
                pygame.Rect(1220, 430, 80, 15),
                pygame.Rect(1240, 380, 40, 15),
                pygame.Rect(1350, 520, 80, 15),
                pygame.Rect(1470, 470, 80, 15),
                pygame.Rect(1590, 520, 80, 15),
                pygame.Rect(1700, 480, 100, 15),
                pygame.Rect(1850, 520, 100, 15),
                pygame.Rect(2000, 480, 100, 15),
                pygame.Rect(2150, 520, 100, 15),
            ]
            self.enemies = [
                Enemy(150, 500, "horizontal"),
                Enemy(300, 450, "horizontal"),
                Enemy(500, 500, "horizontal"),
                Enemy(750, 460, "horizontal"),
                Enemy(950, 420, "horizontal"),
                Enemy(1250, 460, "horizontal"),
                Enemy(1500, 450, "horizontal"),
                Enemy(1750, 460, "horizontal"),
                Enemy(1900, 500, "horizontal"),
                Enemy(2050, 460, "horizontal"),
            ]
            self.coins = []
            for x in range(150, 2300, 200):
                if x not in [750, 1250, 1750]:
                    self.coins.append(Coin(x, 560))
            self.coins.append(Coin(1260, 360))
            self.coins.append(Coin(1280, 360))
            self.health_packs = [
                HealthPack(500, 450),
                HealthPack(1200, 360),
                HealthPack(1900, 450),
            ]
            self.powerups = [PowerUp(800, 400, 'speed'), PowerUp(1800, 400, 'shield')]
            self.boss = None
            self.exit_x = 2350
            self.exit_y = 540

        elif self.number == 2:
            self.world_w = 2600
            self.world_h = 750
            self.platforms = [
                pygame.Rect(0, 600, 2600, 20),
                pygame.Rect(80, 540, 70, 15),
                pygame.Rect(200, 490, 70, 15),
                pygame.Rect(320, 440, 70, 15),
                pygame.Rect(440, 490, 70, 15),
                pygame.Rect(560, 540, 70, 15),
                pygame.Rect(680, 500, 50, 15),
                pygame.Rect(770, 450, 50, 15),
                pygame.Rect(860, 400, 50, 15),
                pygame.Rect(950, 450, 50, 15),
                pygame.Rect(1040, 500, 50, 15),
                pygame.Rect(1100, 460, 80, 15),
                pygame.Rect(1220, 420, 80, 15),
                pygame.Rect(1340, 380, 80, 15),
                pygame.Rect(1460, 420, 80, 15),
                pygame.Rect(1580, 460, 80, 15),
                pygame.Rect(1700, 510, 70, 15),
                pygame.Rect(1820, 460, 70, 15),
                pygame.Rect(1940, 510, 70, 15),
                pygame.Rect(2060, 460, 70, 15),
                pygame.Rect(2180, 510, 70, 15),
                pygame.Rect(2300, 460, 70, 15),
            ]
            self.enemies = [
                Enemy(110, 520, "horizontal"),
                Enemy(230, 470, "horizontal"),
                Enemy(350, 420, "horizontal"),
                Enemy(700, 480, "vertical"),
                Enemy(880, 380, "vertical"),
                Enemy(1150, 440, "horizontal"),
                Enemy(1300, 400, "horizontal"),
                Enemy(1500, 440, "horizontal"),
                Enemy(1850, 440, "vertical"),
                Enemy(2100, 490, "horizontal"),
            ]
            self.coins = []
            for x in range(100, 2500, 180):
                if x not in [700, 1150, 1300, 1850]:
                    self.coins.append(Coin(x, 580))
            self.coins.append(Coin(870, 380))
            self.coins.append(Coin(890, 380))
            self.coins.append(Coin(1350, 360))
            self.health_packs = [
                HealthPack(350, 420),
                HealthPack(1300, 360),
                HealthPack(1850, 440),
            ]
            self.powerups = [PowerUp(500, 500, random.choice(['speed', 'shield', 'magnet']))]
            self.boss = None
            self.exit_x = 2550
            self.exit_y = 560

        elif self.number == 3:
            self.world_w = 2800
            self.world_h = 700
            self.platforms = [
                pygame.Rect(0, 600, 2800, 20),
                pygame.Rect(100, 540, 60, 15),
                pygame.Rect(200, 490, 60, 15),
                pygame.Rect(300, 440, 60, 15),
                pygame.Rect(400, 490, 60, 15),
                pygame.Rect(500, 540, 60, 15),
                pygame.Rect(600, 480, 150, 15),
                pygame.Rect(650, 430, 100, 15),
                pygame.Rect(800, 480, 60, 15),
                pygame.Rect(900, 430, 60, 15),
                pygame.Rect(1000, 480, 60, 15),
                pygame.Rect(1100, 530, 60, 15),
                pygame.Rect(1200, 490, 40, 15),
                pygame.Rect(1280, 490, 40, 15),
                pygame.Rect(1360, 490, 40, 15),
                pygame.Rect(1440, 490, 40, 15),
                pygame.Rect(1550, 540, 80, 15),
                pygame.Rect(1680, 490, 80, 15),
                pygame.Rect(1810, 540, 80, 15),
                pygame.Rect(1940, 490, 80, 15),
                pygame.Rect(2070, 540, 80, 15),
                pygame.Rect(2200, 490, 80, 15),
                pygame.Rect(2330, 540, 80, 15),
                pygame.Rect(2460, 490, 80, 15),
            ]
            self.enemies = [
                Enemy(150, 520, "horizontal"),
                Enemy(350, 420, "horizontal"),
                Enemy(650, 460, "vertical"),
                Enemy(850, 460, "vertical"),
                Enemy(1050, 510, "horizontal"),
                Enemy(1300, 470, "horizontal"),
                Enemy(1500, 470, "vertical"),
                Enemy(1700, 470, "horizontal"),
                Enemy(1900, 520, "horizontal"),
                Enemy(2100, 470, "vertical"),
                Enemy(2300, 520, "horizontal"),
            ]
            self.coins = []
            for x in range(120, 2700, 200):
                self.coins.append(Coin(x, 580))
            self.coins.append(Coin(650, 460))
            self.coins.append(Coin(680, 460))
            self.health_packs = [
                HealthPack(650, 410),
                HealthPack(1500, 470),
                HealthPack(2100, 470),
            ]
            self.powerups = [PowerUp(1000, 450, 'speed')]
            self.boss = None
            self.exit_x = 2750
            self.exit_y = 560

        elif self.number == 4:
            self.world_w = 3000
            self.world_h = 700
            self.platforms = [
                pygame.Rect(0, 600, 3000, 20),
                pygame.Rect(80, 540, 70, 15),
                pygame.Rect(200, 480, 70, 15),
                pygame.Rect(320, 420, 70, 15),
                pygame.Rect(440, 360, 70, 15),
                pygame.Rect(560, 480, 120, 15),
                pygame.Rect(590, 420, 80, 15),
                pygame.Rect(720, 480, 70, 15),
                pygame.Rect(840, 420, 70, 15),
                pygame.Rect(960, 360, 70, 15),
                pygame.Rect(1080, 480, 120, 15),
                pygame.Rect(1110, 420, 80, 15),
                pygame.Rect(1250, 480, 70, 15),
                pygame.Rect(1370, 420, 70, 15),
                pygame.Rect(1490, 360, 70, 15),
                pygame.Rect(1610, 480, 40, 15),
                pygame.Rect(1690, 480, 40, 15),
                pygame.Rect(1770, 480, 40, 15),
                pygame.Rect(1850, 480, 40, 15),
                pygame.Rect(1930, 540, 80, 15),
                pygame.Rect(2060, 480, 80, 15),
                pygame.Rect(2190, 420, 80, 15),
                pygame.Rect(2320, 480, 80, 15),
                pygame.Rect(2450, 540, 80, 15),
                pygame.Rect(2580, 480, 80, 15),
                pygame.Rect(2710, 540, 80, 15),
            ]
            self.enemies = [
                Enemy(130, 520, "horizontal"),
                Enemy(250, 460, "horizontal"),
                Enemy(370, 400, "horizontal"),
                Enemy(600, 460, "vertical"),
                Enemy(770, 460, "vertical"),
                Enemy(900, 400, "horizontal"),
                Enemy(1100, 460, "vertical"),
                Enemy(1500, 400, "horizontal"),
                Enemy(1700, 460, "horizontal"),
                Enemy(1850, 460, "horizontal"),
                Enemy(2100, 460, "vertical"),
                Enemy(2400, 520, "horizontal"),
                Enemy(2600, 460, "horizontal"),
            ]
            self.coins = []
            for x in range(100, 2900, 200):
                if x not in [600, 1100, 1700, 2100]:
                    self.coins.append(Coin(x, 580))
            self.coins.append(Coin(1630, 460))
            self.coins.append(Coin(1710, 460))
            self.coins.append(Coin(1790, 460))
            self.health_packs = [
                HealthPack(450, 340),
                HealthPack(1100, 400),
                HealthPack(2200, 400),
            ]
            self.powerups = [PowerUp(1500, 400, 'shield'), PowerUp(2500, 400, 'speed')]
            self.boss = None
            self.exit_x = 2950
            self.exit_y = 560

        # ============= ГЛАВА 2: ЛЕД (6-9) =============
        elif self.number == 6:
            self.world_w = 2000
            self.world_h = 800
            self.platforms = [
                pygame.Rect(0, 680, 2000, 20),
                pygame.Rect(100, 620, 80, 15),
                pygame.Rect(240, 560, 80, 15),
                pygame.Rect(380, 500, 80, 15),
                pygame.Rect(520, 560, 120, 15),
                pygame.Rect(540, 500, 80, 15),
                pygame.Rect(680, 560, 80, 15),
                pygame.Rect(820, 500, 80, 15),
                pygame.Rect(960, 560, 120, 15),
                pygame.Rect(980, 500, 80, 15),
                pygame.Rect(1120, 620, 80, 15),
                pygame.Rect(1260, 560, 80, 15),
                pygame.Rect(1400, 500, 80, 15),
                pygame.Rect(1540, 560, 80, 15),
                pygame.Rect(1680, 620, 80, 15),
                pygame.Rect(1820, 560, 80, 15),
            ]
            self.enemies = [
                Enemy(150, 600, "horizontal"),
                Enemy(300, 540, "vertical"),
                Enemy(550, 540, "horizontal"),
                Enemy(700, 540, "vertical"),
                Enemy(1000, 540, "horizontal"),
                Enemy(1180, 600, "horizontal"),
                Enemy(1300, 540, "vertical"),
                Enemy(1500, 540, "horizontal"),
                Enemy(1700, 600, "vertical"),
            ]
            self.coins = []
            for x in range(120, 1900, 180):
                self.coins.append(Coin(x, 660))
            self.coins.append(Coin(550, 540))
            self.coins.append(Coin(1000, 540))
            self.health_packs = [
                HealthPack(550, 480),
                HealthPack(1300, 480),
                HealthPack(1700, 540),
            ]
            self.powerups = [PowerUp(800, 500, 'speed')]
            self.boss = None
            self.exit_x = 1950
            self.exit_y = 640

        elif self.number == 7:
            self.world_w = 2200
            self.world_h = 850
            self.platforms = [
                pygame.Rect(0, 720, 2200, 20),
                pygame.Rect(80, 660, 60, 15),
                pygame.Rect(180, 600, 60, 15),
                pygame.Rect(280, 540, 60, 15),
                pygame.Rect(380, 600, 60, 15),
                pygame.Rect(480, 660, 60, 15),
                pygame.Rect(580, 600, 80, 15),
                pygame.Rect(620, 540, 40, 15),
                pygame.Rect(660, 600, 80, 15),
                pygame.Rect(760, 660, 60, 15),
                pygame.Rect(860, 600, 60, 15),
                pygame.Rect(960, 540, 60, 15),
                pygame.Rect(1060, 600, 100, 15),
                pygame.Rect(1100, 540, 60, 15),
                pygame.Rect(1200, 660, 60, 15),
                pygame.Rect(1300, 600, 60, 15),
                pygame.Rect(1400, 540, 60, 15),
                pygame.Rect(1500, 600, 60, 15),
                pygame.Rect(1600, 660, 60, 15),
                pygame.Rect(1700, 600, 100, 15),
                pygame.Rect(1850, 660, 100, 15),
                pygame.Rect(2000, 600, 100, 15),
            ]
            self.enemies = [
                Enemy(120, 640, "horizontal"),
                Enemy(220, 580, "horizontal"),
                Enemy(420, 640, "vertical"),
                Enemy(600, 580, "horizontal"),
                Enemy(800, 640, "horizontal"),
                Enemy(1100, 580, "vertical"),
                Enemy(1350, 580, "horizontal"),
                Enemy(1550, 640, "horizontal"),
                Enemy(1900, 640, "vertical"),
            ]
            self.coins = []
            for x in range(100, 2100, 160):
                self.coins.append(Coin(x, 700))
            self.coins.append(Coin(620, 520))
            self.coins.append(Coin(1100, 520))
            self.health_packs = [
                HealthPack(600, 520),
                HealthPack(1300, 520),
                HealthPack(1900, 580),
            ]
            self.powerups = [PowerUp(1000, 560, 'shield')]
            self.boss = None
            self.exit_x = 2150
            self.exit_y = 680

        elif self.number == 8:
            self.world_w = 2400
            self.world_h = 800
            self.platforms = [
                pygame.Rect(0, 700, 2400, 20),
                pygame.Rect(80, 640, 70, 15),
                pygame.Rect(200, 580, 70, 15),
                pygame.Rect(320, 520, 70, 15),
                pygame.Rect(440, 460, 70, 15),
                pygame.Rect(560, 520, 140, 15),
                pygame.Rect(580, 460, 100, 15),
                pygame.Rect(740, 520, 70, 15),
                pygame.Rect(860, 460, 70, 15),
                pygame.Rect(980, 520, 70, 15),
                pygame.Rect(1100, 460, 140, 15),
                pygame.Rect(1120, 400, 100, 15),
                pygame.Rect(1300, 460, 70, 15),
                pygame.Rect(1420, 520, 70, 15),
                pygame.Rect(1540, 460, 70, 15),
                pygame.Rect(1660, 520, 70, 15),
                pygame.Rect(1780, 580, 70, 15),
                pygame.Rect(1900, 640, 70, 15),
                pygame.Rect(2020, 580, 70, 15),
                pygame.Rect(2140, 640, 70, 15),
                pygame.Rect(2260, 580, 70, 15),
            ]
            self.enemies = [
                Enemy(130, 620, "horizontal"),
                Enemy(250, 560, "vertical"),
                Enemy(370, 500, "horizontal"),
                Enemy(600, 500, "vertical"),
                Enemy(800, 500, "horizontal"),
                Enemy(1150, 440, "vertical"),
                Enemy(1350, 500, "horizontal"),
                Enemy(1500, 500, "vertical"),
                Enemy(1700, 560, "horizontal"),
                Enemy(1850, 620, "horizontal"),
                Enemy(2100, 620, "vertical"),
            ]
            self.coins = []
            for x in range(100, 2300, 180):
                self.coins.append(Coin(x, 680))
            self.coins.append(Coin(590, 440))
            self.coins.append(Coin(1130, 380))
            self.health_packs = [
                HealthPack(580, 440),
                HealthPack(1120, 380),
                HealthPack(2000, 620),
            ]
            self.powerups = [PowerUp(1500, 460, 'speed')]
            self.boss = None
            self.exit_x = 2350
            self.exit_y = 660

        elif self.number == 9:
            self.world_w = 2600
            self.world_h = 900
            self.platforms = [
                pygame.Rect(0, 780, 2600, 20),
                pygame.Rect(80, 720, 70, 15),
                pygame.Rect(200, 660, 70, 15),
                pygame.Rect(320, 600, 70, 15),
                pygame.Rect(440, 660, 120, 15),
                pygame.Rect(460, 600, 80, 15),
                pygame.Rect(600, 660, 70, 15),
                pygame.Rect(720, 600, 70, 15),
                pygame.Rect(840, 660, 120, 15),
                pygame.Rect(860, 600, 80, 15),
                pygame.Rect(1000, 660, 70, 15),
                pygame.Rect(1120, 600, 70, 15),
                pygame.Rect(1240, 540, 70, 15),
                pygame.Rect(1360, 600, 120, 15),
                pygame.Rect(1380, 540, 80, 15),
                pygame.Rect(1520, 600, 70, 15),
                pygame.Rect(1640, 660, 70, 15),
                pygame.Rect(1760, 720, 70, 15),
                pygame.Rect(1880, 660, 70, 15),
                pygame.Rect(2000, 720, 70, 15),
                pygame.Rect(2120, 660, 70, 15),
                pygame.Rect(2240, 720, 70, 15),
                pygame.Rect(2360, 660, 70, 15),
            ]
            self.enemies = [
                Enemy(130, 700, "horizontal"),
                Enemy(250, 640, "vertical"),
                Enemy(470, 640, "horizontal"),
                Enemy(650, 640, "vertical"),
                Enemy(870, 640, "horizontal"),
                Enemy(1150, 580, "horizontal"),
                Enemy(1400, 580, "vertical"),
                Enemy(1650, 640, "horizontal"),
                Enemy(1800, 700, "horizontal"),
                Enemy(2000, 700, "vertical"),
                Enemy(2150, 640, "horizontal"),
                Enemy(2300, 700, "horizontal"),
            ]
            self.coins = []
            for x in range(100, 2500, 160):
                self.coins.append(Coin(x, 760))
            self.coins.append(Coin(470, 580))
            self.coins.append(Coin(870, 580))
            self.coins.append(Coin(1390, 520))
            self.health_packs = [
                HealthPack(470, 580),
                HealthPack(870, 580),
                HealthPack(1750, 640),
            ]
            self.powerups = [PowerUp(1200, 550, 'shield')]
            self.boss = None
            self.exit_x = 2550
            self.exit_y = 760

        # ============= ГЛАВА 3: ВУЛКАН (11-14) =============
        elif self.number == 11:
            self.world_w = 2200
            self.world_h = 700
            self.platforms = [
                pygame.Rect(0, 600, 2200, 20),
                pygame.Rect(100, 540, 80, 15),
                pygame.Rect(240, 480, 80, 15),
                pygame.Rect(380, 420, 80, 15),
                pygame.Rect(520, 480, 40, 15),
                pygame.Rect(600, 480, 40, 15),
                pygame.Rect(680, 480, 40, 15),
                pygame.Rect(760, 480, 40, 15),
                pygame.Rect(840, 420, 80, 15),
                pygame.Rect(980, 480, 80, 15),
                pygame.Rect(1120, 420, 80, 15),
                pygame.Rect(1260, 480, 80, 15),
                pygame.Rect(1400, 540, 80, 15),
                pygame.Rect(1540, 480, 80, 15),
                pygame.Rect(1680, 540, 80, 15),
                pygame.Rect(1820, 480, 80, 15),
                pygame.Rect(1960, 540, 80, 15),
            ]
            self.enemies = [
                Enemy(150, 520, "horizontal"),
                Enemy(300, 460, "horizontal"),
                Enemy(550, 460, "vertical"),
                Enemy(750, 460, "vertical"),
                Enemy(900, 460, "horizontal"),
                Enemy(1050, 460, "horizontal"),
                Enemy(1300, 460, "vertical"),
                Enemy(1600, 520, "horizontal"),
                Enemy(1850, 460, "horizontal"),
            ]
            self.coins = []
            for x in range(120, 2100, 180):
                if x not in [550, 750, 1300]:
                    self.coins.append(Coin(x, 580))
            self.health_packs = [
                HealthPack(550, 460),
                HealthPack(1300, 460),
                HealthPack(1850, 460),
            ]
            self.powerups = [PowerUp(1000, 440, 'speed')]
            self.boss = None
            self.exit_x = 2150
            self.exit_y = 580

        elif self.number == 12:
            self.world_w = 2400
            self.world_h = 700
            self.platforms = [
                pygame.Rect(0, 600, 2400, 20),
                pygame.Rect(80, 540, 60, 15),
                pygame.Rect(180, 540, 60, 15),
                pygame.Rect(280, 540, 60, 15),
                pygame.Rect(380, 480, 50, 15),
                pygame.Rect(470, 480, 50, 15),
                pygame.Rect(560, 480, 50, 15),
                pygame.Rect(650, 540, 120, 15),
                pygame.Rect(820, 480, 50, 15),
                pygame.Rect(910, 480, 50, 15),
                pygame.Rect(1000, 480, 50, 15),
                pygame.Rect(1090, 540, 120, 15),
                pygame.Rect(1260, 480, 50, 15),
                pygame.Rect(1350, 480, 50, 15),
                pygame.Rect(1440, 480, 50, 15),
                pygame.Rect(1530, 480, 50, 15),
                pygame.Rect(1620, 540, 100, 15),
                pygame.Rect(1770, 480, 100, 15),
                pygame.Rect(1920, 540, 100, 15),
                pygame.Rect(2070, 480, 100, 15),
                pygame.Rect(2220, 540, 100, 15),
            ]
            self.enemies = [
                Enemy(130, 520, "horizontal"),
                Enemy(330, 520, "horizontal"),
                Enemy(400, 460, "vertical"),
                Enemy(500, 460, "vertical"),
                Enemy(700, 520, "vertical"),
                Enemy(850, 460, "vertical"),
                Enemy(950, 460, "vertical"),
                Enemy(1150, 520, "vertical"),
                Enemy(1300, 460, "horizontal"),
                Enemy(1500, 460, "horizontal"),
                Enemy(1800, 460, "vertical"),
                Enemy(2000, 520, "horizontal"),
                Enemy(2150, 460, "horizontal"),
            ]
            self.coins = []
            for x in range(100, 2300, 160):
                if x not in [700, 1150, 1800]:
                    self.coins.append(Coin(x, 580))
            self.health_packs = [
                HealthPack(700, 520),
                HealthPack(1150, 520),
                HealthPack(1800, 460),
            ]
            self.powerups = [PowerUp(1400, 480, 'shield')]
            self.boss = None
            self.exit_x = 2350
            self.exit_y = 580

        elif self.number == 13:
            self.world_w = 2600
            self.world_h = 750
            self.platforms = [
                pygame.Rect(0, 640, 2600, 20),
                pygame.Rect(80, 580, 70, 15),
                pygame.Rect(200, 520, 70, 15),
                pygame.Rect(320, 460, 70, 15),
                pygame.Rect(440, 520, 120, 15),
                pygame.Rect(460, 460, 80, 15),
                pygame.Rect(600, 520, 70, 15),
                pygame.Rect(720, 460, 70, 15),
                pygame.Rect(840, 520, 120, 15),
                pygame.Rect(860, 460, 80, 15),
                pygame.Rect(1000, 520, 70, 15),
                pygame.Rect(1120, 460, 70, 15),
                pygame.Rect(1240, 520, 70, 15),
                pygame.Rect(1360, 580, 100, 15),
                pygame.Rect(1500, 520, 100, 15),
                pygame.Rect(1640, 580, 100, 15),
                pygame.Rect(1780, 520, 100, 15),
                pygame.Rect(1920, 580, 100, 15),
                pygame.Rect(2060, 520, 100, 15),
                pygame.Rect(2200, 580, 100, 15),
                pygame.Rect(2340, 520, 100, 15),
            ]
            self.enemies = [
                Enemy(130, 560, "horizontal"),
                Enemy(250, 500, "vertical"),
                Enemy(470, 500, "horizontal"),
                Enemy(650, 500, "vertical"),
                Enemy(870, 500, "horizontal"),
                Enemy(1150, 500, "horizontal"),
                Enemy(1400, 560, "vertical"),
                Enemy(1600, 560, "horizontal"),
                Enemy(1800, 500, "vertical"),
                Enemy(2000, 560, "horizontal"),
                Enemy(2150, 500, "horizontal"),
                Enemy(2300, 560, "vertical"),
            ]
            self.coins = []
            for x in range(100, 2500, 180):
                self.coins.append(Coin(x, 620))
            self.coins.append(Coin(470, 440))
            self.coins.append(Coin(870, 440))
            self.health_packs = [
                HealthPack(470, 440),
                HealthPack(870, 440),
                HealthPack(1800, 500),
            ]
            self.powerups = [PowerUp(1500, 500, 'speed')]
            self.boss = None
            self.exit_x = 2550
            self.exit_y = 620

        elif self.number == 14:
            self.world_w = 2800
            self.world_h = 700
            self.platforms = [
                pygame.Rect(0, 600, 2800, 20),
                pygame.Rect(80, 540, 70, 15),
                pygame.Rect(200, 480, 70, 15),
                pygame.Rect(320, 420, 70, 15),
                pygame.Rect(440, 480, 70, 15),
                pygame.Rect(560, 540, 70, 15),
                pygame.Rect(680, 480, 80, 15),
                pygame.Rect(800, 540, 70, 15),
                pygame.Rect(920, 480, 70, 15),
                pygame.Rect(1040, 420, 70, 15),
                pygame.Rect(1160, 480, 70, 15),
                pygame.Rect(1280, 540, 70, 15),
                pygame.Rect(1400, 480, 80, 15),
                pygame.Rect(1520, 540, 70, 15),
                pygame.Rect(1640, 480, 70, 15),
                pygame.Rect(1760, 420, 70, 15),
                pygame.Rect(1880, 480, 70, 15),
                pygame.Rect(2000, 540, 70, 15),
                pygame.Rect(2120, 480, 120, 15),
                pygame.Rect(2280, 540, 120, 15),
                pygame.Rect(2440, 480, 120, 15),
                pygame.Rect(2600, 540, 120, 15),
            ]
            self.enemies = [
                Enemy(130, 520, "horizontal"),
                Enemy(250, 460, "vertical"),
                Enemy(350, 400, "horizontal"),
                Enemy(500, 520, "horizontal"),
                Enemy(700, 460, "vertical"),
                Enemy(850, 520, "horizontal"),
                Enemy(1000, 400, "vertical"),
                Enemy(1150, 520, "horizontal"),
                Enemy(1300, 520, "horizontal"),
                Enemy(1550, 520, "vertical"),
                Enemy(1700, 460, "horizontal"),
                Enemy(1850, 460, "vertical"),
                Enemy(2000, 520, "horizontal"),
                Enemy(2300, 520, "vertical"),
                Enemy(2500, 460, "horizontal"),
            ]
            self.coins = []
            for x in range(100, 2700, 180):
                if x not in [700, 1400, 2300]:
                    self.coins.append(Coin(x, 580))
            self.health_packs = [
                HealthPack(700, 460),
                HealthPack(1400, 460),
                HealthPack(2300, 460),
            ]
            self.powerups = [PowerUp(1200, 440, 'shield')]
            self.boss = None
            self.exit_x = 2750
            self.exit_y = 580

        # ============= ГЛАВА 4: ЗАМОК (16-19) =============
        elif self.number == 16:
            self.world_w = 2000
            self.world_h = 700
            self.platforms = [
                pygame.Rect(0, 600, 2000, 20),
                pygame.Rect(80, 540, 80, 15),
                pygame.Rect(200, 480, 80, 15),
                pygame.Rect(320, 420, 80, 15),
                pygame.Rect(440, 480, 120, 15),
                pygame.Rect(460, 420, 80, 15),
                pygame.Rect(600, 480, 80, 15),
                pygame.Rect(720, 540, 80, 15),
                pygame.Rect(840, 480, 120, 15),
                pygame.Rect(860, 420, 80, 15),
                pygame.Rect(1000, 540, 80, 15),
                pygame.Rect(1120, 480, 80, 15),
                pygame.Rect(1240, 420, 80, 15),
                pygame.Rect(1360, 480, 80, 15),
                pygame.Rect(1480, 540, 80, 15),
                pygame.Rect(1600, 480, 80, 15),
                pygame.Rect(1720, 540, 80, 15),
                pygame.Rect(1840, 480, 80, 15),
            ]
            self.enemies = [
                Enemy(130, 520, "horizontal"),
                Enemy(250, 460, "horizontal"),
                Enemy(470, 460, "vertical"),
                Enemy(650, 520, "vertical"),
                Enemy(870, 460, "vertical"),
                Enemy(1050, 520, "horizontal"),
                Enemy(1200, 460, "horizontal"),
                Enemy(1400, 520, "vertical"),
                Enemy(1600, 460, "horizontal"),
                Enemy(1800, 520, "horizontal"),
            ]
            self.coins = []
            for x in range(100, 1900, 160):
                if x not in [470, 870, 1400]:
                    self.coins.append(Coin(x, 580))
            self.coins.append(Coin(470, 400))
            self.coins.append(Coin(870, 400))
            self.health_packs = [
                HealthPack(470, 400),
                HealthPack(870, 400),
                HealthPack(1400, 460),
            ]
            self.powerups = [PowerUp(700, 480, 'speed')]
            self.boss = None
            self.exit_x = 1950
            self.exit_y = 560

        elif self.number == 17:
            self.world_w = 2200
            self.world_h = 750
            self.platforms = [
                pygame.Rect(0, 660, 2200, 20),
                pygame.Rect(80, 600, 70, 15),
                pygame.Rect(200, 540, 70, 15),
                pygame.Rect(320, 480, 70, 15),
                pygame.Rect(440, 540, 120, 15),
                pygame.Rect(460, 480, 80, 15),
                pygame.Rect(600, 540, 40, 15),
                pygame.Rect(680, 540, 40, 15),
                pygame.Rect(760, 540, 40, 15),
                pygame.Rect(840, 600, 120, 15),
                pygame.Rect(860, 540, 80, 15),
                pygame.Rect(1000, 600, 70, 15),
                pygame.Rect(1120, 540, 70, 15),
                pygame.Rect(1240, 480, 70, 15),
                pygame.Rect(1360, 540, 40, 15),
                pygame.Rect(1440, 540, 40, 15),
                pygame.Rect(1520, 540, 40, 15),
                pygame.Rect(1600, 540, 40, 15),
                pygame.Rect(1680, 600, 100, 15),
                pygame.Rect(1820, 540, 100, 15),
                pygame.Rect(1960, 600, 100, 15),
            ]
            self.enemies = [
                Enemy(130, 580, "horizontal"),
                Enemy(250, 520, "vertical"),
                Enemy(470, 520, "horizontal"),
                Enemy(620, 520, "vertical"),
                Enemy(700, 520, "vertical"),
                Enemy(870, 580, "horizontal"),
                Enemy(1150, 520, "horizontal"),
                Enemy(1400, 520, "vertical"),
                Enemy(1550, 520, "vertical"),
                Enemy(1850, 520, "horizontal"),
                Enemy(2000, 580, "vertical"),
            ]
            self.coins = []
            for x in range(100, 2100, 180):
                if x not in [620, 870, 1400, 1550]:
                    self.coins.append(Coin(x, 640))
            self.coins.append(Coin(470, 460))
            self.coins.append(Coin(870, 520))
            self.health_packs = [
                HealthPack(470, 460),
                HealthPack(870, 520),
                HealthPack(1850, 520),
            ]
            self.powerups = [PowerUp(1000, 560, 'shield')]
            self.boss = None
            self.exit_x = 2150
            self.exit_y = 640

        elif self.number == 18:
            self.world_w = 2400
            self.world_h = 700
            self.platforms = [
                pygame.Rect(0, 600, 2400, 20),
                pygame.Rect(80, 540, 80, 15),
                pygame.Rect(200, 480, 80, 15),
                pygame.Rect(320, 540, 40, 15),
                pygame.Rect(360, 540, 40, 15),
                pygame.Rect(400, 540, 40, 15),
                pygame.Rect(480, 480, 120, 15),
                pygame.Rect(640, 540, 40, 15),
                pygame.Rect(680, 540, 40, 15),
                pygame.Rect(720, 540, 40, 15),
                pygame.Rect(800, 480, 120, 15),
                pygame.Rect(960, 540, 40, 15),
                pygame.Rect(1000, 540, 40, 15),
                pygame.Rect(1040, 540, 40, 15),
                pygame.Rect(1120, 540, 120, 15),
                pygame.Rect(1280, 480, 80, 15),
                pygame.Rect(1400, 540, 80, 15),
                pygame.Rect(1520, 480, 80, 15),
                pygame.Rect(1640, 540, 80, 15),
                pygame.Rect(1760, 480, 80, 15),
                pygame.Rect(1880, 540, 80, 15),
                pygame.Rect(2000, 480, 80, 15),
                pygame.Rect(2120, 540, 80, 15),
                pygame.Rect(2240, 480, 80, 15),
            ]
            self.enemies = [
                Enemy(130, 520, "horizontal"),
                Enemy(250, 460, "horizontal"),
                Enemy(340, 520, "vertical"),
                Enemy(400, 520, "vertical"),
                Enemy(530, 460, "vertical"),
                Enemy(660, 520, "vertical"),
                Enemy(720, 520, "vertical"),
                Enemy(850, 460, "vertical"),
                Enemy(980, 520, "vertical"),
                Enemy(1170, 520, "horizontal"),
                Enemy(1350, 460, "horizontal"),
                Enemy(1550, 460, "vertical"),
                Enemy(1750, 460, "horizontal"),
                Enemy(1950, 520, "vertical"),
                Enemy(2150, 520, "horizontal"),
            ]
            self.coins = []
            for x in range(100, 2300, 180):
                if x not in [340, 400, 530, 660, 720, 850, 980]:
                    self.coins.append(Coin(x, 580))
            self.coins.append(Coin(530, 460))
            self.coins.append(Coin(850, 460))
            self.coins.append(Coin(1170, 520))
            self.health_packs = [
                HealthPack(530, 460),
                HealthPack(850, 460),
                HealthPack(1750, 460),
            ]
            self.powerups = [PowerUp(1300, 460, 'magnet')]
            self.boss = None
            self.exit_x = 2350
            self.exit_y = 560

        elif self.number == 19:
            self.world_w = 2600
            self.world_h = 800
            self.platforms = [
                pygame.Rect(0, 700, 2600, 20),
                pygame.Rect(80, 640, 70, 15),
                pygame.Rect(200, 580, 70, 15),
                pygame.Rect(320, 520, 70, 15),
                pygame.Rect(440, 460, 70, 15),
                pygame.Rect(560, 520, 140, 15),
                pygame.Rect(580, 460, 100, 15),
                pygame.Rect(740, 520, 70, 15),
                pygame.Rect(860, 460, 70, 15),
                pygame.Rect(980, 520, 70, 15),
                pygame.Rect(1100, 460, 140, 15),
                pygame.Rect(1120, 400, 100, 15),
                pygame.Rect(1300, 460, 70, 15),
                pygame.Rect(1420, 520, 70, 15),
                pygame.Rect(1540, 460, 70, 15),
                pygame.Rect(1660, 520, 140, 15),
                pygame.Rect(1680, 460, 100, 15),
                pygame.Rect(1840, 520, 70, 15),
                pygame.Rect(1960, 580, 70, 15),
                pygame.Rect(2080, 640, 70, 15),
                pygame.Rect(2200, 580, 70, 15),
                pygame.Rect(2320, 640, 70, 15),
                pygame.Rect(2440, 580, 70, 15),
            ]
            self.enemies = [
                Enemy(130, 620, "horizontal"),
                Enemy(250, 560, "vertical"),
                Enemy(370, 500, "horizontal"),
                Enemy(600, 500, "vertical"),
                Enemy(750, 500, "horizontal"),
                Enemy(900, 500, "vertical"),
                Enemy(1130, 440, "horizontal"),
                Enemy(1350, 500, "vertical"),
                Enemy(1580, 500, "horizontal"),
                Enemy(1700, 500, "vertical"),
                Enemy(1900, 560, "horizontal"),
                Enemy(2100, 620, "vertical"),
                Enemy(2250, 620, "horizontal"),
                Enemy(2400, 620, "vertical"),
            ]
            self.coins = []
            for x in range(100, 2500, 180):
                if x not in [600, 1130, 1580, 1700]:
                    self.coins.append(Coin(x, 680))
            self.coins.append(Coin(590, 440))
            self.coins.append(Coin(1130, 380))
            self.coins.append(Coin(1690, 440))
            self.health_packs = [
                HealthPack(590, 440),
                HealthPack(1130, 380),
                HealthPack(1690, 440),
                HealthPack(2100, 620),
            ]
            self.powerups = [PowerUp(1400, 460, 'shield')]
            self.boss = None
            self.exit_x = 2550
            self.exit_y = 680

        # ============= БОСС-РУМЫ (5, 10, 15, 20) =============
        elif self.number == 5:
            self.world_w = 900
            self.world_h = 600
            self.boss_room_color = (40, 20, 10)
            self.platforms = [
                pygame.Rect(0, 550, 900, 20),
                pygame.Rect(120, 480, 100, 15),
                pygame.Rect(320, 420, 100, 15),
                pygame.Rect(520, 480, 100, 15),
                pygame.Rect(720, 420, 100, 15),
            ]
            self.enemies = []
            self.coins = [
                Coin(150, 450), Coin(350, 390), Coin(550, 450),
                Coin(750, 390),
            ]
            self.health_packs = [HealthPack(450, 450), HealthPack(650, 390)]
            self.powerups = [PowerUp(200, 450, 'shield')]
            self.boss = Boss(450, 490, "fire")
            self.exit_x = 850
            self.exit_y = 500

        elif self.number == 10:
            self.world_w = 900
            self.world_h = 600
            self.boss_room_color = (10, 20, 40)
            self.platforms = [
                pygame.Rect(0, 550, 900, 20),
                pygame.Rect(100, 480, 100, 15),
                pygame.Rect(300, 420, 100, 15),
                pygame.Rect(500, 480, 100, 15),
                pygame.Rect(700, 420, 100, 15),
            ]
            self.enemies = []
            self.coins = [
                Coin(130, 450), Coin(330, 390), Coin(530, 450),
                Coin(730, 390),
            ]
            self.health_packs = [HealthPack(430, 450), HealthPack(630, 390), HealthPack(830, 450)]
            self.powerups = [PowerUp(200, 450, 'speed')]
            self.boss = Boss(450, 490, "ice")
            self.boss.hp = 50
            self.boss.max_hp = 50
            self.exit_x = 850
            self.exit_y = 500

        elif self.number == 15:
            self.world_w = 900
            self.world_h = 600
            self.boss_room_color = (0, 20, 40)
            self.platforms = [
                pygame.Rect(0, 550, 900, 20),
                pygame.Rect(100, 480, 100, 15),
                pygame.Rect(300, 420, 100, 15),
                pygame.Rect(500, 480, 100, 15),
                pygame.Rect(700, 420, 100, 15),
            ]
            self.enemies = []
            self.coins = [
                Coin(130, 450), Coin(330, 390), Coin(530, 450),
                Coin(730, 390),
            ]
            self.health_packs = [HealthPack(430, 450), HealthPack(630, 390), HealthPack(830, 450)]
            self.powerups = [PowerUp(200, 450, 'shield')]
            self.boss = Boss(450, 490, "water")
            self.boss.hp = 45
            self.boss.max_hp = 45
            self.exit_x = 850
            self.exit_y = 500

        elif self.number == 20:
            self.world_w = 900
            self.world_h = 600
            self.boss_room_color = (20, 10, 30)
            self.platforms = [
                pygame.Rect(0, 550, 900, 20),
                pygame.Rect(100, 480, 100, 15),
                pygame.Rect(300, 420, 100, 15),
                pygame.Rect(500, 480, 100, 15),
                pygame.Rect(700, 420, 100, 15),
            ]
            self.enemies = []
            self.coins = [
                Coin(130, 450), Coin(330, 390), Coin(530, 450),
                Coin(730, 390),
            ]
            self.health_packs = [HealthPack(430, 450), HealthPack(630, 390), HealthPack(830, 450)]
            self.powerups = [PowerUp(200, 450, 'shield'), PowerUp(700, 450, 'speed')]
            self.boss = Boss(450, 490, "shadow")
            self.boss.hp = 60
            self.boss.max_hp = 60
            self.exit_x = 850
            self.exit_y = 500

# =============================================
# ФУНКЦИИ ОТРИСОВКИ 
# =============================================

def draw_background(ox, oy, level=None):
    theme = LEVEL_THEMES.get(level.number, {})
    bg_color = theme.get("bg", SKY_BLUE)

    if level and level.is_boss_level and level.boss_room_color:
        screen.fill(level.boss_room_color)
        if level.boss and level.boss.boss_type == "fire":
            for i in range(HEIGHT - 50, HEIGHT):
                r = 200 + int(55 * math.sin(pygame.time.get_ticks() / 1000 + i * 0.1))
                g = 80 + int(30 * math.sin(pygame.time.get_ticks() / 1500 + i * 0.05))
                b = 0
                pygame.draw.line(screen, (r, g, b), (0, i), (WIDTH, i))
            boss_text = big_font.render("🔥 ОГНЕННЫЙ БОСС", True, ORANGE)
            screen.blit(boss_text, (WIDTH//2 - boss_text.get_width()//2, 20))
        elif level.boss and level.boss.boss_type == "ice":
            for i in range(HEIGHT - 50, HEIGHT):
                alpha = 50 + int(30 * math.sin(pygame.time.get_ticks() / 2000 + i * 0.05))
                pygame.draw.line(screen, (150, 220, 255, alpha), (0, i), (WIDTH, i))
            boss_text = big_font.render("❄️ ЛЕДЯНОЙ БОСС", True, CYAN)
            screen.blit(boss_text, (WIDTH//2 - boss_text.get_width()//2, 20))
        elif level.boss and level.boss.boss_type == "water":
            for i in range(HEIGHT - 50, HEIGHT):
                alpha = 50 + int(30 * math.sin(pygame.time.get_ticks() / 2000 + i * 0.05))
                pygame.draw.line(screen, (0, 100, 200, alpha), (0, i), (WIDTH, i))
            boss_text = big_font.render("💧 ВОДЯНОЙ БОСС", True, WATER_BLUE)
            screen.blit(boss_text, (WIDTH//2 - boss_text.get_width()//2, 20))
        elif level.boss and level.boss.boss_type == "shadow":
            for i in range(HEIGHT - 50, HEIGHT):
                alpha = 50 + int(30 * math.sin(pygame.time.get_ticks() / 2000 + i * 0.05))
                pygame.draw.line(screen, (80, 0, 120, alpha), (0, i), (WIDTH, i))
            boss_text = big_font.render("🌑 ТЕНЕВОЙ БОСС", True, PURPLE)
            screen.blit(boss_text, (WIDTH//2 - boss_text.get_width()//2, 20))
        return

    screen.fill(bg_color)

    if level.number <= 4:
        for i in range(0, 15):
            x = (i * 220 - ox * 0.1) % (WIDTH + 400) - 200
            if 0 < x < WIDTH + 100:
                tree_height = 120 + (i * 7) % 60
                pygame.draw.rect(screen, (101, 67, 33), (x + 30, HEIGHT - 200 - tree_height, 20, tree_height + 100))
                pygame.draw.circle(screen, (0, 120, 0), (x + 40, HEIGHT - 220 - tree_height), 70 + (i * 5) % 30)
                pygame.draw.circle(screen, (0, 100, 0), (x + 20, HEIGHT - 190 - tree_height), 50 + (i * 3) % 20)
                pygame.draw.circle(screen, (0, 80, 0), (x + 60, HEIGHT - 200 - tree_height), 60 + (i * 7) % 25)
        for i in range(30):
            x = (i * 67) % WIDTH
            y = HEIGHT - 10 + math.sin(i * 1.3) * 8
            pygame.draw.circle(screen, (255, 200, 200), (int(x), int(y)), 3)
            pygame.draw.circle(screen, (255, 255, 0), (int(x), int(y)), 1)
    elif level.number <= 9:
        for i in range(0, 20):
            x = (i * 150 - ox * 0.1) % (WIDTH + 300) - 150
            if 0 < x < WIDTH:
                height = 30 + (i * 7) % 40
                points = [(x, 0), (x + 10, height), (x + 20, 0)]
                pygame.draw.polygon(screen, (200, 230, 255, 150), points)
                points = [(x + 3, 0), (x + 10, height - 5), (x + 17, 0)]
                pygame.draw.polygon(screen, (220, 240, 255, 100), points)
        for i in range(0, 15):
            x = (i * 200 - ox * 0.15) % (WIDTH + 400) - 200
            if 0 < x < WIDTH:
                pygame.draw.rect(screen, (200, 230, 255, 80), (x, HEIGHT - 50, 15, 50))
                pygame.draw.rect(screen, (220, 240, 255, 60), (x + 3, HEIGHT - 40, 9, 40))
    elif level.number <= 14:
        for i in range(0, 15):
            x = (i * 200 - ox * 0.1) % (WIDTH + 400) - 200
            if 0 < x < WIDTH:
                height = 30 + (i * 7) % 40
                color_r = 150 + (i * 11) % 50
                pygame.draw.polygon(screen, (color_r, 50, 20), [(x, HEIGHT-50), (x+30, HEIGHT-50-height), (x+60, HEIGHT-50)])
        for i in range(WIDTH):
            height = 8 + 4 * math.sin(i * 0.1)
            r = 200 + int(55 * math.sin(i * 0.08))
            g = 80 + int(30 * math.sin(i * 0.05))
            b = 0
            pygame.draw.line(screen, (r, g, b), (i, HEIGHT - 2 - height), (i, HEIGHT - 2))
    elif level.number <= 19:
        for i in range(0, 12):
            x = (i * 250 - ox * 0.1) % (WIDTH + 500) - 250
            if 0 < x < WIDTH:
                pygame.draw.rect(screen, (60, 40, 80), (x + 20, HEIGHT - 300, 15, 300))
                pygame.draw.rect(screen, (80, 50, 100), (x + 5, HEIGHT - 300, 45, 20))
                pygame.draw.polygon(screen, (100, 60, 120), [(x, HEIGHT-300), (x+25, HEIGHT-340), (x+50, HEIGHT-300)])
                pygame.draw.rect(screen, (80, 50, 100), (x + 5, HEIGHT - 280, 45, 10))
        for i in range(0, 8):
            x = (i * 320 - ox * 0.05) % (WIDTH + 500) - 250
            if 0 < x < WIDTH:
                pygame.draw.circle(screen, (150, 100, 50, 80), (int(x + 25), HEIGHT - 150), 15 + (i * 3) % 10)

def draw_ui(player, coins, total, deaths, level, game_state):
    panel = pygame.Surface((WIDTH, 80), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 180))
    screen.blit(panel, (0, 0))
    pygame.draw.line(screen, (255, 255, 255, 40), (0, 80), (WIDTH, 80), 2)

    hp_x, hp_y = 200, 15
    hp_w, hp_h = 250, 35

    pygame.draw.rect(screen, HEALTH_BG, (hp_x, hp_y, hp_w, hp_h), border_radius=17)

    hp_ratio = player.hp / player.max_hp
    if hp_ratio > 0.5:
        color = HEALTH_GREEN
    elif hp_ratio > 0.25:
        color = HEALTH_YELLOW
    else:
        color = HEALTH_RED

    hp_fill = int(hp_w * hp_ratio)
    if hp_fill > 0:
        for i in range(hp_fill):
            pos = hp_x + i
            progress = i / hp_fill
            r = int(255 * (1 - progress) + 0)
            g = int(0 * (1 - progress) + 255 * (progress))
            b = 0
            pygame.draw.rect(screen, (r, g, b), (pos, hp_y + 3, 2, hp_h - 6))

    pygame.draw.rect(screen, WHITE, (hp_x, hp_y, hp_w, hp_h), 3, border_radius=17)

    hp_text = font.render(f"❤️ {int(player.hp)}/{int(player.max_hp)}", True, WHITE)
    screen.blit(hp_text, (hp_x + hp_w//2 - hp_text.get_width()//2, hp_y + 5))

    coin_text = font.render(f"🪙 {coins}/{total}", True, WHITE)
    screen.blit(coin_text, (15, 12))

    deaths_text = font.render(f"💀 {deaths}", True, WHITE)
    screen.blit(deaths_text, (15, 48))

    level_text = font.render(f"🏆 Уровень {level}", True, WHITE)
    screen.blit(level_text, (WIDTH - 180, 12))

    menu_text = small_font.render("[M] Меню", True, LIGHT_GRAY)
    screen.blit(menu_text, (WIDTH - 100, 48))

    # Таймер и комбо
    elapsed = (pygame.time.get_ticks() - level_start_time) // 1000
    timer_text = small_font.render(f"⏱ {elapsed}с", True, WHITE)
    screen.blit(timer_text, (WIDTH - 80, 85))

    if combo > 1:
        combo_color = GOLD if combo >= 5 else ORANGE
        combo_text = font.render(f"🔥 x{combo}", True, combo_color)
        screen.blit(combo_text, (WIDTH - 100, 110))

    # Активные бонусы
    if player.powerups:
        y_offset = 110
        for power, frames in player.powerups.items():
            icons = {'speed': '⚡ Ускорение', 'shield': '🛡 Щит', 'magnet': '🧲 Магнит'}
            colors = {'speed': YELLOW, 'shield': CYAN, 'magnet': PINK}
            text = small_font.render(f"{icons[power]} {frames // 60 + 1}с", True, colors[power])
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
            y_offset += 25

    theme = LEVEL_THEMES.get(level, {})
    if theme:
        name_text = small_font.render(theme.get("name", ""), True, GOLD)
        screen.blit(name_text, (WIDTH//2 - name_text.get_width()//2, 85))

    draw_achievements()

    if game_state == "dead":
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        screen.blit(s, (0, 0))
        text = big_font.render("💀 ТЫ УМЕР!", True, RED)
        text2 = font.render("Нажми R для рестарта", True, WHITE)
        text3 = small_font.render(f"Смертей: {deaths} | Монет: {coins}", True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 60))
        screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 + 10))
        screen.blit(text3, (WIDTH//2 - text3.get_width()//2, HEIGHT//2 + 50))

    if game_state == "win":
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        screen.blit(s, (0, 0))
        if level == 20:
            text = big_font.render("🎉 ПОБЕДА!", True, GREEN)
            text2 = font.render("Ты прошёл все 20 уровней!", True, WHITE)
            text3 = font.render("Нажми R для начала заново", True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 60))
            screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 + 10))
            screen.blit(text3, (WIDTH//2 - text3.get_width()//2, HEIGHT//2 + 50))
        else:
            text = big_font.render(f"🌟 УРОВЕНЬ {level} ПРОЙДЕН!", True, GREEN)
            text2 = font.render("Нажми R для следующего уровня", True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
            screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 + 20))

# =============================================
# ДОСТИЖЕНИЯ (твои + не трогал)
# =============================================

achievements = {
    "first_step": {"name": "🏅 Первый шаг", "unlocked": False},
    "boss_slayer": {"name": "💪 Убийца боссов", "unlocked": False},
    "collector": {"name": "👑 Коллекционер", "unlocked": False},
    "immortal": {"name": "💀 Бессмертный?", "unlocked": False},
    "master": {"name": "⭐ Мастер", "unlocked": False},
    "combo_master": {"name": "🔥 Комбо-мастер", "unlocked": False},
}

def check_achievements():
    if not achievements["first_step"]["unlocked"] and current_level >= 2:
        achievements["first_step"]["unlocked"] = True
        print("🏆 ДОСТИЖЕНИЕ: Первый шаг")

    if not achievements["boss_slayer"]["unlocked"]:
        boss_kills = 0
        for i in [5, 10, 15, 20]:
            if i in unlocked_levels:
                boss_kills += 1
        if boss_kills >= 2:
            achievements["boss_slayer"]["unlocked"] = True
            print("🏆 ДОСТИЖЕНИЕ: Убийца боссов")

    if not achievements["collector"]["unlocked"] and coins_collected >= 50:
        achievements["collector"]["unlocked"] = True
        print("🏆 ДОСТИЖЕНИЕ: Коллекционер")

    if not achievements["immortal"]["unlocked"] and deaths >= 10:
        achievements["immortal"]["unlocked"] = True
        print("🏆 ДОСТИЖЕНИЕ: Бессмертный?")

    if not achievements["master"]["unlocked"] and max_unlocked >= 20:
        achievements["master"]["unlocked"] = True
        print("🏆 ДОСТИЖЕНИЕ: Мастер")

    if not achievements["combo_master"]["unlocked"] and combo >= 5:
        achievements["combo_master"]["unlocked"] = True
        print("🏆 ДОСТИЖЕНИЕ: Комбо-мастер")

def draw_achievements():
    y = 10
    for ach in achievements.values():
        if ach["unlocked"]:
            text = small_font.render(ach["name"], True, GOLD)
            screen.blit(text, (WIDTH - 200, y))
            y += 22

# =============================================
# МЕНЮ ПАУЗЫ
# =============================================

def draw_pause_menu():
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 180))
    screen.blit(s, (0, 0))

    title = big_font.render("⏸ ПАУЗА", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))

    info = font.render("Нажми ESC чтобы продолжить", True, LIGHT_GRAY)
    screen.blit(info, (WIDTH//2 - info.get_width()//2, 250))

    info2 = font.render("Нажми R чтобы перезапустить", True, LIGHT_GRAY)
    screen.blit(info2, (WIDTH//2 - info2.get_width()//2, 300))

# =============================================
# ПЛАВНОЕ МЕНЮ (твоё — оставил)
# =============================================

menu_alpha = 0
menu_target = 0
menu_transition_speed = 0.05

def draw_menu():
    global menu_alpha, menu_target
    screen.fill((20, 20, 40))

    for i in range(30):
        x = (i * 137 + pygame.time.get_ticks() // 100) % WIDTH
        y = (i * 251 + pygame.time.get_ticks() // 150) % HEIGHT
        size = 1 + (i % 3)
        alpha = 100 + int(50 * math.sin(pygame.time.get_ticks() / 2000 + i))
        pygame.draw.circle(screen, (255, 255, 255, alpha), (x, y), size)

    menu_alpha += (menu_target - menu_alpha) * menu_transition_speed

    title_y = 50 + int(5 * math.sin(pygame.time.get_ticks() / 2000))
    title = huge_font.render("RED BALL", True, RED)
    title_shadow = huge_font.render("RED BALL", True, DARK_RED)
    screen.blit(title_shadow, (WIDTH//2 - title.get_width()//2 + 3, title_y + 3))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, title_y))

    subtitle = big_font.render("ADVENTURE", True, GOLD)
    screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, title_y + 70))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]

    buttons = [
        {"text": "▶ ИГРАТЬ", "y": 220, "action": "play"},
        {"text": "⚙ НАСТРОЙКИ", "y": 320, "action": "settings"},
        {"text": "🚪 ВЫХОД", "y": 420, "action": "exit"}
    ]

    for btn in buttons:
        x = WIDTH//2 - 120
        y = btn["y"]
        w, h = 240, 55

        hover = (mouse_x > x and mouse_x < x + w and mouse_y > y and mouse_y < y + h)

        color = (60, 60, 80) if not hover else (100, 100, 180)
        border_color = GOLD if hover else (80, 80, 80)

        pygame.draw.rect(screen, (0, 0, 0, 100), (x + 4, y + 4, w, h), border_radius=12)
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=12)
        pygame.draw.rect(screen, border_color, (x, y, w, h), 2, border_radius=12)

        if hover:
            glow = pygame.Surface((w + 20, h + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow, (255, 215, 0, 20), (10, 10, w, h), border_radius=12)
            screen.blit(glow, (x - 10, y - 10))

        text = font.render(btn["text"], True, WHITE if not hover else GOLD)
        screen.blit(text, (x + w//2 - text.get_width()//2, y + h//2 - text.get_height()//2))

        if hover and clicked:
            menu_target = 1
            return btn["action"]

    progress_text = small_font.render(f"Пройдено уровней: {max_unlocked - 1}/19", True, GOLD)
    screen.blit(progress_text, (WIDTH//2 - progress_text.get_width()//2, HEIGHT - 40))

    return None

# =============================================
# ВЫБОР УРОВНЕЙ (твоё — оставил)
# =============================================

level_select_scroll = 0
level_select_target = 0

def draw_level_select():
    global level_select_scroll, level_select_target, menu_state, current_level, cutscene_played
    screen.fill((10, 10, 30))

    level_select_scroll += (level_select_target - level_select_scroll) * 0.1

    title = big_font.render("ВЫБОР УРОВНЯ", True, GOLD)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 15))
    progress_text = small_font.render(f"Пройдено: {max_unlocked - 1}/19 | Всего уровней: 20", True, LIGHT_GRAY)
    screen.blit(progress_text, (WIDTH//2 - progress_text.get_width()//2, 65))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]

    cols = 5
    rows = 4
    spacing_x = 120
    spacing_y = 95
    start_x = WIDTH//2 - (cols - 1) * spacing_x // 2
    start_y = 110

    btn_x = WIDTH - 140
    btn_y = HEIGHT//2 + 10
    btn_w, btn_h = 130, 50

    hover_btn = (mouse_x > btn_x and mouse_x < btn_x + btn_w and mouse_y > btn_y and mouse_y < btn_y + btn_h)
    color_btn = (60, 60, 120) if not hover_btn else (100, 100, 200)

    pygame.draw.rect(screen, color_btn, (btn_x, btn_y, btn_w, btn_h), border_radius=10)
    pygame.draw.rect(screen, GOLD if hover_btn else (80, 80, 80), (btn_x, btn_y, btn_w, btn_h), 2, border_radius=10)

    arrow_offset = 3 * math.sin(pygame.time.get_ticks() / 500) if hover_btn else 0
    arrow_text = font.render("→ Глава 2", True, WHITE if not hover_btn else GOLD)
    screen.blit(arrow_text, (btn_x + 10, btn_y + 12 + arrow_offset))

    if hover_btn and clicked:
        menu_state = "chapter2_preview"
        return

    for i in range(20):
        row = i // cols
        col = i % cols
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y

        level_num = i + 1
        is_boss = (level_num == 5 or level_num == 10 or level_num == 15 or level_num == 20)
        is_unlocked = level_num in unlocked_levels
        theme = LEVEL_THEMES.get(level_num, {})

        hover = (mouse_x > x - 35 and mouse_x < x + 35 and mouse_y > y - 28 and mouse_y < y + 28)

        scale = 1.0
        if hover and is_unlocked:
            scale = 1.1 + 0.03 * math.sin(pygame.time.get_ticks() / 200)

        if is_unlocked:
            if is_boss:
                color = (180, 50, 50) if not hover else (220, 80, 80)
            else:
                color = (60, 60, 120) if not hover else (100, 100, 180)
        else:
            color = (40, 40, 40)

        w, h = int(70 * scale), int(56 * scale)
        draw_x = x - w//2
        draw_y = y - h//2

        pygame.draw.rect(screen, color, (draw_x, draw_y, w, h), border_radius=10)
        pygame.draw.rect(screen, GOLD if is_unlocked and hover else (60, 60, 60),
                        (draw_x, draw_y, w, h), 2, border_radius=10)

        if is_boss and is_unlocked:
            text = font.render("👑", True, WHITE)
            screen.blit(text, (x - text.get_width()//2, y - 16))
            text = small_font.render(str(level_num), True, WHITE)
            screen.blit(text, (x - text.get_width()//2, y + 10))
        elif not is_unlocked:
            text = font.render("🔒", True, WHITE)
            screen.blit(text, (x - text.get_width()//2, y - 10))
            text = small_font.render(str(level_num), True, (60, 60, 60))
            screen.blit(text, (x - text.get_width()//2, y + 18))
        else:
            text = font.render(str(level_num), True, WHITE)
            screen.blit(text, (x - text.get_width()//2, y - 5))

        if is_boss and is_unlocked:
            label = small_font.render("БОСС", True, GOLD)
            screen.blit(label, (x - label.get_width()//2, y + 32))
        elif is_unlocked:
            label = small_font.render("✓", True, GREEN)
            screen.blit(label, (x - label.get_width()//2, y + 32))

        if hover and clicked and is_unlocked:
            current_level = level_num
            if current_level == 1 and not cutscene_played:
                play_cutscene()
                reset_level()
                menu_state = "playing"
                return
            else:
                reset_level()
                menu_state = "playing"
                return

    x_back, y_back = 20, HEIGHT - 50
    hover_back = (mouse_x > x_back and mouse_x < x_back + 100 and mouse_y > y_back and mouse_y < y_back + 40)
    color_back = (60, 60, 80) if not hover_back else (100, 100, 150)
    pygame.draw.rect(screen, color_back, (x_back, y_back, 100, 40), border_radius=10)
    pygame.draw.rect(screen, WHITE, (x_back, y_back, 100, 40), 2, border_radius=10)
    back_text = font.render("← НАЗАД", True, WHITE)
    screen.blit(back_text, (x_back + 10, y_back + 8))

    if hover_back and clicked:
        menu_state = "main"

def draw_chapter2_preview():
    global menu_state
    screen.fill((10, 10, 30))

    for i in range(30):
        x = (i * 137 + pygame.time.get_ticks() // 100) % WIDTH
        y = (i * 251 + pygame.time.get_ticks() // 150) % HEIGHT
        size = 1 + (i % 3)
        alpha = 100 + int(50 * math.sin(pygame.time.get_ticks() / 2000 + i))
        pygame.draw.circle(screen, (255, 255, 255, alpha), (x, y), size)

    title = big_font.render("ГЛАВА 2", True, GOLD)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))

    soon_text = huge_font.render("СКОРО...", True, WHITE)
    soon_rect = soon_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 10))
    screen.blit(soon_text, soon_rect)

    desc_text = font.render("Новые уровни и боссы уже в разработке!", True, LIGHT_GRAY)
    screen.blit(desc_text, (WIDTH//2 - desc_text.get_width()//2, HEIGHT//2 + 50))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]

    x_back, y_back = WIDTH//2 - 120, HEIGHT//2 + 120
    w_back, h_back = 240, 50

    hover_back = (mouse_x > x_back and mouse_x < x_back + w_back and mouse_y > y_back and mouse_y < y_back + h_back)
    color_back = (60, 60, 80) if not hover_back else (100, 100, 150)

    pygame.draw.rect(screen, color_back, (x_back, y_back, w_back, h_back), border_radius=10)
    pygame.draw.rect(screen, GOLD, (x_back, y_back, w_back, h_back), 2, border_radius=10)

    back_text = font.render("← НАЗАД К ГЛАВЕ 1", True, WHITE if not hover_back else GOLD)
    screen.blit(back_text, (x_back + w_back//2 - back_text.get_width()//2, y_back + 12))

    if hover_back and clicked:
        menu_state = "levels"

def draw_settings():
    global menu_state, fullscreen, screen
    screen.fill((10, 10, 30))

    title = big_font.render("⚙ НАСТРОЙКИ", True, GOLD)
    title_y = 30 + int(3 * math.sin(pygame.time.get_ticks() / 1500))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, title_y))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]

    settings_y = 130
    settings = [
        {"text": f"Полноэкранный режим: {'ВКЛ' if fullscreen else 'ВЫКЛ'}", "y": settings_y, "action": "fullscreen"},
        {"text": "Сбросить прогресс", "y": settings_y + 60, "action": "reset"},
    ]

    for setting in settings:
        x = WIDTH//2 - 200
        y = setting["y"]
        w, h = 400, 50

        hover = (mouse_x > x and mouse_x < x + w and mouse_y > y and mouse_y < y + h)
        color = (60, 60, 80) if not hover else (100, 100, 150)

        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
        pygame.draw.rect(screen, LIGHT_GRAY, (x, y, w, h), 2, border_radius=10)

        text = font.render(setting["text"], True, WHITE if not hover else GOLD)
        screen.blit(text, (x + 20, y + 12))

        if hover and clicked:
            if setting["action"] == "fullscreen":
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
                pygame.display.set_caption("Red Ball Adventure")
            elif setting["action"] == "reset":
                global unlocked_levels, max_unlocked, deaths
                unlocked_levels = [1]
                max_unlocked = 1
                deaths = 0
                save_progress()

    x_back, y_back = WIDTH//2 - 200, settings_y + 180 + 30
    w_back, h_back = 400, 50

    hover_back = (mouse_x > x_back and mouse_x < x_back + w_back and mouse_y > y_back and mouse_y < y_back + h_back)
    color_back = (60, 60, 80) if not hover_back else (100, 100, 150)

    pygame.draw.rect(screen, color_back, (x_back, y_back, w_back, h_back), border_radius=10)
    pygame.draw.rect(screen, LIGHT_GRAY, (x_back, y_back, w_back, h_back), 2, border_radius=10)

    back_text = font.render("← НАЗАД В МЕНЮ", True, WHITE if not hover_back else GOLD)
    screen.blit(back_text, (x_back + w_back//2 - back_text.get_width()//2, y_back + 12))

    if hover_back and clicked:
        menu_state = "main"
        return

# =============================================
# ФУНКЦИИ ДЛЯ ИГРЫ
# =============================================

def reset_level():
    global player, level, coins_collected, total_coins, game_state, particles, level_start_time, combo, combo_timer
    player = Player(level.start_x, level.start_y)
    level = Level(current_level)
    coins_collected = 0
    total_coins = len(level.coins)
    game_state = "playing"
    particles = []
    level_start_time = pygame.time.get_ticks()
    combo = 0
    combo_timer = 0

def unlock_level(level_num):
    global unlocked_levels, max_unlocked
    if level_num not in unlocked_levels:
        unlocked_levels.append(level_num)
        unlocked_levels.sort()
        max_unlocked = max(unlocked_levels)
        save_progress()

# =============================================
# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
# =============================================
current_level = 1
player = Player(50, 300)
level = Level(current_level)
camera = Camera()
coins_collected = 0
total_coins = len(level.coins)
particles = []
game_state = "playing"
menu_state = "main"
cutscene_played = False
paused = False

load_progress()

# =============================================
# ГЛАВНЫЙ ЦИКЛ
# =============================================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_progress()
            running = False

        if event.type == pygame.KEYDOWN:
            if menu_state == "settings":
                if event.key == pygame.K_ESCAPE:
                    menu_state = "main"
                    save_progress()
                continue

            if menu_state == "playing":
                if event.key == pygame.K_ESCAPE:
                    if game_state == "playing":
                        paused = not paused
                    else:
                        save_progress()
                        menu_state = "main"
                if event.key == pygame.K_r:
                    if game_state == "dead":
                        deaths += 1
                        reset_level()
                        save_progress()
                        check_achievements()
                    elif game_state == "win":
                        if current_level == 20:
                            menu_state = "main"
                            current_level = 1
                            deaths = 0
                            reset_level()
                            save_progress()
                            check_achievements()
                        else:
                            next_level = current_level + 1
                            if next_level <= 20:
                                unlock_level(next_level)
                            current_level = next_level
                            reset_level()
                            save_progress()
                            check_achievements()
                    else:
                        reset_level()
                if event.key == pygame.K_SPACE and game_state == "playing" and not paused:
                    if player.jump():
                        total_jumps += 1
                if event.key == pygame.K_m:
                    save_progress()
                    menu_state = "main"

            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
                pygame.display.set_caption("Red Ball Adventure")

    if menu_state == "main":
        result = draw_menu()
        if result == "exit":
            save_progress()
            running = False
        elif result == "play":
            menu_state = "levels"
        elif result == "settings":
            menu_state = "settings"

    elif menu_state == "levels":
        draw_level_select()

    elif menu_state == "chapter2_preview":
        draw_chapter2_preview()

    elif menu_state == "settings":
        draw_settings()

    elif menu_state == "playing":
        if game_state == "playing" and not paused:
            keys = pygame.key.get_pressed()
            speed_mult = 2 if 'speed' in player.powerups else 1
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.vx = -PLAYER_SPEED * speed_mult
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.vx = PLAYER_SPEED * speed_mult

            if keys[pygame.K_SPACE]:
                player.jump_buffer = 8

            player.update()
            camera.update(player.x, player.y, level.world_w, level.world_h)
            ox, oy = camera.x, camera.y

            player.on_ground = False
            player_rect = player.get_rect()

            for plat in level.platforms:
                if player_rect.colliderect(plat):
                    if player.vy > 0 and player_rect.bottom - plat.top < 30:
                        player.y = plat.top - player.radius
                        player.vy = 0
                        player.on_ground = True
                        player.can_jump = True
                        if player.jump_buffer > 0:
                            player.jump()
                    elif player.vy < 0 and player_rect.top - plat.bottom < 30:
                        player.y = plat.bottom + player.radius
                        player.vy = 0
                    elif player.vx > 0 and player_rect.right - plat.left < 30:
                        player.x = plat.left - player.radius
                        player.vx = 0
                    elif player.vx < 0 and player_rect.left - plat.right < 30:
                        player.x = plat.right + player.radius
                        player.vx = 0

            for enemy in level.enemies[:]:
                enemy.update(player)
                if player.get_rect().colliderect(enemy.get_rect()):
                    if player.vy > 0 and player.y < enemy.y and player.vy > 3:
                        enemy.hp -= 2 if 'damage' in player.powerups else 1
                        player.vy = JUMP_POWER * 0.5
                        player.on_ground = False
                        player.can_jump = False

                        if enemy.hp <= 0:
                            enemy.alive = False
                            level.enemies.remove(enemy)
                            total_kills += 1
                            combo += 1
                            combo_timer = 120
                            gold_bonus = random.randint(5, 15) * min(combo, 5)
                            damage_numbers.append(DamageNumber(enemy.x, enemy.y, f"+{gold_bonus}", GOLD))
                            play_sound(SOUND_COIN)

                            for _ in range(25):
                                particles.append(Particle(
                                    enemy.x, enemy.y,
                                    random.choice([ORANGE, RED, YELLOW]),
                                    random.uniform(-6, 6), random.uniform(-6, 0),
                                    random.randint(3, 8), life=30
                                ))
                            player.heal(5)
                            check_achievements()
                        else:
                            damage_numbers.append(DamageNumber(enemy.x, enemy.y, "-1", WHITE))
                    else:
                        if player.take_damage(15):
                            game_state = "dead"
                            deaths += 1
                            play_sound(SOUND_DEATH)
                            save_progress()
                            check_achievements()
                        combo = 0
                        if player.x < enemy.x:
                            player.vx = -5
                        else:
                            player.vx = 5
                        player.vy = -5

            if level.boss and level.boss.alive:
                level.boss.update()
                if player.get_rect().colliderect(level.boss.get_rect()):
                    if player.vy > 0 and player.y < level.boss.y and player.vy > 3:
                        if level.boss.take_damage(3):
                            level.boss.alive = False
                            check_achievements()
                            play_sound(SOUND_WIN)
                            for _ in range(60):
                                particles.append(Particle(
                                    level.boss.x, level.boss.y,
                                    random.choice([GOLD, ORANGE, RED, YELLOW, WHITE]),
                                    random.uniform(-10, 10), random.uniform(-10, 0),
                                    random.randint(5, 12), life=45
                                ))
                            player.heal(50)
                        player.vy = JUMP_POWER * 0.4
                        player.on_ground = False
                        player.can_jump = False
                    else:
                        if player.take_damage(20):
                            game_state = "dead"
                            deaths += 1
                            play_sound(SOUND_DEATH)
                            save_progress()
                            check_achievements()
                        if player.x < level.boss.x:
                            player.vx = -8
                        else:
                            player.vx = 8
                        player.vy = -8

                for attack in level.boss.attacks[:]:
                    if player.get_rect().colliderect(attack.get_rect()):
                        if player.take_damage(10):
                            game_state = "dead"
                            deaths += 1
                            play_sound(SOUND_DEATH)
                            save_progress()
                            check_achievements()
                        if attack in level.boss.attacks:
                            level.boss.attacks.remove(attack)

            for coin in level.coins[:]:
                coin.update()
                if player.get_rect().colliderect(coin.get_rect()):
                    level.coins.remove(coin)
                    coins_collected += 1
                    play_sound(SOUND_COIN)
                    damage_numbers.append(DamageNumber(coin.x, coin.y, "+1", GOLD))
                    check_achievements()
                    for _ in range(15):
                        particles.append(Particle(
                            coin.x, coin.y, GOLD,
                            random.uniform(-4, 4), random.uniform(-4, 4),
                            random.randint(2, 6), life=25
                        ))
                    player.heal(2)

            for hp_pack in level.health_packs[:]:
                hp_pack.update()
                if player.get_rect().colliderect(hp_pack.get_rect()):
                    level.health_packs.remove(hp_pack)
                    player.heal(25)
                    play_sound(SOUND_POWERUP)
                    for _ in range(25):
                        particles.append(Particle(
                            hp_pack.x, hp_pack.y,
                            (100, 255, 100),
                            random.uniform(-5, 5), random.uniform(-5, 5),
                            random.randint(3, 7), life=25
                        ))

            for pu in level.powerups[:]:
                pu.update()
                if player.get_rect().colliderect(pu.get_rect()):
                    level.powerups.remove(pu)
                    player.powerups[pu.type] = 300
                    play_sound(SOUND_POWERUP)
                    damage_numbers.append(DamageNumber(pu.x, pu.y, pu.type.upper(), pu.color))
                    for _ in range(30):
                        particles.append(Particle(
                            pu.x, pu.y, pu.color,
                            random.uniform(-6, 6), random.uniform(-6, 6),
                            random.randint(3, 8), life=30
                        ))

            exit_rect = pygame.Rect(level.exit_x - 25, level.exit_y - 30, 50, 60)
            all_coins = (coins_collected >= total_coins)
            boss_dead = not level.boss or not level.boss.alive

            if all_coins and boss_dead and player.get_rect().colliderect(exit_rect):
                game_state = "win"
                check_achievements()
                play_sound(SOUND_WIN)
                for _ in range(40):
                    particles.append(Particle(
                        level.exit_x, level.exit_y,
                        random.choice([GREEN, GOLD, WHITE]),
                        random.uniform(-6, 6), random.uniform(-6, 0),
                        random.randint(4, 9), life=40
                    ))

            if player.y > HEIGHT + 200:
                if player.take_damage(50):
                    game_state = "dead"
                    deaths += 1
                    play_sound(SOUND_DEATH)
                    save_progress()
                    check_achievements()
                else:
                    player.y = 100
                    player.x = level.start_x
                    player.vy = -5
                    player.vx = 0

            if combo_timer > 0:
                combo_timer -= 1
            else:
                combo = 0

            draw_background(ox, oy, level)

            for plat in level.platforms:
                theme = LEVEL_THEMES.get(level.number, {})
                plat_color = theme.get("platform", BROWN)
                plat_color_dark = (plat_color[0]//2, plat_color[1]//2, plat_color[2]//2)
                pygame.draw.rect(screen, (0, 0, 0, 50), (plat.x - ox + 4, plat.y - oy + 4, plat.w, plat.h))
                pygame.draw.rect(screen, plat_color, (plat.x - ox, plat.y - oy, plat.w, plat.h))
                pygame.draw.rect(screen, plat_color_dark, (plat.x - ox, plat.y - oy, plat.w, 4))
                pygame.draw.rect(screen, (80, 50, 30), (plat.x - ox, plat.y - oy, plat.w, plat.h), 2)

            for enemy in level.enemies:
                enemy.draw(screen, ox, oy)

            if level.boss:
                level.boss.draw(screen, ox, oy)

            for coin in level.coins:
                coin.draw(screen, ox, oy)

            for hp_pack in level.health_packs:
                hp_pack.draw(screen, ox, oy)

            for pu in level.powerups:
                pu.draw(screen, ox, oy)

            all_coins = (coins_collected >= total_coins)
            boss_dead = not level.boss or not level.boss.alive
            can_exit = all_coins and boss_dead

            exit_color = GREEN if can_exit else GRAY
            pygame.draw.rect(screen, exit_color, (level.exit_x - ox - 25, level.exit_y - oy - 30, 50, 60))
            pygame.draw.rect(screen, DARK_GREEN if can_exit else (80, 80, 80),
                            (level.exit_x - ox - 20, level.exit_y - oy - 25, 40, 8))

            if can_exit:
                arrow_y = level.exit_y - oy - 50 + math.sin(pygame.time.get_ticks() / 400) * 10
                arrow_points = [
                    (level.exit_x - ox, arrow_y - 18),
                    (level.exit_x - ox - 12, arrow_y - 6),
                    (level.exit_x - ox + 12, arrow_y - 6)
                ]
                pygame.draw.polygon(screen, GREEN, arrow_points)
                exit_text = font.render("ВЫХОД", True, WHITE)
                screen.blit(exit_text, (level.exit_x - ox - exit_text.get_width()//2,
                                       level.exit_y - oy + 12))

            player.draw(screen, ox, oy)

            for p in particles[:]:
                if not p.update():
                    particles.remove(p)
                else:
                    p.draw(screen)

            for d in damage_numbers[:]:
                if not d.update():
                    damage_numbers.remove(d)
                else:
                    d.draw(screen, ox, oy)

            draw_ui(player, coins_collected, total_coins, deaths, current_level, game_state)

            if level.is_boss_level and level.boss and level.boss.alive:
                boss_info = small_font.render("⚔️ УНИЧТОЖЬ БОССА!", True, GOLD)
                screen.blit(boss_info, (WIDTH//2 - boss_info.get_width()//2, 90))

        else:
            ox, oy = camera.x, camera.y
            draw_background(ox, oy, level)

            for plat in level.platforms:
                theme = LEVEL_THEMES.get(level.number, {})
                plat_color = theme.get("platform", BROWN)
                pygame.draw.rect(screen, plat_color, (plat.x - ox, plat.y - oy, plat.w, plat.h))

            for enemy in level.enemies:
                enemy.draw(screen, ox, oy)

            if level.boss:
                level.boss.draw(screen, ox, oy)

            for coin in level.coins:
                coin.draw(screen, ox, oy)

            for hp_pack in level.health_packs:
                hp_pack.draw(screen, ox, oy)

            for pu in level.powerups:
                pu.draw(screen, ox, oy)

            all_coins = (coins_collected >= total_coins)
            boss_dead = not level.boss or not level.boss.alive
            can_exit = all_coins and boss_dead
            exit_color = GREEN if can_exit else GRAY
            pygame.draw.rect(screen, exit_color, (level.exit_x - ox - 25, level.exit_y - oy - 30, 50, 60))
            pygame.draw.rect(screen, DARK_GREEN if can_exit else (80, 80, 80),
                            (level.exit_x - ox - 20, level.exit_y - oy - 25, 40, 8))

            if can_exit:
                exit_text = font.render("ВЫХОД", True, WHITE)
                screen.blit(exit_text, (level.exit_x - ox - exit_text.get_width()//2,
                                       level.exit_y - oy + 12))

            player.draw(screen, ox, oy)

            for p in particles[:]:
                if not p.update():
                    particles.remove(p)
                else:
                    p.draw(screen)

            for d in damage_numbers[:]:
                if not d.update():
                    damage_numbers.remove(d)
                else:
                    d.draw(screen, ox, oy)

            draw_ui(player, coins_collected, total_coins, deaths, current_level, game_state)

            if paused:
                draw_pause_menu()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()