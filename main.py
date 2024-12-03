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

    def draw(self, frame):
        for i in range(self.rows):
            for j in range(self.cols):
                x1, y1 = j * self.cell_width, i * self.cell_height
                x2, y2 = (j + 1) * self.cell_width, (i + 1) * self.cell_height

                if self.maze[i][j] == 1:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), -1)

        cv2.circle(frame, (self.cell_width // 2, self.cell_height // 2), min(self.cell_width, self.cell_height) // 4,
                   (0, 255, 0), -1)
        cv2.circle(frame, ((self.cols - 1) * self.cell_width + self.cell_width // 2,
                           (self.rows - 1) * self.cell_height + self.cell_height // 2),
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
    rows = 15
    cols = 20

    maze = Maze(window_width, window_height, rows, cols)
    maze.generate()

    while not maze.solve((0, 0), (rows - 1, cols - 1)):
        maze.generate()

    handsDetector = mp.solutions.hands.Hands()

    victory = False
    while cap.isOpened():
        ret, frame = cap.read()

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

            finish_x = (cols - 1) * maze.cell_width + maze.cell_width // 2
            finish_y = (rows - 1) * maze.cell_height + maze.cell_height // 2
            if abs(x_tip - finish_x) < maze.cell_width // 2 and abs(y_tip - finish_y) < maze.cell_height // 2:
                victory = True

        maze.draw(frame)

        if victory:
            cv2.putText(frame, "YOU WIN!!!", (window_width // 2 - 150, window_height // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

        cv2.imshow("Maze Game", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

main()
