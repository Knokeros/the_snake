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

    def init(self, color=None):
        """Устанавливаем стартовую позицию в центре экрана."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = color

    def draw_cell(self, position=None, color=None):
        """Рисуем одну ячейку на поле."""
        position = position or self.position
        color = color or self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблоко."""

    def init(self, taked_positions, color=APPLE_COLOR):
        """Инициализация яблока с параметрами занятых клеток и цвета."""
        super().init(color)
        self.randomize_position(taked_positions)

    def randomize_position(self, taked_positions):
        """Устанавливаем яблоко в случайную точку."""
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in taked_positions:
                self.position = new_position
                break

    def draw(self):
        """Метод рисования яблока."""
        self.draw_cell()


class Snake(GameObject):
    """Класс змейка."""

    def init(self, color=SNAKE_COLOR):
        """Инициализация змейки с параметром цвета."""
        super().init(color)
        self.position = ((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),)
        self.length = 2
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = self.direction

    def move(self):
        """Метод движения змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        # Добавляем новую голову
        self.position = (new_head,) + self.position

        # Удаление последнего сегмента, если не съела
        if len(self.position) > self.length:
            self.position = self.position[:-1]

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.position[0]

    def reset(self):
        """Метод сброса позиции змейки."""
        self.length = 2
        self.position = ((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),)
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def update_direction(self):
        """Обновляет направление движения."""
        self.direction = self.next_direction

    def draw(self):
        """Метод рисования змейки."""
        for position in self.position[:-1]:
            self.draw_cell(position)
        self.draw_cell(self.position[0])


def collisions(snake):
    """Обработка столкновений."""
    head_position = snake.get_head_position()
    if head_position in snake.position[1:]:
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
    snake.init()
    apple = Apple()
    apple.init(set(snake.position))

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
            apple.randomize_position(set(snake.position))

        # Рисуем объекты
        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
