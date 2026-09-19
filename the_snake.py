from random import choice, randint
import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центральная точка экрана, выровненная по сетке:
SCREEN_CENTER = (
    (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE,
    (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

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

# Настройка игрового окна:
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    0,
    32
)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс для игровых объектов."""

    def __init__(self, body_color=None):
        """Инициализирует положение и цвет игрового объекта."""
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw(self):
        """Подготавливает метод для отрисовки игрового объекта."""
        pass


class Apple(GameObject):
    """Класс яблока, которое появляется на игровом поле."""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализирует яблоко и задаёт его случайную позицию."""
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает для яблока случайную позицию на игровом поле."""
        random_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        random_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (random_x, random_y)

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(
            self.position,
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки, отвечающий за её движение и состояние."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует змейку и задаёт её начальное состояние."""
        super().__init__(body_color=body_color)
        self.reset()

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещает змейку на одну клетку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def draw(self):
        """Отрисовывает все сегменты змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                position,
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(
            self.get_head_position(),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last is not None:
            last_rect = pygame.Rect(
                self.last,
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(
                screen,
                BOARD_BACKGROUND_COLOR,
                last_rect
            )


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш и меняет направление змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_UP
                and game_object.direction != DOWN
            ):
                game_object.next_direction = UP
            elif (
                event.key == pygame.K_DOWN
                and game_object.direction != UP
            ):
                game_object.next_direction = DOWN
            elif (
                event.key == pygame.K_LEFT
                and game_object.direction != RIGHT
            ):
                game_object.next_direction = LEFT
            elif (
                event.key == pygame.K_RIGHT
                and game_object.direction != LEFT
            ):
                game_object.next_direction = RIGHT


def main():
    """Запускает игру и управляет основным игровым циклом."""
    pygame.init()

    snake = Snake()
    apple = Apple()

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position()

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
