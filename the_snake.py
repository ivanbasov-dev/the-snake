from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центральная точка экрана:
SCREEN_CENTER = (
    (GRID_WIDTH // 2) * GRID_SIZE,
    (GRID_HEIGHT // 2) * GRID_SIZE
)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Клавиши изменения направления:
DIRECTION_KEYS = {
    (UP, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_LEFT): LEFT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_UP): UP,
    (RIGHT, pg.K_DOWN): DOWN,
}

# Клавиши изменения скорости:
SPEED_UP_KEYS = (pg.K_EQUALS, pg.K_KP_PLUS)
SPEED_DOWN_KEYS = (pg.K_MINUS, pg.K_KP_MINUS)

# Цвет фона:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20
MIN_SPEED = 10
MAX_SPEED = 30
SPEED_CHANGE = 1

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Родительский класс для игровых объектов."""

    def __init__(self, body_color=None):
        """Инициализирует положение и цвет игрового объекта."""
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw(self):
        """Определяет интерфейс отрисовки."""
        raise NotImplementedError(
            'Метод draw() должен быть переопределён '
            f'в дочернем классе {self.__class__.__name__}.'
        )

    def draw_cell(self, position, color, border_color=None):
        """Отрисовывает одну ячейку игрового поля."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)

        if border_color is not None:
            pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Класс яблока, которое появляется на игровом поле."""

    def __init__(self, occupied_positions=None, body_color=APPLE_COLOR):
        """Инициализирует яблоко и задаёт его случайную позицию."""
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions):
        """Устанавливает для яблока случайную позицию на игровом поле."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        self.draw_cell(self.position, self.body_color, BORDER_COLOR)


class Snake(GameObject):
    """Класс змейки, отвечающий за её движение и состояние."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует змейку и задаёт её начальное состояние."""
        super().__init__(body_color=body_color)
        self.speed = SPEED
        self.reset()
        self.direction = RIGHT

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещает змейку на одну клетку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        # Вычисляем координаты в insert(), чтобы избежать создания
        # лишних переменных и дублирования ссылок на объект в списке.
        self.positions.insert(0, (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        ))

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        if new_direction is not None:
            self.direction = new_direction

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def draw(self):
        """Отрисовывает все сегменты змейки на игровом поле."""
        for position in self.positions[:-1]:
            self.draw_cell(position, self.body_color)

        self.draw_cell(self.get_head_position(), self.body_color)

        if self.last is not None:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)


def set_game_title(speed):
    """Обновляет заголовок окна."""
    pg.display.set_caption(
        f'Змейка | Скорость: {speed} | +/- | ESC — выход'
    )


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш и меняет направление змейки."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False

        if event.type != pg.KEYDOWN:
            continue

        if event.key == pg.K_ESCAPE:
            return False

        if event.key in SPEED_UP_KEYS:
            game_object.speed = min(
                game_object.speed + SPEED_CHANGE,
                MAX_SPEED,
            )
            set_game_title(game_object.speed)
            continue

        if event.key in SPEED_DOWN_KEYS:
            game_object.speed = max(
                game_object.speed - SPEED_CHANGE,
                MIN_SPEED,
            )
            set_game_title(game_object.speed)
            continue

        new_direction = DIRECTION_KEYS.get(
            (game_object.direction, event.key),
            game_object.direction,
        )
        game_object.update_direction(new_direction)

    return True


def main():
    """Запускает игру и управляет основным игровым циклом."""
    pg.init()

    snake = Snake()
    apple = Apple(snake.positions or [])
    set_game_title(snake.speed)

    # Заполняем фон один раз при старте
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        if not handle_keys(snake):
            break

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.draw_cell(apple.position, BOARD_BACKGROUND_COLOR)
            snake.length += 1
            apple.randomize_position(snake.positions or [])
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions or [])

        apple.draw()
        snake.draw()
        pg.display.update()
        clock.tick(snake.speed)

    pg.quit()


if __name__ == '__main__':
    main()
