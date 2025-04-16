"""
Generate a more realistic avatar using matplotlib and mplsoccer
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle, Arc, PathPatch
from matplotlib.path import Path
import matplotlib.colors as mcolors
from mplsoccer.pitch import Pitch
import matplotlib.patheffects as path_effects

def generate_realistic_avatar(output_path, size=(600, 600), dpi=100):
    """
    Generate a more realistic avatar using matplotlib and mplsoccer
    
    Args:
        output_path: Path to save the avatar image
        size: Size of the avatar image (width, height)
        dpi: DPI of the avatar image
    """
    # Calculate figure size in inches
    fig_width = size[0] / dpi
    fig_height = size[1] / dpi
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)
    
    # Set background color
    fig.patch.set_facecolor('#1a3c8a')  # Star College blue
    
    # Create a circular background
    circle_bg = Circle((0.5, 0.5), 0.45, transform=ax.transAxes, 
                      facecolor='#1a3c8a', edgecolor='#c8a415', linewidth=3, 
                      zorder=1, alpha=1)
    ax.add_patch(circle_bg)
    
    # Add a gradient effect to the background
    gradient = np.linspace(0, 1, 100).reshape(1, -1)
    gradient = np.vstack((gradient, gradient))
    
    # Create a radial gradient for the face
    x = np.linspace(-1, 1, 100)
    y = np.linspace(-1, 1, 100)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    face_gradient = 1 - np.clip(R, 0, 1)
    
    # Create face
    face = Circle((0.5, 0.5), 0.35, transform=ax.transAxes, 
                 facecolor='#f5d6a7', edgecolor='#e8c591', linewidth=1.5, 
                 zorder=2, alpha=1)
    ax.add_patch(face)
    
    # Add facial features
    
    # Eyes
    # Left eye
    eye_left = Ellipse((0.4, 0.55), 0.1, 0.15, transform=ax.transAxes, 
                      facecolor='white', edgecolor='#555555', linewidth=1, 
                      zorder=3)
    ax.add_patch(eye_left)
    
    # Right eye
    eye_right = Ellipse((0.6, 0.55), 0.1, 0.15, transform=ax.transAxes, 
                       facecolor='white', edgecolor='#555555', linewidth=1, 
                       zorder=3)
    ax.add_patch(eye_right)
    
    # Pupils
    pupil_left = Circle((0.4, 0.55), 0.03, transform=ax.transAxes, 
                       facecolor='#222222', zorder=4)
    ax.add_patch(pupil_left)
    
    pupil_right = Circle((0.6, 0.55), 0.03, transform=ax.transAxes, 
                        facecolor='#222222', zorder=4)
    ax.add_patch(pupil_right)
    
    # Eyebrows
    eyebrow_left = Arc((0.4, 0.62), 0.15, 0.1, theta1=180, theta2=360, 
                      transform=ax.transAxes, linewidth=2, color='#333333', zorder=3)
    ax.add_patch(eyebrow_left)
    
    eyebrow_right = Arc((0.6, 0.62), 0.15, 0.1, theta1=180, theta2=360, 
                       transform=ax.transAxes, linewidth=2, color='#333333', zorder=3)
    ax.add_patch(eyebrow_right)
    
    # Nose
    nose_line = plt.Line2D([0.5, 0.5], [0.55, 0.45], transform=ax.transAxes, 
                          color='#555555', linewidth=1.5, zorder=3)
    ax.add_line(nose_line)
    
    nose_base = Arc((0.5, 0.45), 0.1, 0.05, theta1=0, theta2=180, 
                   transform=ax.transAxes, linewidth=1.5, color='#555555', zorder=3)
    ax.add_patch(nose_base)
    
    # Mouth - smiling
    mouth = Arc((0.5, 0.35), 0.2, 0.1, theta1=0, theta2=180, 
               transform=ax.transAxes, linewidth=2, color='#333333', zorder=3)
    ax.add_patch(mouth)
    
    # Hair
    # Create a more realistic hairstyle
    hair_color = '#222222'
    
    # Top hair
    hair_top = Ellipse((0.5, 0.75), 0.5, 0.3, transform=ax.transAxes, 
                      facecolor=hair_color, edgecolor='none', zorder=1.5)
    ax.add_patch(hair_top)
    
    # Side hair - left
    hair_left = Ellipse((0.3, 0.55), 0.15, 0.3, transform=ax.transAxes, 
                       facecolor=hair_color, edgecolor='none', zorder=1.5)
    ax.add_patch(hair_left)
    
    # Side hair - right
    hair_right = Ellipse((0.7, 0.55), 0.15, 0.3, transform=ax.transAxes, 
                        facecolor=hair_color, edgecolor='none', zorder=1.5)
    ax.add_patch(hair_right)
    
    # Add ears
    ear_left = Ellipse((0.25, 0.5), 0.05, 0.1, transform=ax.transAxes, 
                      facecolor='#f5d6a7', edgecolor='#e8c591', linewidth=1, 
                      zorder=1.8)
    ax.add_patch(ear_left)
    
    ear_right = Ellipse((0.75, 0.5), 0.05, 0.1, transform=ax.transAxes, 
                       facecolor='#f5d6a7', edgecolor='#e8c591', linewidth=1, 
                       zorder=1.8)
    ax.add_patch(ear_right)
    
    # Add a Star College emblem
    star_points = 5
    star_outer_radius = 0.05
    star_inner_radius = star_outer_radius * 0.4
    star_center = (0.5, 0.2)
    
    theta = np.linspace(0, 2 * np.pi, 2 * star_points + 1)[:-1]
    radius = np.ones_like(theta)
    radius[1::2] = star_inner_radius / star_outer_radius
    
    x = star_center[0] + star_outer_radius * radius * np.sin(theta)
    y = star_center[1] + star_outer_radius * radius * np.cos(theta)
    
    star = plt.Polygon(np.column_stack([x, y]), transform=ax.transAxes, 
                      closed=True, facecolor='#c8a415', edgecolor='#1a3c8a', 
                      linewidth=1, zorder=5)
    ax.add_patch(star)
    
    # Add "StarBot" text
    text = ax.text(0.5, 0.08, "StarBot", transform=ax.transAxes, 
                  ha='center', va='center', fontsize=16, fontweight='bold', 
                  color='white', zorder=5)
    
    # Add a subtle shadow effect to the text
    text.set_path_effects([path_effects.withStroke(linewidth=3, foreground='#1a3c8a')])
    
    # Remove axis
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Save the figure
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    
    print(f"Realistic avatar saved to {output_path}")

def main():
    """
    Generate a realistic avatar
    """
    output_path = "static/images/realistic_avatar.png"
    generate_realistic_avatar(output_path)
    
    # Also save as avatar.png for the chatbot to use
    avatar_path = "static/images/avatar.png"
    generate_realistic_avatar(avatar_path)

if __name__ == "__main__":
    main()
