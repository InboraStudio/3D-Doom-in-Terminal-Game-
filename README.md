# 3D-Doom-in-Terminal-Game-
A Python Game in Terminal with All Deep Research log's and formulas



https://github.com/user-attachments/assets/1b2ab652-7a71-4df5-9b34-1339f73e7f6a



## A lightweight raycasting engine that runs directly in your terminal!  
Inspired by classic games like **Doom** and **Wolfenstein 3D**, this project simulates 3D environments using **ASCII characters** and basic trigonometry.

---

##  Game Logic Breakdown (Math-Based)

This project uses fundamental raycasting techniques to simulate a 3D world from a 2D map.

### Player
- **Position:** `P = (px, py)`
- **View angle (facing direction):** `θ` in radians

---

### Raycasting Per Column

For each column `i` on the terminal screen:

### 1. **Field of View**
```cpp
FOV = π / 3 # e.g. 60 degrees field of view ray_angle = θ - (FOV / 2) + (i / screen_width) * FOV
```


#### 2. **Ray Angle**
```cpp
ray_angle = θ - (FOV / 2) + (i / screen_width) * FOV
```

#### 3. **Ray Direction Vector**
```cpp

https://github.com/user-attachments/assets/4cd98917-8033-4464-a7ce-5cff0fca05cc


ray_dir_x = cos(ray_angle)
ray_dir_y = sin(ray_angle)
```
- Iterate along the ray in small steps until a wall is hit.

![image](https://github.com/user-attachments/assets/ea5be348-f84c-45fb-8f60-a34538908847)

#### 4. **Ray Marching (DDA Algorithm)**
Iteratively step through the map until a wall is hit:

```cpp
(x, y) = (px, py)

loop:
    x += ray_dir_x * step
    y += ray_dir_y * step
    if map[⌊y⌋][⌊x⌋] == wall:
        break
```

#### 5. **Distance to Wall**
```cpp
distance = sqrt((x - px)² + (y - py)²)
```

#### 6. **Wall Height on Terminal**
```cpp
wall_height = screen_height / distance
```

#### 7. **Shading by Distance**
```cpp
if distance < close:        char = '█'
elif distance < medium:     char = '▓'
elif distance < far:        char = '░'
else:                       char = '.'
```

#### 8. **Rotation (Left/Right)**
```cpp
θ += Δθ # positive for right, negative for left
```

#### 9. **Movement (W/S or Up/Down)**
```cpp
px += cos(θ) * move_speed # forward py += sin(θ) * move_speed px -= cos(θ) * move_speed # backward py -= sin(θ) * move_speed
```
---

### Controls

| Key         | Action                   |
|-------------|--------------------------|
| ← / →       | Rotate view (left/right) |
| ↑ / ↓       | Move forward/backward    |
| W / S       | Optional movement keys   |

---

### Map

The world is a 2D grid:

```python
map = [
    [1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1],
    [1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1],
    [1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1]
]
```

Where:
- `1` = Wall
- `0` = Walkable space

---

## Dependencies

- Python 3
- `curses` (comes with Python for Unix/macOS)
  - Windows: use `windows-curses` via `pip install windows-curses`

---


## Credits

Built with ❤️ using:
- ASCII art rendering
- Basic trigonometry
- Classic game engine inspiration

---

##  Future Ideas

- Add monsters or objects
- Map editor using text input
- Minimap overlay
- Save/load map feature
