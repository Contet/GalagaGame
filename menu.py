import pygame
import subprocess
import csv
import os

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Размеры экрана
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
# IMAGE_FRONT = pygame.image.load("front.png")
# Инициализируем pygame
pygame.init()

# Создаем экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Устанавливаем заголовок окна
pygame.display.set_caption("Menu")

# Создаем шрифт для текста
font = pygame.font.SysFont('Arial', 30)

# Триггеры ошибок и тд
error_log_pass = False
suc_login = False
error_log = False

# Создаем кнопки main меню
buttons_list_main = [
    {"text": "Начать игру", "action": lambda: set_current_page("LOG_REG")},
    {"text": "Настройки", "action": lambda: set_current_page("settings")},
    {"text": "Выход", "action": lambda: pygame.quit()}
]

# Создаем кнопки settings меню
buttons_list_set = [
    {"text": "Увеличить звук", "action": None},
    {"text": "Уменьшить звук", "action": None},
    {"text": "Выход в главное меню", "action": lambda: set_current_page("main")}
]

buttons_list_LOG_REG = [
    {"text": "Войти", "action": lambda: print("Нажато войти")},
    {"text": "Зарегистрироваться", "action": lambda: register_player(username_text, password_text) and print("Нажато reg")},
    {"text": "Выход в главное меню", "action": lambda: set_current_page("main")}
]

# Текущая страница (main или settings)
current_page = "main"

def set_current_page(page):
    global current_page
    current_page = page

# Путь к файлу базы данных
DB_FILE = "data_base_of_game.csv"

# Игрок, вводящий логин и пароль
current_player = None

max_score = ""

# Функция для проверки логина и пароля
def check_login(username, password):
    global current_player
    try:
        with open(DB_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username and row["password"] == password:
                    global max_score
                    max_score = str(row["max_score"])
                    print(max_score)
                    current_player = row
                    return True
    except FileNotFoundError:
        pass
    return False

# Функция для регистрации нового игрока
def register_player(username, password):
    global current_player
    try:
        with open(DB_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    error_reg = "Ошибка. Пользователь с таким именем уже существует"
                    return print(error_reg)
                else:
                    file.close
        with open(DB_FILE, "a", newline="") as file:
            fieldnames = ["username", "password","max_score"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({"username": username, "password": password, "max_score": 0})
        current_player = {"username": username, "password": password}
        return True
    except:
        return False

# Добавляем поле ввода логина и пароля
input_box_username = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT //  1.3 - 50, 200, 50)
input_box_password = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 1.3 , 200, 50)
username_text = ""
password_text = ""
login_password_entered = False

# Основной цикл игры
running = True
while running:

    # Обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обрабатываем нажатие кнопок 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_page == "main":
                for i, button in enumerate(buttons_list_main):
                    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 100 + i * 50, 200, 50)
                    if button_rect.collidepoint(event.pos):
                        button["action"]()
            elif current_page == "settings":
                for i, button in enumerate(buttons_list_set):
                    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 100 + i * 50, 200, 50)
                    if button_rect.collidepoint(event.pos):
                        button["action"]()
            elif current_page == "LOG_REG":
                for i, button in enumerate(buttons_list_LOG_REG):

                    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 100 + i * 50, 200, 50)
                    if button_rect.collidepoint(event.pos):
                        if button["text"] == "Войти" :
                            if check_login(username_text, password_text):
                                print("Must open game")
                                print(max_score)
                                subprocess.Popen(["main.exe", username_text, max_score])
                                running = False
                            else:
                                print("Неверный логин или пароль")
                                error_log_pass = True
                                suc_login = False
                                error_log = False
                        elif button["text"] == "Зарегистрироваться":
                            if register_player(username_text, password_text):
                                print("Регистрация успешна!")
                                error_log_pass = False
                                suc_login = True
                                error_log = False
                            else:
                                print("Ошибка регистрации")
                                error_log_pass = False
                                suc_login = False
                                error_log = True
                        else:
                            button["action"]()

        # Обрабатываем ввод текста
        elif event.type == pygame.KEYDOWN:
            if current_page == "LOG_REG":
                if input_box_username.collidepoint(pygame.mouse.get_pos()):
                    if event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        login_password_entered = True
                    else:
                        username_text += event.unicode
                elif input_box_password.collidepoint(pygame.mouse.get_pos()):
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        login_password_entered = True
                    else:
                        password_text += event.unicode

    # Рендерим фон
    screen.fill(WHITE)

    # Рендерим кнопки в зависимости от текущей страницы
    if current_page == "main":
        for i, button in enumerate(buttons_list_main):
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 100 + i * 50, 200, 50)
            pygame.draw.rect(screen, WHITE, button_rect)

            text = font.render(button["text"], True, BLACK)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)

    elif current_page == "settings":
        for i, button in enumerate(buttons_list_set):
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 100 + i * 50, 200, 50)
            pygame.draw.rect(screen, WHITE, button_rect)

            text = font.render(button["text"], True, BLACK)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)

    elif current_page == "LOG_REG":
        for i, button in enumerate(buttons_list_LOG_REG):
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 100 + i * 50, 200, 50)
            error_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 10 + i * 10, 200, 50)
            pygame.draw.rect(screen, WHITE, button_rect)

            text = font.render(button["text"], True, BLACK)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
        if error_log_pass:
            text_error = font.render("Неверный пароль", True, BLACK)
            text_rect_error = text.get_rect(center=error_rect.center)
            screen.blit(text_error, text_rect_error)
        elif suc_login:
            text_error = font.render("Регистрация успешна!", True, BLACK)
            text_rect_error = text.get_rect(center=error_rect.center)
            screen.blit(text_error, text_rect_error)
        elif error_log:
            text_error = font.render("Ошибка. Уже есть такой пользователь", True, BLACK)
            text_rect_error = text.get_rect(center=error_rect.center)
            screen.blit(text_error, text_rect_error)


        # Рендерим поля ввода логина и пароля
        pygame.draw.rect(screen, BLACK, input_box_username, 2)
        text_surface = font.render(username_text, True, BLACK)
        screen.blit(text_surface, (input_box_username.x + 5, input_box_username.y + 5))

        pygame.draw.rect(screen, BLACK, input_box_password, 2)
        text_surface = font.render("*" * len(password_text), True, BLACK)
        screen.blit(text_surface, (input_box_password.x + 5, input_box_password.y + 5))

        # # Отображаем сообщение о необходимости нажать Enter
        # if not login_password_entered:

        #     text = font.render("Нажмите Enter для входа ", True, BLACK)
        #     text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        #     screen.blit(text, text_rect)

    # Обновляем экран
    pygame.display.update()
