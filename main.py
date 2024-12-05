import cv2
import random
import mediapipe as mp

class Maze:
    def __init__(self, width, height, rows, cols):
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.cell_width = width // cols
        self.cell_height = height // rows
        self.maze = [[1 for _ in range(cols)] for _ in range(rows)]
        self.player_pos = (self.cell_width // 2, self.cell_height // 2)

    def generate(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.maze[i][j] = random.randint(0, 1)

    def draw(self, frame, ox, oy):
        for i in range(-1, self.rows + 1):
            for j in range(-1, self.cols + 1):
                x1, y1 = ox + j * self.cell_width, oy + i * self.cell_height
                x2, y2 = ox + (j + 1) * self.cell_width, oy + (i + 1) * self.cell_height

                if i == -1 or j == -1 or i == self.rows or j == self.cols or self.maze[i][j] == 1:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), -1)

        cv2.circle(frame, (ox + self.cell_width // 2, oy + self.cell_height // 2), min(self.cell_width, self.cell_height) // 4,
                   (0, 255, 0), -1)
        cv2.circle(frame, (ox + (self.cols - 1) * self.cell_width + self.cell_width // 2,
                           oy + (self.rows - 1) * self.cell_height + self.cell_height // 2),
                   min(self.cell_width, self.cell_height) // 4, (255, 0, 0), -1)

    def solve(self, start, end):
        stack = [start]
        used = set()

        if self.maze[start[0]][start[1]] == 1:
            return False

        while stack:
            x, y = stack.pop()

            if (x, y) == end:
                return True

            used.add((x, y))

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.rows and 0 <= ny < self.cols:
                    if (nx, ny) not in used and self.maze[nx][ny] == 0:
                        stack.append((nx, ny))

        return False


def main():
    cap = cv2.VideoCapture(1)
    window_width = 1000
    window_height = 600
    maze_width = 500
    maze_height = 350
    rows = 8
    cols = 10

    while cap.isOpened():
        maze = Maze(maze_width, maze_height, rows, cols)
        maze.generate()

        while not maze.solve((0, 0), (rows - 1, cols - 1)):
            maze.generate()

        handsDetector = mp.solutions.hands.Hands()

        game_started = False
        victory = False
        game_over = False

        ox = (window_width - maze_width) // 2
        oy = (window_height - maze_height) // 2

        while cap.isOpened():
            ret, frame = cap.read()

            if cv2.waitKey(1) & 0xFF == 27 or not ret:
                exit(0)

            if cv2.waitKey(1) & 0xFF == ord('r'):
                break

            frame = cv2.flip(frame, 1)

            frame = cv2.resize(frame, (window_width, window_height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = handsDetector.process(frame)

            if results.multi_hand_landmarks and not victory:
                x_tip = int(results.multi_hand_landmarks[0].landmark[8].x *
                            frame.shape[1])
                y_tip = int(results.multi_hand_landmarks[0].landmark[8].y *
                            frame.shape[0])
                cv2.circle(frame, (x_tip, y_tip), 10, (255, 0, 0), -1)

                finish_x = ox + (cols - 1) * maze.cell_width + maze.cell_width // 2
                finish_y = oy + (rows - 1) * maze.cell_height + maze.cell_height // 2
                start_x = ox + maze.cell_width // 2
                start_y = oy + maze.cell_height // 2

                if game_started and not victory:
                    maze_x = (x_tip - ox) // maze.cell_width
                    maze_y = (y_tip - oy) // maze.cell_height
                    if maze_x == -1 or maze_x == maze.cols or maze_y == -1 or maze_y == maze.rows or (
                            0 <= maze_x < cols and 0 <= maze_y < rows and maze.maze[maze_y][maze_x] == 1):
                        game_over = True

                if not game_started and abs(x_tip - start_x) < maze.cell_width // 2 and abs(
                        y_tip - start_y) < maze.cell_height // 2:
                    game_started = True

                if not game_over and game_started and (x_tip - finish_x) < maze.cell_width // 2 and abs(
                        y_tip - finish_y) < maze.cell_height // 2:
                    victory = True

            maze.draw(frame, ox, oy)

            if not game_started and not game_over:
                cv2.putText(frame, "Place your finger in the START circle!",
                            (window_width // 2 - 300, window_height - 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            if victory:
                cv2.putText(frame, "YOU WIN! Press R to restart the game",
                            (window_width // 2 - 300, window_height - 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            if game_over:
                cv2.putText(frame, "Game Over! Press R to restart the game",
                            (window_width // 2 - 350, window_height - 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            cv2.imshow("Maze Game", frame)


main()
