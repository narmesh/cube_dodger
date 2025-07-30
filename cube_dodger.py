from ursina import *
import random
from math import sin, cos, radians

# Initialize Ursina
app = Ursina()

# Game constants
PLATFORM_SIZE = 20  # Size of the accessible platform
FORWARD_SPEED = 8
OBSTACLE_SPAWN_DISTANCE = 25
GROUND_SIZE = 50
PLAYER_SPEED = 12  # Speed for manual movement

class Player(Entity):
    def __init__(self):
        super().__init__(
            model='cube',
            color=color.blue,
            scale=(0.5, 0.5, 0.5),
            position=(0, 0.5, 0)
        )
        self.is_jumping = False
        self.jump_speed = 0
        self.original_scale_y = 0.5
        self.move_speed = PLAYER_SPEED
        self.auto_forward = False  # Start with auto-forward disabled
        
        print(f"Player created at position: {self.position}")
        
    def update(self):
        # Handle jumping
        if self.is_jumping:
            self.jump_speed -= 15 * time.dt
            self.y += self.jump_speed * time.dt
            
            if self.y <= 0.5:
                self.y = 0.5
                self.is_jumping = False
                self.jump_speed = 0
    
        # Only apply auto-forward when enabled and not being manually controlled
        if self.auto_forward and not (held_keys['up arrow'] or held_keys['down arrow']):
            new_z = self.z + FORWARD_SPEED * time.dt * 0.3  # Slower auto movement
            half_platform = PLATFORM_SIZE / 2
            if new_z <= half_platform - 1:
                self.z = new_z
    
    def move_left(self):
        new_x = self.x - self.move_speed * time.dt
        half_platform = PLATFORM_SIZE / 2
        if new_x >= -half_platform + 1:  # Better buffer
            self.x = new_x

    def move_right(self):
        new_x = self.x + self.move_speed * time.dt
        half_platform = PLATFORM_SIZE / 2
        if new_x <= half_platform - 1:  # Better buffer
            self.x = new_x

    def move_forward(self):
        new_z = self.z + self.move_speed * time.dt
        half_platform = PLATFORM_SIZE / 2
        if new_z <= half_platform - 1:
            self.z = new_z

    def move_backward(self):
        new_z = self.z - self.move_speed * time.dt
        half_platform = PLATFORM_SIZE / 2
        if new_z >= -half_platform + 1:
            self.z = new_z
    
    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_speed = 8
            print("Player jumping!")

class Obstacle(Entity):
    def __init__(self, x_pos, z_pos, obstacle_type):
        self.obstacle_type = obstacle_type
        
        if obstacle_type == "normal":
            super().__init__(
                model='cube',
                color=color.red,
                scale=(0.5, 1, 0.5),
                position=(x_pos, 0.5, z_pos)
            )
        elif obstacle_type == "low":
            super().__init__(
                model='cube',
                color=color.orange,
                scale=(0.5, 0.5, 0.5),
                position=(x_pos, 0.25, z_pos)
            )
        elif obstacle_type == "tall":
            super().__init__(
                model='cube',
                color=color.magenta,
                scale=(0.5, 1.5, 0.5),
                position=(x_pos, 0.75, z_pos)
            )
        elif obstacle_type == "wide":
            super().__init__(
                model='cube',
                color=color.yellow,
                scale=(1.5, 0.8, 0.5),
                position=(x_pos, 0.4, z_pos)
            )
        
        print(f"Obstacle created: {obstacle_type} at position {self.position}")
    
    def update(self):
        # Simple movement toward the center of the platform
        center = Vec3(0, 0, 0)
        direction_to_center = center - self.position
        direction_to_center.y = 0  # Don't move vertically
        
        if direction_to_center.length() > 0.5:
            direction_to_center = direction_to_center.normalized()
            self.position += direction_to_center * game_speed * 0.5 * time.dt
    
        # Remove obstacle when it reaches the center or goes too far
        if distance(self, center) < 1 or distance(self, center) > PLATFORM_SIZE:
            destroy(self)
            if self in obstacles:
                obstacles.remove(self)

class CameraController:
    def __init__(self, target):
        self.target = target
        self.mode = "follow"  # "follow", "fixed", "orbit", "first_person"
        self.orbit_angle = 0
        self.distance = 8
        self.height = 5
        
    def update(self):
        if self.mode == "follow":
            # Smooth following camera
            target_pos = self.target.position + Vec3(0, self.height, -self.distance)
            camera.position = lerp(camera.position, target_pos, time.dt * 5)
            camera.look_at(self.target)
            
        elif self.mode == "fixed":
            # Fixed position overlooking the platform
            camera.position = Vec3(0, 15, -PLATFORM_SIZE/2)
            camera.look_at(self.target)
            
        elif self.mode == "orbit":
            # Orbiting camera around the player
            self.orbit_angle += time.dt * 30  # Rotate 30 degrees per second
            offset_x = sin(radians(self.orbit_angle)) * self.distance
            offset_z = cos(radians(self.orbit_angle)) * self.distance
            camera.position = self.target.position + Vec3(offset_x, self.height, offset_z)
            camera.look_at(self.target)
            
        elif self.mode == "first_person":
            # First person view
            camera.position = self.target.position + Vec3(0, 0.3, 0)
            camera.rotation = self.target.rotation
    
    def cycle_mode(self):
        modes = ["follow", "fixed", "orbit", "first_person"]
        current_index = modes.index(self.mode)
        self.mode = modes[(current_index + 1) % len(modes)]
        print(f"Camera mode: {self.mode}")
    
    def adjust_distance(self, delta):
        self.distance = max(3, min(15, self.distance + delta))
        print(f"Camera distance: {self.distance}")

class GameManager:
    def __init__(self):
        self.score = 0
        self.game_over = False
        self.spawn_timer = 0
        self.spawn_interval = 1.5
        self.speed_increase_timer = 0
        
    def update(self):
        global game_speed
        
        if self.game_over:
            return
            
        # Update score
        self.score += time.dt * 10
        score_text.text = f'Score: {int(self.score)}'
        
        # Increase speed over time
        self.speed_increase_timer += time.dt
        if self.speed_increase_timer >= 5:
            game_speed += 0.3
            self.speed_increase_timer = 0
            print(f"Speed increased to: {game_speed}")
        
        # Spawn obstacles
        self.spawn_timer += time.dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_obstacle()
            self.spawn_timer = 0
            self.spawn_interval = max(0.8, self.spawn_interval - 0.005)
    
    def spawn_obstacle(self):
        global metrics
        # Spawn obstacles at the edges of the platform
        half_platform = PLATFORM_SIZE / 2 - 1  # Stay within bounds
    
        # More controlled spawning
        spawn_positions = [
            # Front edge
            (random.uniform(-half_platform, half_platform), half_platform),
            # Back edge
            (random.uniform(-half_platform, half_platform), -half_platform),
            # Left edge
            (-half_platform, random.uniform(-half_platform, half_platform)),
            # Right edge
            (half_platform, random.uniform(-half_platform, half_platform))
        ]
    
        x_pos, z_pos = random.choice(spawn_positions)
        obstacle_type = random.choice(["normal", "low", "tall", "wide"])
        obstacle = Obstacle(x_pos, z_pos, obstacle_type)
        obstacles.append(obstacle)
        metrics['obstacles_spawned'] += 1
    
    def check_collision(self):
        if self.game_over:
            return
            
        for obstacle in obstacles:
            # Check if obstacle is near player
            if distance(obstacle, player) < 0.8:
                # Check height collision based on obstacle type
                collision = False
                
                if obstacle.obstacle_type in ["normal", "wide"]:
                    collision = True
                elif obstacle.obstacle_type == "low":
                    if player.y < 1.2:  # Can jump over
                        collision = True
                elif obstacle.obstacle_type == "tall":
                    collision = True  # Always collides (too tall to jump)
                
                if collision:
                    self.game_over = True
                    self.show_game_over()
                    print("COLLISION! Game Over!")
    
    def show_game_over(self):
        game_over_text.text = f'GAME OVER!\nFinal Score: {int(self.score)}\nPress R to Restart'
        game_over_text.enabled = True
    
    def restart_game(self):
        global game_speed, metrics
        self.game_over = False
        self.score = 0
        game_speed = FORWARD_SPEED
        self.spawn_timer = 0
        self.spawn_interval = 1.5
        self.speed_increase_timer = 0
        
        # Reset player
        player.position = (0, 0.5, -PLATFORM_SIZE/4)
        player.is_jumping = False
        player.jump_speed = 0
        
        # Clear obstacles
        for obstacle in obstacles[:]:
            destroy(obstacle)
        obstacles.clear()
        
        # Reset metrics
        metrics['obstacles_spawned'] = 0
        
        game_over_text.enabled = False
        print("Game restarted!")

# Create platform ground
ground = Entity(
    model='cube',
    color=color.gray,
    scale=(PLATFORM_SIZE, 0.05, PLATFORM_SIZE),
    position=(0, -0.25, 0)
)

# Create platform borders for visual reference
border_thickness = 0.1
borders = [
    # Front border
    Entity(model='cube', color=color.white, scale=(PLATFORM_SIZE, 0.2, border_thickness), 
           position=(0, 0, PLATFORM_SIZE/2)),
    # Back border  
    Entity(model='cube', color=color.white, scale=(PLATFORM_SIZE, 0.2, border_thickness), 
           position=(0, 0, -PLATFORM_SIZE/2)),
    # Left border
    Entity(model='cube', color=color.white, scale=(border_thickness, 0.2, PLATFORM_SIZE), 
           position=(-PLATFORM_SIZE/2, 0, 0)),
    # Right border
    Entity(model='cube', color=color.white, scale=(border_thickness, 0.2, PLATFORM_SIZE), 
           position=(PLATFORM_SIZE/2, 0, 0)),
]

# Create grid lines for better visual reference
grid_lines = []
grid_spacing = 2
for i in range(-int(PLATFORM_SIZE/2), int(PLATFORM_SIZE/2) + 1, grid_spacing):
    if i != 0:  # Skip center lines
        # Vertical lines
        grid_lines.append(Entity(
            model='cube',
            color=color.light_gray,
            scale=(0.05, 0.05, PLATFORM_SIZE),
            position=(i, 0.01, 0)
        ))
        # Horizontal lines
        grid_lines.append(Entity(
            model='cube',
            color=color.light_gray,
            scale=(PLATFORM_SIZE, 0.05, 0.05),
            position=(0, 0.01, i)
        ))

# Initialize game objects
player = Player()
obstacles = []
game_manager = GameManager()
game_speed = FORWARD_SPEED
camera_controller = CameraController(player)

# Initialize metrics
metrics = {
    'fps': 0,
    'obstacles_spawned': 0,
    'obstacles_active': 0,
    'current_speed': game_speed,
    'player_position': (0, 0, 0),
    'camera_mode': 'follow'
}

# Set up initial camera
camera.position = (0, 5, -8)
camera.rotation_x = 25
camera.fov = 75

print(f"Camera position: {camera.position}")

def update():
    # Update camera
    camera_controller.update()
    
    # Update game manager
    game_manager.update()
    game_manager.check_collision()
    
    # Update metrics
    update_metrics()

def update_metrics():
    global metrics
    metrics['fps'] = int(1/time.dt) if time.dt > 0 else 0
    metrics['obstacles_active'] = len(obstacles)
    metrics['current_speed'] = round(game_speed, 1)
    metrics['player_position'] = (round(player.x, 1), round(player.y, 1), round(player.z, 1))
    metrics['camera_mode'] = camera_controller.mode
    
    # Update metrics display
    metrics_text.text = f'FPS: {metrics["fps"]}\nSpeed: {metrics["current_speed"]}\nObstacles: {metrics["obstacles_active"]}\nPos: {metrics["player_position"]}\nCam: {metrics["camera_mode"]}'

# Input handling with new controls
def input(key):
    if not game_manager.game_over:
        # Movement controls
        if key == 'left arrow':
            player.move_left()
        elif key == 'right arrow':
            player.move_right()
        elif key == 'up arrow':
            player.move_forward()
        elif key == 'down arrow':
            player.move_backward()
        elif key == 'space':
            player.jump()
    
    # Camera controls (available anytime)
    if key == 'c':
        camera_controller.cycle_mode()
    
    if key == 'v':
        # Toggle auto-forward movement
        player.auto_forward = not player.auto_forward
        print(f"Auto-forward: {player.auto_forward}")
    
    # Camera distance adjustment
    if key == 'page up':
        camera_controller.adjust_distance(-1)
    elif key == 'page down':
        camera_controller.adjust_distance(1)
    
    if key == 'r' and game_manager.game_over:
        game_manager.restart_game()
    
    if key == 'escape':
        quit()

# Continuous input handling for smooth movement
def update_input():
    if not game_manager.game_over:
        if held_keys['left arrow']:
            player.move_left()
        if held_keys['right arrow']:
            player.move_right()
        if held_keys['up arrow']:
            player.move_forward()
        if held_keys['down arrow']:
            player.move_backward()

# Add continuous input to the main update loop
original_update = update
def update():
    original_update()
    update_input()

# UI Elements
score_text = Text(
    'Score: 0',
    position=(-0.8, 0.45),
    scale=2,
    color=color.white
)

game_over_text = Text(
    '',
    position=(0, 0),
    scale=2,
    color=color.red,
    origin=(0, 0),
    enabled=False
)

metrics_text = Text(
    'FPS: 0\nSpeed: 0\nObstacles: 0\nPos: (0,0,0)\nCam: follow',
    position=(0.5, 0.4),
    scale=1.2,
    color=color.cyan,
    origin=(0, 0)
)

instructions_text = Text(
    'Arrows: Move in all directions | Space: Jump | C: Camera | V: Auto-Forward | PgUp/Dn: Zoom | R: Restart | ESC: Quit',
    position=(0, -0.45),
    scale=0.8,
    color=color.light_gray,
    origin=(0, 0)
)

# Add some basic lighting
light = DirectionalLight()
light.position = (2, 2, 2)
light.rotation = (45, -45, 45)

# Set window properties
window.title = 'Cube Dodger - 3D Free Movement Runner'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# Start the game
if __name__ == '__main__':
    print("Starting Cube Dodger - Free Movement Edition!")
    print("Controls:")
    print("- Arrow Keys: Move in all directions")
    print("- Space: Jump")
    print("- C: Cycle camera modes (Follow/Fixed/Orbit/First-Person)")
    print("- V: Toggle auto-forward movement")
    print("- Page Up/Down: Adjust camera distance")
    print("- R: Restart (when game over)")
    print("- ESC: Quit")
    print(f"Player starts at: {player.position}")
    print(f"Platform size: {PLATFORM_SIZE}x{PLATFORM_SIZE}")
    
    app.run()
