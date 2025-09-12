import pygame
import numpy as np
import matplotlib.pyplot as plt

WIDTH, HEIGHT = 1080, 720
e = 0.7 
g = 9.81  
gravity = "down"
gravity_enabled = True
pause = False


class Particle:
    def __init__(self, position, velocity, radius):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.radius = radius


    def update(self, dt, g, gravity, gravity_enabled):
        self.position += self.velocity * dt
        if gravity_enabled == True:
            if gravity == "down" or gravity == "up":
                self.velocity[1] += g * dt
            elif gravity == "left" or gravity == "right":
                self.velocity[0] += g * dt
        self.handle_wall_collision()

    def handle_wall_collision(self):
        if self.position[0] + self.radius > WIDTH:
            self.position[0] = WIDTH - self.radius  
            if self.velocity[0] > 0:
                self.velocity[0] = -e * self.velocity[0]
                if abs(self.velocity[0]) < 5.5:
                    self.velocity[0] = 0

        if self.position[0] - self.radius < 0:
            self.position[0] = self.radius
            if self.velocity[0] < 0:
                self.velocity[0] = -e * self.velocity[0]
                if abs(self.velocity[0]) < 5.5:
                    self.velocity[0] = 0
                    
        if self.position[1] + self.radius > HEIGHT:
            self.position[1] = HEIGHT - self.radius
            if self.velocity[1] > 0:
                self.velocity[1] = -e * self.velocity[1]
                if abs(self.velocity[1]) < 5.0:
                    self.velocity[1] = 0

        if self.position[1] - self.radius < 0:
            self.position[1] = self.radius
            self.velocity[0] *= 0.95 
            if self.velocity[1] < 0:
                self.velocity[1] = -e * self.velocity[1]
                if abs(self.velocity[1]) < 5.0:
                    self.velocity[1] = 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position.astype(int), self.radius)


class GravitySim:
    def __init__(self, mass, radius, vx, vy, gravity):
        self.particles = []
        self.mass = mass
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.g = gravity
        self.gravity = "down"
        self.gravity_enabled = gravity_enabled
        self.pause = pause
        self.cmap = plt.get_cmap("plasma")
        self.attractor = None

    def add_particle(self, position):
        velocity = np.array([self.vx, self.vy], dtype=float)

        self.particles.append(Particle(position=position, velocity=velocity, radius=self.radius))

    def gravity_enable(self):
        if self.gravity_enabled == True:
            self.gravity_enabled = False
        elif self.gravity_enabled == False:
            self.gravity_enabled = True

    def gravity_up(self):
        self.g = -1 * abs(self.g)
        self.gravity = "up"

    def gravity_down(self):
        self.g = abs(self.g)
        self.gravity = "down"

    def gravity_left(self):
        self.g = -1 * abs(self.g)
        self.gravity = "left"

    def gravity_right(self):
        self.g = abs(self.g)
        self.gravity = "right"

    def pause_sim(self):
        if self.pause == True:
            self.pause = False
        elif self.pause == False:
            self.pause = True

    def attract(self):
        if self.attractor == None:
            self.attractor = "attract"
        elif self.attractor == "attract":
            self.attractor = None

    def repel(self):
        if self.attractor == None:
            self.attractor = "repel"
        elif self.attractor == "repel":
            self.attractor = None

    def collision(self, p1, p2):
        delta = p2.position - p1.position
        dist = np.linalg.norm(delta)
        if dist == 0:
            return

        normal = delta / dist
        rel_vel = p2.velocity - p1.velocity
        vel_along_normal = np.dot(rel_vel, normal)

        if vel_along_normal > 0:
            return

        impulse = -(1 + e) * vel_along_normal * normal / 2
        p1.velocity -= impulse
        p2.velocity += impulse

        if abs(p1.velocity[1]) < 0.1:
            p1.velocity[1] = 0
        if abs(p1.velocity[0]) < 0.1:
            p1.velocity[0] = 0
        if abs(p2.velocity[1]) < 0.1:
            p2.velocity[1] = 0
        if abs(p2.velocity[0]) < 0.1:
            p2.velocity[0] = 0

        overlap = p1.radius + p2.radius - dist
        correction = normal * (overlap / 2)
        p1.position -= correction
        p2.position += correction
        p1.handle_wall_collision()
        p2.handle_wall_collision()


    def update(self, dt, zoom_level, camera_offset):
        if self.pause == False:
            mouse_pos = np.array(pygame.mouse.get_pos(), dtype=float) / zoom_level + camera_offset
            k = 5000  

            for p in self.particles:
                if self.attractor in ['attract', 'repel']:
                    direction = mouse_pos - p.position
                    distance_sq = np.dot(direction, direction) + 1e-6
                    direction_norm = direction / np.sqrt(distance_sq)
                    strength = 1 if self.attractor == 'attract' else -1
                    force = strength * k / distance_sq
                    p.velocity += force * direction_norm


                p.update(dt, self.g, self.gravity, self.gravity_enabled)

            cell_size = 2 * self.radius
            grid = {}
            for p in self.particles:
                cell = (int(p.position[0] // cell_size), int(p.position[1] // cell_size))
                grid.setdefault(cell, []).append(p)

            processed = set()
            for cell, plist in grid.items():
                neighbors = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        neighbors.extend(grid.get((cell[0]+dx, cell[1]+dy), []))

                for p1 in plist:
                    for p2 in neighbors:
                        if p1 is p2:
                            continue
                        key = tuple(sorted((id(p1), id(p2))))
                        if key in processed:
                            continue
                        if np.linalg.norm(p1.position - p2.position) < p1.radius + p2.radius:
                            self.collision(p1, p2)
                            processed.add(key)

    def draw(self, surface, font, arrow_font, camera_offset, zoom_level):
        if self.gravity == "up":
            status_text = "↑"
        elif self.gravity == "down":
            status_text = "↓"
        if self.gravity == "left":
            status_text = "←"
        elif self.gravity == "right":
            status_text = "→"

        if self.attractor in ['attract', 'repel']:
            mouse_screen_pos = pygame.mouse.get_pos()
            color = (0, 255, 0) if self.attractor == 'attract' else (255, 50, 50)
            pygame.draw.circle(surface, color, mouse_screen_pos, 15, 2)

        if self.gravity_enabled == True:
            status_surface = arrow_font.render(status_text, True, (255, 255, 255))
        else:
            status_surface = arrow_font.render(status_text, True, (255, 69, 50))

        surface.blit(status_surface, (WIDTH - 35, 5))
        text_surface = font.render(f"Particles: {len(self.particles)}", True, (255, 255, 255))
        surface.blit(text_surface, (10, 10))

        for p in self.particles:
            speed = np.linalg.norm(p.velocity)
            t = min(speed / 200, 1.0)
            rgba = self.cmap(t)
            rgb = tuple(int(255 * c) for c in rgba[:3])

            screen_pos = (pygame.Vector2(p.position) - camera_offset) * zoom_level
            pygame.draw.circle(surface, rgb, screen_pos, p.radius * zoom_level)