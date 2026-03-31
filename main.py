# exemple_squelette.py

# Exemple d'import
from snake import *
from map import *
import tkinter as tk

def draw_grid(canvas, grid):
    canvas.delete("all")
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            x1, y1 = c * CELL_SIZE, r * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            cell_value = grid[r, c]
            color = colors.get(cell_value, "white")
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

def q_function(snake: Snake, map: Map) -> int:
    random = generate_random(0, 3)
    coords = snake.project_head(directions[random])
    q = map.evaluate_value(coords)
    
# def func(map: Map, snake : Snake):
def test_snake(snake: Snake, map: Map, canvas):
    random = generate_random(0, 3)
    coords = snake.project_head(directions[random])
    while (not map.is_empty_space(coords)):
        random = generate_random(0, 3)
        coords = snake.project_head(directions[random])
    print(directions_names[random])
    snake.update_snake(coords, map.grid_)
    draw_grid(canvas, map.grid_)
    canvas.after(500, lambda: test_snake(snake, map, canvas))

def main():
    map = Map(10)
    snake = Snake([(1,3), (1,4), (1,5)], map.grid_)
    snake.print(map.grid_)
    root = tk.Tk()
    root.title("Snake")
    root.geometry("400x400")  # optionnel : taille en pixels
    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()
    draw_grid(canvas, map.grid_)
    canvas.after(10, lambda: test_snake(snake, map, canvas))
    root.mainloop()

if __name__ == "__main__":
    main()