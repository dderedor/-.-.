import pygame
import random

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
FPS = 20

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект на игровом поле."""
        pygame.draw.rect(surface, self.body_color,
                         (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        self.body_color = RED
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
                         random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self):
        self.body_color = GREEN
        self.length = 1
        self.positions = [(CELL_SIZE, CELL_SIZE)]  # Начальная позиция
        self.direction = (CELL_SIZE, 0)  # Движение вправо
        self.next_direction = None

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction

    def move(self):
        """Обновляет позицию змейки."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

        new_head = (self.positions[0][0] + self.direction[0],
                    self.positions[0][1] + self.direction[1])

        # Добавляем новую голову
        self.positions.insert(0, new_head)

        # Удаляем последний элемент, если длина не увеличилась
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for pos in self.positions:
            # Используем позицию каждой части тела змейки
            pygame.draw.rect(surface, self.body_color, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(CELL_SIZE, CELL_SIZE)]
        self.direction = (CELL_SIZE, 0)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction((0, -CELL_SIZE))
            elif event.key == pygame.K_DOWN:
                snake.update_direction((0, CELL_SIZE))
            elif event.key == pygame.K_LEFT:
                snake.update_direction((-CELL_SIZE, 0))
            elif event.key == pygame.K_RIGHT:
                snake.update_direction((CELL_SIZE, 0))


def main():
    """Основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Изгиб Питона")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.move()

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка на столкновение с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Отрисовка
        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
