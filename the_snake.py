"""
Игра змейка.
Змея растет при поедание яблока.
При столкновение со своим телом игра заканчивается.
"""
from random import choice, randint
import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Константы клавиш:
KEY_UP = pg.K_UP
KEY_DOWN = pg.K_DOWN
KEY_LEFT = pg.K_LEFT
KEY_RIGHT = pg.K_RIGHT

# Словарь направлений:
DIRECTION_MAP = {
    (KEY_UP, LEFT): UP,
    (KEY_UP, RIGHT): UP,
    (KEY_DOWN, LEFT): DOWN,
    (KEY_DOWN, RIGHT): DOWN,
    (KEY_LEFT, UP): LEFT,
    (KEY_LEFT, DOWN): LEFT,
    (KEY_RIGHT, UP): RIGHT,
    (KEY_RIGHT, DOWN): RIGHT,
}


class GameObject:
    """Базовый класс."""

    def __init__(self, color=None):
        """Устанавливаем стартовую позицию в центре экрана."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = color

    def draw(self):
        """Отрисовка объектов реализованая в дочерних классах."""

    def draw_cell(self, position=None, color=None):
        """Рисуем одну ячейку на поле."""
        position = position or self.position
        color = color or self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблоко."""

    def __init__(self, taked_positions=(), color=APPLE_COLOR):
        """Инициализация яблока с параметрами занятых клеток и цвета."""
        super().__init__(color)
        self.randomize_position(taked_positions)

    def randomize_position(self, taked_positions=()):
        """Устанавливаем яблоко в случайную точку."""
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in taked_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовка яблока."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс змейка."""

    def __init__(self, color=SNAKE_COLOR):
        """Инициализация змейки с параметром цвета."""
        super().__init__(color)
        self.reset()

    def move(self):
        """Метод движения змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        # Добавляем новую голову
        self.positions.insert(0, new_head)

        # Удаление последнего сегмента, если не съела
        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод сброса позиции змейки."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.next_direction = self.direction

    def update_direction(self):
        """Обновляет направление движения."""
        self.direction = self.next_direction

    def draw(self):
        """Метод рисования змейки."""
        for position in self.positions:
            self.draw_cell(position)


def collisions(snake, apple):
    """Обработка столкновений."""
    head_position = snake.get_head_position()
    if head_position in snake.positions[1:]:
        snake.reset()
        apple.randomize_position(tuple(snake.positions))

    if head_position == apple.position:
        snake.length += 1
        apple.randomize_position(tuple(snake.positions))


def handle_keys(snake):
    """Обработка действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit('Game Over')
        if event.type == pg.KEYDOWN:
            new_direction = DIRECTION_MAP.get(
                (event.key, snake.direction), snake.direction)
            snake.next_direction = new_direction


def main():
    """Основная программа."""
    # Инициализация PyGame:
    pg.init()
    # Создание объектов
    snake = Snake()
    apple = Apple(tuple(snake.positions))

    # Основная логика игры
    while True:
        clock.tick(SPEED)

        # Очистка экрана
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Управление змейкой
        handle_keys(snake)

        # Обновляем направления движения
        snake.update_direction()
        snake.move()

        # Проверка столкновений
        collisions(snake, apple)

        # Рисуем объекты
        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
