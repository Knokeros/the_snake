"""
Реализуем игру змейка, которая растет при поедание яблока,
при столкновение со своим телом игра заканчивается.
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


class GameObject:
    """Базовый класс."""

    def __init__(self, color=None):
        """Устанавливаем стартовую позицию в центре экрана."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = color

    def draw(self):
        """Отрисовка объекта."""
        self.draw_cell(self.position, self.body_color)

    def draw_cell(self, position=None, color=None):
        """Рисуем одну ячейку на поле."""
        position = position or self.position
        color = color or self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблоко."""

    def __init__(self, taked_positions=None, color=APPLE_COLOR):
        """Инициализация яблока с параметрами занятых клеток и цвета."""
        super().__init__(color)
        if taked_positions is None:
            taked_positions = set()
        self.randomize_position(taked_positions)

    def randomize_position(self, taked_positions):
        """Устанавливаем яблоко в случайную точку."""
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in taked_positions:
                self.position = new_position
                break


class Snake(GameObject):
    """Класс змейка."""

    def __init__(self, color=SNAKE_COLOR):
        """Инициализация змейки с параметром цвета."""
        super().__init__(color)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = self.direction

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
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def update_direction(self):
        """Обновляет направление движения."""
        self.direction = self.next_direction

    def draw(self):
        """Метод рисования змейки."""
        for position in self.positions:
            self.draw_cell(position)


def collisions(snake):
    """Обработка столкновений."""
    head_position = snake.get_head_position()
    if head_position in snake.positions[1:]:
        snake.reset()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная программа."""
    # Инициализация PyGame:
    pg.init()
    # Создание объектов
    snake = Snake()
    apple = Apple(set(snake.positions))

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
        collisions(snake)

        # Проверка на съеденное яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(set(snake.positions))

        # Рисуем объекты
        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
