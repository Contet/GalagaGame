import pygame
import random
from pygame import transform
import sys
import csv
import os

# Инициализация Pygame
pygame.init()

# Путь к файлу базы данных
DB_FILE = "data_base_of_game.csv"

# Инициализация игрока
if len(sys.argv) > 1:
    print("Сработала функция sys и аргументы передались вот они кстати:")
    print(sys.argv[1], sys.argv[2])
    player_usrename = sys.argv[1]
    max_score_player = sys.argv[2]
else:
    player_usrename = "inkognito"
    max_score_player = 0

# Установка окна игры
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Galaga-like Game")

# Включение V-Sync
pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE | pygame.DOUBLEBUF)

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Загрузка изображений
try:
    player_image_orig = pygame.image.load("player.png")
    enemy_image_orig = pygame.image.load("enemy.png")
    fast_enemy_image_orig = pygame.image.load("fast_enemy.png")  # Изображение нового типа врага
    background_gif = pygame.image.load("background.gif")
    bullet_image_orig = pygame.image.load("bullet.png")
    bonus_life_image_orig = pygame.image.load("bonus_life.png")  # Изображение бонуса жизни
    bonus_bullet_image_orig = pygame.image.load("bonus_bullet.png")  # Изображение бонуса для нового типа пуль
    bonus_speed_image_orig = pygame.image.load("bonus_speed.png")
except pygame.error:
    print("Не удалось загрузить изображения")
    pygame.quit()
    exit()

# Масштабирование изображений
player_scale = 1.0
enemy_scale = 1.0
bullet_scale = 0.5
bonus_scale = 0.5
player_image = pygame.transform.scale(player_image_orig, (int(player_image_orig.get_width() * player_scale), int(player_image_orig.get_height() * player_scale)))
enemy_image = pygame.transform.scale(enemy_image_orig, (int(enemy_image_orig.get_width() * enemy_scale), int(enemy_image_orig.get_height() * enemy_scale)))
fast_enemy_image = pygame.transform.scale(fast_enemy_image_orig, (int(fast_enemy_image_orig.get_width() * enemy_scale), int(fast_enemy_image_orig.get_height() * enemy_scale)))
bullet_image = pygame.transform.scale(bullet_image_orig, (int(bullet_image_orig.get_width() * bullet_scale), int(bullet_image_orig.get_height() * bullet_scale)))
bonus_life_image = pygame.transform.scale(bonus_life_image_orig, (int(bonus_life_image_orig.get_width() * bonus_scale), int(bonus_life_image_orig.get_height() * bonus_scale)))
bonus_bullet_image = pygame.transform.scale(bonus_bullet_image_orig, (int(bonus_bullet_image_orig.get_width() * bonus_scale), int(bonus_bullet_image_orig.get_height() * bonus_scale)))
bonus_speed_image = pygame.transform.scale(bonus_speed_image_orig, (int(bonus_speed_image_orig.get_width() * bonus_scale), int(bonus_speed_image_orig.get_height() * bonus_scale)))

# Получение размеров изображений
player_width, player_height = player_image.get_size()
enemy_width, enemy_height = enemy_image.get_size()
fast_enemy_width, fast_enemy_height = fast_enemy_image.get_size()
bullet_width, bullet_height = bullet_image.get_size()
bonus_life_width, bonus_life_height = bonus_life_image.get_size()
bonus_bullet_width, bonus_bullet_height = bonus_bullet_image.get_size()
bonus_speed_width, bonus_speed_height = bonus_speed_image.get_size()

# Масштабирование фонового GIF-изображения
background_gif = transform.scale(background_gif, (screen_width, screen_height))

# Функция для отображения меню
def show_menu():
    menu_font = pygame.font.Font(None, 36)
    menu_text = menu_font.render("Нажмите пробел для начала игры", True, WHITE)
    menu_rect = menu_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(menu_text, menu_rect)
    pygame.display.flip()

# Функция изменения счета
def update_max_score(player_username, score_player):
    try:
        with open(DB_FILE, "r+", newline="") as file:
            fieldnames = ["username", "password", "max_score"]
            reader = csv.DictReader(file)
            rows = list(reader)
            found = False
            for row in rows:
                if row["username"] == player_username and int(row["max_score"]) < score_player:
                    row["max_score"] = str(score_player)
                    found = True
                    break
            if found:
                file.seek(0)
                file.truncate()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            return found
    except:
        return False

# Координаты игрока
player_x = screen_width // 2
player_y = screen_height - player_height - 10

# Списки врагов
enemies = []
fast_enemies = []

# Список пуль
bullets = []

# Список бонусов
bonuses = []

# Таймеры для создания новых врагов и бонусов
enemy_timer = 0
fast_enemy_timer = 0
bonus_timer = 0
enemy_spawn_rate = 60  # Один враг каждые 60 кадров
fast_enemy_spawn_rate = 180  # Один быстрый враг каждые 180 кадров
bonus_spawn_rate = 300  # Один бонус каждые 600 кадров

# Жизни игрока
player_lives = 3

# Изначально очков
score_player = 0

# Уровень игрока
level = 1
level_up_score = 1000  # Количество очков для перехода на следующий уровень

# Флаг для отображения меню
show_menu_flag = True

# Флаг для конца игры
game_over = False

# Флаг для бонуса нового типа пуль
new_bullet_bonus = False
new_bullet_timer = 0

# Скорорсть игрока по умолчанию
player_speed = 2

# Флаг для бонуса speed
bonus_speed = False
bonus_speed_timer = 0

# Главный игровой цикл
running = True
clock = pygame.time.Clock()
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_menu_flag = False
            if event.key == pygame.K_SPACE and not show_menu_flag:
                # Создание новой пули
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y - bullet_height
                bullets.append([bullet_x, bullet_y])
            
            if new_bullet_bonus:
                bullets.append([bullet_x - 40, bullet_y])
                bullets.append([bullet_x + 40, bullet_y])


    if show_menu_flag:
        # Отображение меню
        screen.blit(background_gif, (0, 0))
        show_menu()
    elif game_over:
        # Конец игры
        screen.blit(background_gif, (0, 0))
        game_over_font = pygame.font.Font(None, 48)
        game_over_text = game_over_font.render("Игра окончена", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()
    else:
        # Очистка экрана
        screen.blit(background_gif, (0, 0))

        # Движение игрока
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 5
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += 5

        # Создание новых врагов и бонусов
        enemy_timer += 1
        fast_enemy_timer += 1
        bonus_timer += 1
        if enemy_timer >= enemy_spawn_rate:
            enemy_timer = 0
            enemy_x = random.randint(enemy_width, screen_width - enemy_width)
            enemy_y = -enemy_height
            enemies.append([enemy_x, enemy_y])

        if fast_enemy_timer >= fast_enemy_spawn_rate:
            fast_enemy_timer = 0
            fast_enemy_x = random.randint(fast_enemy_width, screen_width - fast_enemy_width)
            fast_enemy_y = -fast_enemy_height
            fast_enemies.append([fast_enemy_x, fast_enemy_y])

        if bonus_timer >= bonus_spawn_rate:
            bonus_timer = 0
            bonus_type = random.choice(["life", "bullet", "speed"])
            bonus_x = random.randint(bonus_life_width, screen_width - bonus_life_width)
            bonus_y = -bonus_life_height
            bonuses.append({"type": bonus_type, "x": bonus_x, "y": bonus_y})

        # Движение врагов
        for i, enemy in enumerate(enemies):
            enemy_x, enemy_y = enemy
            enemy_y += 2  # Скорость обычных врагов
            enemies[i] = (enemy_x, enemy_y)

            # Проверка столкновения с игроком
            if enemy_y + enemy_height >= player_y and enemy_x >= player_x and enemy_x < player_x + player_width:
                enemies.pop(i)
                player_lives -= 1
                if player_lives <= 0:
                    # Игра окончена
                    update_max_score(player_usrename, score_player)
                    game_over = True

        # Движение быстрых врагов
        for i, fast_enemy in enumerate(fast_enemies):
            fast_enemy_x, fast_enemy_y = fast_enemy
            fast_enemy_y += 4  # Увеличенная скорость для быстрых врагов
            fast_enemies[i] = (fast_enemy_x, fast_enemy_y)

            # Проверка столкновения с игроком
            if fast_enemy_y + fast_enemy_height >= player_y and fast_enemy_x >= player_x and fast_enemy_x < player_x + player_width:
                fast_enemies.pop(i)
                player_lives -= 1
                if player_lives <= 0:
                    # Игра окончена
                    update_max_score(player_usrename, score_player)
                    game_over = True

        # Движение бонусов
        for i, bonus in enumerate(bonuses):
            bonus["y"] += 3  # Скорость падения бонусов
            if bonus["y"] > screen_height:
                bonuses.pop(i)  # Удаление бонусов, вышедших за пределы экрана

            # Проверка столкновения с игроком
            if bonus["y"] + bonus_life_height >= player_y and bonus["x"] >= player_x and bonus["x"] < player_x + player_width:
                if bonus["type"] == "life":
                    player_lives += 1
                elif bonus["type"] == "bullet":
                    new_bullet_bonus = True
                    new_bullet_timer = 300  # Бонус активен 5 секунд (300 кадров)
                elif bonus["type"] == "speed":
                    bonus_speed = True
                    bonus_speed_timer = 600  # Бонус активен 10 секунд (600 кадров)
                bonuses.pop(i)

            
        # Удаление врагов, которые вышли за пределы экрана
        enemies = [enemy for enemy in enemies if enemy[1] <= screen_height]
        fast_enemies = [fast_enemy for fast_enemy in fast_enemies if fast_enemy[1] <= screen_height]

        # Перемещение пуль
        for i, bullet in enumerate(bullets):
            bullet[1] -= 5  # Скорость перемещения пули
            if bullet[1] < -bullet_height:
                bullets.pop(i)  # Удаление пули за пределами экрана

        # Обработка столкновений пуль с врагами
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (
                    bullet[0] >= enemy[0]
                    and bullet[0] <= enemy[0] + enemy_width
                    and bullet[1] >= enemy[1]
                    and bullet[1] <= enemy[1] + enemy_height
                ):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score_player += 100

        # Обработка столкновений пуль с быстрыми врагами
        for bullet in bullets[:]:
            for fast_enemy in fast_enemies[:]:
                if (
                    bullet[0] >= fast_enemy[0]
                    and bullet[0] <= fast_enemy[0] + fast_enemy_width
                    and bullet[1] >= fast_enemy[1]
                    and bullet[1] <= fast_enemy[1] + fast_enemy_height
                ):
                    bullets.remove(bullet)
                    fast_enemies.remove(fast_enemy)
                    score_player += 150

        # Проверка на переход на новый уровень
        if score_player >= level * level_up_score:
            level += 1
            fast_enemy_spawn_rate = max(30, fast_enemy_spawn_rate - 10)  # Увеличение частоты появления быстрых врагов

        # Уменьшение таймера бонуса нового типа пуль
        if new_bullet_bonus:
            new_bullet_timer -= 1
            if new_bullet_timer <= 0:
                new_bullet_bonus = False

        # Уменьшение таймера бонуса speed
        if bonus_speed:
            player_speed = 5
            bonus_speed_timer -= 1
            if  bonus_speed_timer <= 0:
                player_speed = 1
                bonus_speed_timer = False

            # Обработка движения игрока    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed

        # Отображение объектов на экране
        screen.blit(player_image, (player_x, player_y))
        for enemy in enemies:
            screen.blit(enemy_image, enemy)
        for fast_enemy in fast_enemies:
            screen.blit(fast_enemy_image, fast_enemy)
        for bullet in bullets:
            screen.blit(bullet_image, bullet)
        for bonus in bonuses:
            if bonus["type"] == "life":
                screen.blit(bonus_life_image, (bonus["x"], bonus["y"]))
            elif bonus["type"] == "bullet":
                screen.blit(bonus_bullet_image, (bonus["x"], bonus["y"]))
            elif bonus["type"] == "speed":
                screen.blit(bonus_speed_image, (bonus["x"], bonus["y"]))

        # Отображение информации об игроке
        font = pygame.font.Font(None, 36)

        score_text = font.render(f"Игрок: {player_usrename}", True, WHITE)
        screen.blit(score_text, (10, 10))
        lives_text = font.render(f"Жизни: {player_lives}", True, WHITE)
        screen.blit(lives_text, (10, 50))
        level_text = font.render(f"Уровень: {level}", True, WHITE)
        screen.blit(level_text, (10, 90))
        level_text = font.render(f"Рекорд: {max_score_player}", True, WHITE)
        screen.blit(level_text, (10, 130))
        score_text = font.render(f"Счет: {score_player}", True, WHITE)
        screen.blit(score_text, (10, 170))

        # Обновление дисплея
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(60)

# Завершение работы Pygame
pygame.quit()
