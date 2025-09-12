import pygame
import numpy as np
import matplotlib.pyplot as plt

class WaveSim:
    def __init__(self, screen_width, screen_height, Nx, Ny, dt, c):
        self.Lx = screen_width
        self.Ly = screen_height
        self.Nx = Nx
        self.Ny = Ny
        self.dt = dt
        self.dx = self.Lx / (self.Nx - 1)
        self.dy = self.Ly / (self.Ny - 1)
        self.c = c
        self.damping = 0.999

        self.u = np.zeros((self.Nx, self.Ny))       
        self.u_prev = np.zeros((self.Nx, self.Ny)) 
        self.boundaries = np.zeros((self.Nx, self.Ny)) 

        self.cmap = plt.get_cmap('seismic') 
        self.pause = False
        self.amp = 1.0 

    def interact(self, mouse_pos, width, height):
        i = int(mouse_pos[0] / (width / self.Nx))    
        j = int(mouse_pos[1] / (height / self.Ny))  
        if 0 <= i < self.Ny and 0 <= j < self.Nx and self.boundaries[j, i] == 0:
            self.u[j, i] = self.amp  

    def boundary(self, mouse_pos, width, height):
        i = int(mouse_pos[0] / (width / self.Nx))
        j = int(mouse_pos[1] / (height / self.Ny))
        if 0 <= i < self.Ny and 0 <= j < self.Nx:
            if self.boundaries[j, i] == 1:
                self.boundaries[j, i] = 0
            else:
                self.boundaries[j, i] = 1
                self.u[j, i] = 0
                self.u_prev[j, i] = 0

    def pause_sim(self):
        self.pause = not self.pause

    def update(self):
        if self.pause == False:
            u_new = np.zeros_like(self.u)
            u_new[1:-1, 1:-1] = (2 * self.u[1:-1, 1:-1] - self.u_prev[1:-1, 1:-1] + (self.c * self.dt) ** 2 * ((self.u[2:, 1:-1] - 2 * self.u[1:-1, 1:-1] + self.u[:-2, 1:-1]) / self.dx ** 2 + (self.u[1:-1, 2:] - 2 * self.u[1:-1, 1:-1] + self.u[1:-1, :-2]) / self.dy ** 2))
            u_new *= self.damping
            u_new[self.boundaries == 1] = 0
            self.u_prev = self.u
            self.u = u_new

    def draw(self, surface):
        width = surface.get_width()
        height = surface.get_height()
        max_amp = self.amp
        norm_field = (self.u + max_amp) / (2 * max_amp)
        norm_field = np.clip(norm_field, 0.0, 1.0)
        color_data = self.cmap(norm_field)[..., :3] * 255
        color_data = color_data.astype(np.uint8)
        surf = pygame.surfarray.make_surface(np.transpose(color_data, (1, 0, 2)))
        surf = pygame.transform.scale(surf, (width, height))
        surface.blit(surf, (0, 0))