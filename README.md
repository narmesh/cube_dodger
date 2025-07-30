# 🟦 Cube Dodger — 3D Free Movement Runner
![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Ursina Engine](https://img.shields.io/badge/Ursina-Game%20Engine-orange?logo=unity)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Playable-brightgreen)

**Cube Dodger** is a fast-paced 3D endless runner game built in **Python using the Ursina Engine**. You control a cube on a large platform, dodging dynamically spawning obstacles while managing increasing speed. The challenge? **Survive as long as you can and beat your high score!**

---

## 🎮 Gameplay Features
- 🟦 Free 3D Movement (Left, Right, Forward, Backward)
- 🕹️ Dynamic Camera Modes (Follow, Fixed, Orbit, First-Person)
- 🚧 Randomized Obstacle Spawning (Low, Tall, Wide)
- 🏃 Auto-Forward Mode Toggle
- 🏆 Score & Speed Scaling System
- 📊 Real-time Metrics Display (FPS, Speed, Obstacles)

---

## 📦 Dependencies
| Library  | Purpose                    |
|----------|----------------------------|
| `ursina` | 3D game engine (main framework) |
| `random` | Obstacle spawn logic |
| `math`   | Camera orbit & rotation math |

### Install Dependencies:
```bash
pip install ursina
```

## 📂 Folder Structure
```
cube_dodger/
├── cube_dodger.py      # Main game file (single-file project)
└── README.md            # Project documentation
```

## ▶️ How to Play
- Make sure Python 3.8+ is installed.
- Install required dependencies:
```
pip install ursina
```
- Run the game:
```
python cube_dodger.py
```

## 🎮 Controls
| Action                 | Key(s)              |
| ---------------------- | ------------------- |
| Move Left              | ⬅️ Left Arrow       |
| Move Right             | ➡️ Right Arrow      |
| Move Forward           | ⬆️ Up Arrow         |
| Move Backward          | ⬇️ Down Arrow       |
| Jump                   | Spacebar            |
| Toggle Auto-Forward    | V                   |
| Cycle Camera Modes     | C                   |
| Adjust Camera Zoom     | Page Up / Page Down |
| Restart (on Game Over) | R                   |
| Quit Game              | ESC                 |

## 🧩 Gameplay Logic Breakdown
- Obstacles spawn from all platform edges and move towards the center.
- Obstacle Types:

  - Normal Block (Red): Dodge sideways.
  - Low Wall (Orange): Jump over.
  - Tall Wall (Magenta): Must dodge sideways.
  - Wide Block (Yellow): Occupies more space horizontally.
- Collision with obstacles ends the game.
- Game Speed increases every few seconds.
- Camera Modes can be switched on-the-fly.

## 📊 On-Screen Metrics
- FPS Counter
- Current Game Speed
- Active Obstacles Count
- Player Position Coordinates
- Camera Mode Status

## 📸 Screenshots
<img width="1365" height="719" alt="image" src="https://github.com/user-attachments/assets/b628ac5a-0095-4dc1-bc1a-d3e35a16b49e" />


## 👨‍💻 Author
[Narmesh Kumar Sah](https://github.com/narmesh/)

## ⭐️ Give it a Star!
If you like this project, don't forget to ⭐️ star it on GitHub!
