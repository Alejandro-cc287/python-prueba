import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Ellipse
import math
import random

class FlowerAnimation:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 10), facecolor='black')
        self.ax.set_facecolor('#001122')  
        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-6, 10)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.petal_colors = ['#FF69B4', '#FF1493', '#DC143C', '#B22222', '#FF6347']
        self.leaf_color = '#228B22'
        self.stem_color = '#32CD32'
        self.center_color = '#FFD700'
        self.petals = []
        self.leaves = []
        self.stem_parts = []
        self.sparkles = []
        
    def create_heart_petal(self, center_x, center_y, size, angle, color):
        """Crea un pétalo en forma de corazón"""
        t = np.linspace(0, 2*np.pi, 100)
        x = size * (16 * np.sin(t)**3)
        y = size * (13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t))
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        x_rot = x * cos_a - y * sin_a + center_x
        y_rot = x * sin_a + y * cos_a + center_y
        
        return x_rot, y_rot
    
    def create_rose_petal(self, center_x, center_y, size, angle, color):
        """Crea un pétalo de rosa más realista"""
        t = np.linspace(0, np.pi, 50)
        r = size * (1 + 0.3 * np.cos(3*t)) * np.sin(t)
        x = r * np.cos(t + angle) + center_x
        y = r * np.sin(t + angle) + center_y
        
        return x, y
    
    def create_sparkle(self, x, y, size=0.1):
        """Crea una estrellita brillante"""
        angles = np.linspace(0, 2*np.pi, 8)
        outer_r = size
        inner_r = size * 0.4
        
        points_x, points_y = [], []
        for i, angle in enumerate(angles):
            r = outer_r if i % 2 == 0 else inner_r
            points_x.append(x + r * np.cos(angle))
            points_y.append(y + r * np.sin(angle))
            
        return points_x, points_y
    
    def animate_flower(self, frame):
        """Función principal de animación"""
        self.ax.clear()
        self.ax.set_facecolor('#001122')
        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-6, 10)
        self.ax.axis('off')
        
        if frame >= 0:
            stem_height = min(frame / 30.0, 1.0) * 6
            self.ax.plot([0, 0], [-6, -6 + stem_height], 
                        color=self.stem_color, linewidth=8, alpha=0.9)
            
            if stem_height > 1:
                for i in range(int(stem_height)):
                    y_pos = -6 + i + 0.5
                    self.ax.plot([-0.1, 0.1], [y_pos, y_pos], 
                               color='#228B22', linewidth=2, alpha=0.7)
        
        if frame >= 20:
            leaf_progress = min((frame - 20) / 30.0, 1.0)
            
            if leaf_progress > 0:
                leaf_size = leaf_progress * 1.5
                t = np.linspace(0, np.pi, 30)
                leaf_x = -leaf_size * np.cos(t) - 2
                leaf_y = leaf_size * np.sin(t) - 2
                self.ax.fill(leaf_x, leaf_y, color=self.leaf_color, alpha=0.8)
                self.ax.plot([-2, 0], [-2, -1], color='#228B22', linewidth=3)
            
            if leaf_progress > 0.5:
                leaf_size = (leaf_progress - 0.5) * 3
                t = np.linspace(0, np.pi, 30)
                leaf_x = leaf_size * np.cos(t) + 1.5
                leaf_y = leaf_size * np.sin(t) - 3
                self.ax.fill(leaf_x, leaf_y, color=self.leaf_color, alpha=0.8)
                self.ax.plot([1.5, 0], [-3, -2], color='#228B22', linewidth=3)
        
        if frame >= 40:
            petal_progress = min((frame - 40) / 60.0, 1.0)
            center_x, center_y = 0, 0
            
            for layer in range(3):
                num_petals = 6 + layer * 2
                radius = 2 - layer * 0.3
                
                for i in range(num_petals):
                    if petal_progress > i / num_petals:
                        angle = (2 * np.pi * i / num_petals) + layer * 0.2
                        petal_x = center_x + radius * np.cos(angle) * 0.7
                        petal_y = center_y + radius * np.sin(angle) * 0.7
                        
                        px, py = self.create_heart_petal(petal_x, petal_y, 
                                                       0.15 * (1.2 - layer * 0.2), 
                                                       angle, self.petal_colors[layer])
                        
                        alpha = 0.9 - layer * 0.1
                        self.ax.fill(px, py, color=self.petal_colors[layer], 
                                   alpha=alpha, edgecolor='white', linewidth=0.5)
            
            if petal_progress > 0.8:
                center_size = (petal_progress - 0.8) * 5 * 0.5
                circle = Circle((center_x, center_y), center_size, 
                              color=self.center_color, alpha=0.9)
                self.ax.add_patch(circle)
                
                if center_size > 0.15:
                    for i in range(8):
                        angle = i * np.pi / 4
                        dot_x = center_x + 0.1 * np.cos(angle)
                        dot_y = center_y + 0.1 * np.sin(angle)
                        self.ax.plot(dot_x, dot_y, 'o', color='#FF8C00', markersize=3)
        
        if frame >= 80:
            magic_progress = (frame - 80) / 100.0
            
            num_sparkles = min(int(magic_progress * 20), 20)
            for i in range(num_sparkles):
                angle = (frame + i * 30) * 0.1
                distance = 3 + 1.5 * np.sin((frame + i * 20) * 0.05)
                spark_x = distance * np.cos(angle)
                spark_y = distance * np.sin(angle) + 1
                
                spark_px, spark_py = self.create_sparkle(spark_x, spark_y, 0.15)
                color = random.choice(['#FFD700', '#FFFFFF', '#FF69B4', '#00FFFF'])
                self.ax.fill(spark_px, spark_py, color=color, alpha=0.8)
        

        
        if frame >= 60:
            for i in range(15):
                star_x = -7 + (i * 14 / 15)
                star_y = 8 + 1.5 * np.sin((frame + i * 30) * 0.1)
                brightness = 0.5 + 0.5 * np.sin((frame + i * 20) * 0.15)
                self.ax.plot(star_x, star_y, '*', color='white', 
                           markersize=8, alpha=brightness)
        
        if frame < 200:
            progress = min(frame / 200.0 * 100, 100)
            self.ax.text(-7.5, -5.5, f"Creciendo... {progress:.0f}%", 
                        color='white', fontsize=10, alpha=0.7)
    
    def start_animation(self):
        """Inicia la animación completa"""
        ani = animation.FuncAnimation(self.fig, self.animate_flower, 
                                    frames=250, interval=100, repeat=True)
        return ani


def main():
    """Función principal"""
    print("🌹 Animación de Flor Creciendo")
    print("=" * 40)
    
    animator = FlowerAnimation()
    
    print("🌹 Creando una hermosa flor...")
    print("\n✨ La animación incluye:")
    print("- Tallo creciendo desde la raíz")
    print("- Hojas brotando a los lados")
    print("- Pétalos floreciendo en capas")
    print("- Efectos mágicos y brillos")
    print("- Estrellas parpadeantes de fondo")
    print("\n🎬 ¡Disfruta la animación!")
    
    try:
        ani = animator.start_animation()
        plt.tight_layout()
        plt.show()
        
    except KeyboardInterrupt:
        print("\n🌹 ¡Animación finalizada!")
    except Exception as e:
        print(f"⚠️ Error: {e}")
        print("Asegúrate de tener matplotlib instalado: pip install matplotlib numpy")


if __name__ == "__main__":
    main()      