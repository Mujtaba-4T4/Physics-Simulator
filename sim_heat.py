import pygame
import numpy as np
import matplotlib.pyplot as plt

class HeatSim:
    def __init__(self, screen_width, screen_height, Nx, Ny, dt, alpha):
        self.Lx = screen_width
        self.Ly = screen_height
        self.Nx = Nx
        self.Ny = Ny
        self.dt = dt
        self.dx = self.Lx / (self.Nx - 1)
        self.dy = self.Ly / (self.Ny - 1)
        self.alpha = alpha

        self.u = np.zeros((self.Nx, self.Ny))        
        self.boundaries = np.zeros((self.Nx, self.Ny))  

        self.cmap = plt.get_cmap('hot')
        self.temp = 1.0  
        self.pause = False

    def heat(self, mouse_pos, width, height):
        i = int(mouse_pos[0] / (width / self.Nx))   
        j = int(mouse_pos[1] / (height / self.Ny))  

        if 0 <= i < self.Ny and 0 <= j < self.Nx and self.boundaries[j, i] == 0:
            self.u[j, i] = self.temp

    def boundary(self, mouse_pos, width, height):
        i = int(mouse_pos[0] / (width / self.Nx))  
        j = int(mouse_pos[1] / (height / self.Ny)) 

        if 0 <= i < self.Ny and 0 <= j < self.Nx:
            if self.boundaries[j, i] == 1:
                self.boundaries[j, i] = 0
            else:
                self.boundaries[j, i] = 1
                self.u[j, i] = 0

    def pause_sim(self):
        if self.pause == True:
            self.pause = False
        elif self.pause == False:
            self.pause = True

    def update(self):
        if self.pause == False:
            u_new = self.u.copy()
            u_new[1:-1, 1:-1] = self.u[1:-1, 1:-1] + self.alpha * self.dt * ((self.u[2:, 1:-1] - 2 * self.u[1:-1, 1:-1] + self.u[:-2, 1:-1]) / self.dx**2 + (self.u[1:-1, 2:] - 2 * self.u[1:-1, 1:-1] + self.u[1:-1, :-2]) / self.dy**2)
            boundary_indices = np.where(self.boundaries == 1)
            u_new[boundary_indices] = self.u[boundary_indices]
            self.u = u_new

    def draw(self, surface):
        width = surface.get_width()
        height = surface.get_height()
        norm_temp = np.clip(self.u, 0.0, 1.0) * 255
        color_data = self.cmap(norm_temp / 255.0)[..., :3] * 255
        surf = pygame.surfarray.make_surface(np.transpose(color_data, (1, 0, 2)))
        surf = pygame.transform.scale(surf, (width, height))
        surface.blit(surf, (0, 0))