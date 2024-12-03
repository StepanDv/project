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


def main():
    cap = cv2.VideoCapture(0)
    window_width = 1000
    window_height = 600
    rows = 15
    cols = 20

    maze = Maze(window_width, window_height, rows, cols)
    maze.generate()

    while cap.isOpened():
        ret, frame = cap.read()

        frame = cv2.flip(frame, 1)

        frame = cv2.resize(frame, (window_width, window_height))

        maze.draw(frame)
        cv2.imshow("Maze Game", frame)

        if cv2.waitKey(1) & 0xFF == 27 or not ret:
            break

main()