import json
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.patches import Rectangle

class ParkEnvironment:
    def __init__(self, width, height, grid_size=50):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.obstacles = []
        self.start = None
        self.goal = None
        

    
    def load_obstacles_from_json(self, file_path):
        """Load obstacles, start, and goal from a JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.start = data.get("start")
            self.goal = data.get("goal")
            self.obstacles.extend(data.get("obstacles", []))
            self.obstacles.extend(data.get("fence", []))

    def is_free(self, x, y, robot_radius=0):
        """Check if a point is in free space (not inside any obstacle)."""
        if not (0 <= x <= self.width and 0 <= y <= self.height):
            return False

        for obs in self.obstacles:
            pos_x, pos_y = obs['position']
            h, w = obs['height'], obs['width']
            if (pos_x - robot_radius <= x <= pos_x + w + robot_radius and
                    pos_y - robot_radius <= y <= pos_y + h + robot_radius):
                return False
        return True

    def draw_element(self, ax, element, is_obstacle=False):
        
            img = Image.open(element["image"])
            pos_x, pos_y = element["position"]
            pos_x = (pos_x // self.grid_size) * self.grid_size
            pos_y = (pos_y // self.grid_size) * self.grid_size
            h = (element["height"] // self.grid_size) * self.grid_size
            w = (element["width"] // self.grid_size) * self.grid_size
            ax.imshow(img, extent=(pos_x, pos_x + w, pos_y, pos_y + h))
        

    def visualize(self):
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal', adjustable='box')

        
        ax.add_patch(Rectangle((0, 0), self.width, self.height, color="lightgreen", zorder=0))

        
        for x in range(0, self.width, self.grid_size):
            ax.axvline(x, color='gray', linestyle='--', linewidth=0.5)
        for y in range(0, self.height, self.grid_size):
            ax.axhline(y, color='gray', linestyle='--', linewidth=0.5)

        for obs in self.obstacles:
            self.draw_element(ax, obs, is_obstacle=True)

        if self.start:
            self.draw_element(ax, self.start)

        if self.goal:
            self.draw_element(ax, self.goal)

        plt.grid(True)
        plt.show()
def main():
    # Initialize the environment
    env = ParkEnvironment(width=51, height=51, grid_size=3)

    # Path to the JSON file
    json_path = '/Users/farzanehhaghighatbin/Desktop/UCS_Project/Park/park.json'  # Ensure this file exists in the same directory or provide the correct path

    # Load the JSON file with 30 obstacles
    try:
        env.load_obstacles_from_json(json_path)
    except FileNotFoundError:
        print(f"Error: The file {json_path} was not found.")
        return
   
    # Visualize the environment
    env.visualize()

if __name__ == "__main__":
    main()