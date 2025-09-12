# Physics Simulator

Physics Simulator is a interactive tool for exploring gravitational particle dynamics, heat diffusion, and wave propagation.

## Requirements
- `Python 3.8+`
- `pygame`
- `pygame_gui`
- `numpy`
- `matplotlib`

## How to Use
- Run `main.py` to access the main menu.
   - Choose Gravity, Heat, or Wave simulation.

- Configure Parameters:
   - Enter the parameters in input screen.
   - Input values (e.g., mass, radius, grid size, time step)
   - press `Enter`. Invalid inputs use default values.

- Interact with Simulations:
   - Gravity Simulation:
     - `Left-click` : Spawn particles.
     - `P` : Toggle spawning/panning.
     - `M`/`N` : Enable attraction/repulsion.
     - `G` : Toggle gravity.
     - `W`/`A`/`S`/`D` : Set gravity direction (up/left/down/right).
     - `Space` : Pause/resume.
     - `<`/`>` : Adjust speed (0.1x–5.0x).
     - `R` : Reset view.
     - `Esc` : Return to menu.
       
   - Heat Simulation:
     - `Left-click` : Add heat.
     - `Right-click` : Toggle fixed boundaries.
     - `Space` : Pause/resume.
     - `<`/`>` : Adjust speed.
     - `R` : Reset view.
     - `Esc` : Return to menu.
       
   - Wave Simulation:
     - `Left-click` : Create wave disturbances.
     - `Right-click` : Toggle fixed boundaries.
     - `Space` : Pause/resume.
     - `<`/`>` : Adjust speed.
     - `R` : Reset view.
     - `Esc` : Return to menu.

- Camera Controls:
   - `Mouse wheel` : Zoom in/out 
   - `Drag` : Pan camera (Particle spawning must be off for Gravity simulation)

## Project Structure
- `main.py`: Manages the application loop and UI.
- `sim_gravity.py`: Simulates gravity and collisions of particles.
- `sim_heat.py`: Simulates 2D heat diffusion.
- `sim_wave.py`: Simulates 2D wave propagation.
