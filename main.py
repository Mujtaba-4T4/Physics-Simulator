import pygame
import pygame_gui
import sys
from sim_gravity import GravitySim
from sim_heat import HeatSim
from sim_wave import WaveSim

WIDTH, HEIGHT = 1080, 720
BG_COLOR = (20, 20, 30)
FPS = 60
state = "menu"  
sim_speed = 1.0
camera_offset = pygame.Vector2(0, 0)  
zoom_level = 1.0                      

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monaspaceradonvarregular", 24)
arrow_font = pygame.font.SysFont("monaspaceradonvarregular", 40)

ui = pygame_gui.UIManager((WIDTH, HEIGHT))

gravity_button = pygame_gui.elements.UIButton(pygame.Rect(390, 150, 300, 100), "Gravity Simulation", manager=ui)
heat_button = pygame_gui.elements.UIButton(pygame.Rect(390, 280, 300, 100), "Heat Simulation", manager=ui)
wave_button = pygame_gui.elements.UIButton(pygame.Rect(390, 410, 300, 100), "Wave Simulation", manager=ui)
menu_buttons = [gravity_button, heat_button, wave_button]

# Gravity input labels and inputs
gravity_mass_label = pygame_gui.elements.UILabel(pygame.Rect(50, 100, 80, 30), "Mass", manager=ui)
gravity_mass_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(140, 100, 100, 30), manager=ui)
gravity_radius_label = pygame_gui.elements.UILabel(pygame.Rect(50, 140, 80, 30), "Radius", manager=ui)
gravity_radius_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(140, 140, 100, 30), manager=ui)
gravity_vx_label = pygame_gui.elements.UILabel(pygame.Rect(50, 180, 80, 30), "Vx", manager=ui)
gravity_vx_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(140, 180, 100, 30), manager=ui)
gravity_vy_label = pygame_gui.elements.UILabel(pygame.Rect(50, 220, 80, 30), "Vy", manager=ui)
gravity_vy_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(140, 220, 100, 30), manager=ui)
gravity_gravity_label = pygame_gui.elements.UILabel(pygame.Rect(50, 260, 80, 30), "Gravity", manager=ui)
gravity_gravity_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(140, 260, 100, 30), manager=ui)

grav_input_buttons = [gravity_mass_label, gravity_mass_input, gravity_radius_label, gravity_radius_input, gravity_vx_label, gravity_vx_input, gravity_vy_label,gravity_vy_input, gravity_gravity_label, gravity_gravity_input]

# Nx, Ny, dt input
Nx_label = pygame_gui.elements.UILabel(pygame.Rect(50, 220, 80, 30), "Nx", manager=ui)
Nx_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(140, 220, 100, 30), manager=ui)
Ny_label = pygame_gui.elements.UILabel(pygame.Rect(50, 260, 80, 30), "Ny", manager=ui)
Ny_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(140, 260, 100, 30), manager=ui)
dt_label = pygame_gui.elements.UILabel(pygame.Rect(50, 300, 80, 30), "dt", manager=ui)
dt_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(140, 300, 100, 30), manager=ui)
pde_input_buttons = [Nx_label, Nx_input, Ny_label, Ny_input, dt_label, dt_input]

# Heat input 
heat_alpha_label = pygame_gui.elements.UILabel(pygame.Rect(50, 340, 80, 30), "Alpha", manager=ui)
heat_alpha_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(140, 340, 100, 30), manager=ui)
heat_input_buttons = [heat_alpha_label, heat_alpha_input]

# Wave input
wave_c_label = pygame_gui.elements.UILabel(pygame.Rect(50, 340, 80, 30), "c (speed)", manager=ui)
wave_c_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(140, 340, 100, 30), manager=ui)
wave_input_buttons = [wave_c_label, wave_c_input]

for button in grav_input_buttons + heat_input_buttons + wave_input_buttons + pde_input_buttons:
    button.hide()

gravity_sim = None
heat_sim = None
wave_sim = None
mouse_held = False
right_mouse_held = False
spawn_particle = True
running = True
accum_time = 0.0
while running:
    dt = (clock.tick(FPS) / 500) * sim_speed
    accum_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        ui.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == gravity_button:
                    state = "gravity_input"
                    for button in menu_buttons:
                        button.hide()
                    for button in grav_input_buttons:
                        button.show()
                elif event.ui_element == heat_button:
                    state = "heat_input"
                    for button in menu_buttons:
                        button.hide()
                    for button in heat_input_buttons + pde_input_buttons:
                        button.show()
                elif event.ui_element == wave_button:
                    state = "wave_input"
                    for button in menu_buttons:
                        button.hide()
                    for button in wave_input_buttons + pde_input_buttons:
                        button.show()

        if state == "gravity_input":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                try:
                    mass = float(gravity_mass_input.get_text())
                    radius = float(gravity_radius_input.get_text())
                    vx = float(gravity_vx_input.get_text())
                    vy = float(gravity_vy_input.get_text())
                    gravity = float(gravity_gravity_input.get_text())
                except ValueError:
                    mass = 1
                    radius = 5
                    vx = 10
                    vy = 10
                    gravity = 9.81
                gravity_sim = GravitySim(mass, radius, vx, vy, gravity)
                state = "gravity"
                for button in grav_input_buttons:
                    button.hide()        

        elif state == "heat_input":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                try:
                    Nx = int(Nx_input.get_text())
                    Ny = int(Ny_input.get_text())
                    dt = float(dt_input.get_text())
                    alpha = float(heat_alpha_input.get_text())
                except ValueError:
                    Nx = 40
                    Ny = 40
                    dt = 20
                    alpha = 0.5
                heat_sim = HeatSim(WIDTH, HEIGHT, Nx, Ny, dt, alpha)
                state = "heat"
                for button in heat_input_buttons + pde_input_buttons:
                    button.hide()

        elif state == "wave_input":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                try:
                    Nx = int(Nx_input.get_text())
                    Ny = int(Ny_input.get_text())
                    dt = float(dt_input.get_text())
                    c = float(wave_c_input.get_text())
                except ValueError:
                    Nx = 80
                    Ny = 80
                    dt = 5
                    c = 0.5
                wave_sim = WaveSim(WIDTH, HEIGHT, Nx, Ny, dt, c)
                state = "wave"
                for button in wave_input_buttons + pde_input_buttons:
                    button.hide()            

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_held = True
                prev_mouse_pos = pygame.Vector2(event.pos)
            elif event.button == 3:
                right_mouse_held = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_held = False
            elif event.button == 3:
                right_mouse_held = False
            
        if state == "gravity" and mouse_held == True and spawn_particle == True:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            world_pos = mouse_pos / zoom_level + camera_offset
            gravity_sim.add_particle(world_pos)
        elif event.type == pygame.MOUSEMOTION and mouse_held and not spawn_particle:
            mouse_pos = pygame.Vector2(event.pos)
            delta = mouse_pos - prev_mouse_pos
            camera_offset -= delta / zoom_level
            prev_mouse_pos = mouse_pos

        if state == "heat" and mouse_held == True:
            heat_sim.heat(pygame.mouse.get_pos(), WIDTH, HEIGHT)
        elif state == "heat" and right_mouse_held == True:
            heat_sim.boundary(pygame.mouse.get_pos(), WIDTH, HEIGHT)

        if state == "wave" and mouse_held == True:
            wave_sim.interact(pygame.mouse.get_pos(), WIDTH, HEIGHT, )
        elif state == "wave" and right_mouse_held == True:
            wave_sim.boundary(pygame.mouse.get_pos(), WIDTH, HEIGHT)
            
        if event.type == pygame.KEYDOWN:
            if state == "gravity":
                if event.key == pygame.K_SPACE:
                    gravity_sim.pause_sim()
                if event.key == pygame.K_COMMA or event.key == pygame.K_LESS:
                    sim_speed = max(0.1, sim_speed - 0.1)
                if event.key == pygame.K_PERIOD or event.key == pygame.K_GREATER:
                    sim_speed = min(5.0, sim_speed + 0.1)
                if event.key == pygame.K_r:
                    camera_offset = pygame.Vector2(0, 0)
                    zoom_level = 1.0
                if event.key == pygame.K_m:
                    gravity_sim.attract()
                if event.key == pygame.K_n:
                    gravity_sim.repel()
                if event.key == pygame.K_p:
                    spawn_particle = not spawn_particle
                if event.key == pygame.K_g:
                    gravity_sim.gravity_enable()
                if event.key == pygame.K_w:
                    gravity_sim.gravity_up()
                if event.key == pygame.K_s:
                    gravity_sim.gravity_down()
                if event.key == pygame.K_a:
                    gravity_sim.gravity_left()
                if event.key == pygame.K_d:
                    gravity_sim.gravity_right()
                if event.key == pygame.K_ESCAPE:
                    state = "menu"
                    for button in menu_buttons:
                        button.show()
            elif state == "heat":
                if event.key == pygame.K_SPACE:
                    heat_sim.pause_sim()
                if event.key == pygame.K_COMMA or event.key == pygame.K_LESS:
                    sim_speed = max(0.1, sim_speed - 0.1)
                if event.key == pygame.K_PERIOD or event.key == pygame.K_GREATER:
                    sim_speed = min(5.0, sim_speed + 0.1)
                if event.key == pygame.K_r:
                    camera_offset = pygame.Vector2(0, 0)
                    zoom_level = 1.0
                if event.key == pygame.K_ESCAPE:
                    state = "menu"
                    for button in menu_buttons:
                        button.show()
            elif state == "wave":
                if event.key == pygame.K_SPACE:
                    wave_sim.pause_sim()
                if event.key == pygame.K_COMMA or event.key == pygame.K_LESS:
                    sim_speed = max(0.1, sim_speed - 0.1)
                if event.key == pygame.K_PERIOD or event.key == pygame.K_GREATER:
                    sim_speed = min(5.0, sim_speed + 0.1)
                if event.key == pygame.K_r:
                    camera_offset = pygame.Vector2(0, 0)
                    zoom_level = 1.0
                if event.key == pygame.K_ESCAPE:
                    state = "menu"
                    for button in menu_buttons:
                        button.show()    

        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                zoom_level *= 1.1
            elif event.y < 0:
                zoom_level *= 0.9

            zoom_level = max(0.5, min(5.0, zoom_level))

    screen.fill(BG_COLOR)

    if state in ["menu", "gravity_input", "heat_input", "wave_input"]:
        ui.update(dt)
        ui.draw_ui(screen)

    if state == "gravity":
        gravity_sim.update(dt, zoom_level, camera_offset)
        gravity_sim.draw(screen, font, arrow_font, camera_offset, zoom_level)
        border_rect_screen = pygame.Rect(0, 0, WIDTH, HEIGHT)
        border_rect_screen.topleft = (-camera_offset) * zoom_level
        border_rect_screen.size = (WIDTH * zoom_level, HEIGHT * zoom_level)
        pygame.draw.rect(screen, (200, 200, 200), border_rect_screen, width=2)
    elif state == "heat":
        heat_sim.update()
        heat_sim.draw(screen)
        border_rect_screen = pygame.Rect(0, 0, WIDTH, HEIGHT)
        border_rect_screen.topleft = (-camera_offset) * zoom_level
        border_rect_screen.size = (WIDTH * zoom_level, HEIGHT * zoom_level)
        pygame.draw.rect(screen, (200, 200, 200), border_rect_screen, width=2)
    elif state == "wave":
        wave_sim.update()
        wave_sim.draw(screen)
        border_rect_screen = pygame.Rect(0, 0, WIDTH, HEIGHT)
        border_rect_screen.topleft = (-camera_offset) * zoom_level
        border_rect_screen.size = (WIDTH * zoom_level, HEIGHT * zoom_level)
        pygame.draw.rect(screen, (200, 200, 200), border_rect_screen, width=2)
    pygame.display.flip()

pygame.quit()
sys.exit()