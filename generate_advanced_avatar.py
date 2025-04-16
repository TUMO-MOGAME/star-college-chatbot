"""
Generate an advanced realistic avatar using matplotlib and mplsoccer
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle, Arc, PathPatch, FancyBboxPatch
from matplotlib.path import Path
import matplotlib.colors as mcolors
from mplsoccer.pitch import Pitch
from mplsoccer.utils import FontManager
import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap

def generate_advanced_avatar(output_path, size=(600, 600), dpi=100):
    """
    Generate an advanced realistic avatar using matplotlib and mplsoccer

    Args:
        output_path: Path to save the avatar image
        size: Size of the avatar image (width, height)
        dpi: DPI of the avatar image
    """
    # Calculate figure size in inches
    fig_width = size[0] / dpi
    fig_height = size[1] / dpi

    # Create figure with a specific aspect ratio
    fig = plt.figure(figsize=(fig_width, fig_height), dpi=dpi, facecolor='#1a3c8a')

    # Create a custom axis instead of using mplsoccer's Pitch
    ax = fig.add_subplot(111)
    ax.set_facecolor('#1a3c8a')

    # Create a circular border
    circle_border = Circle((0, 0), 0.9, facecolor='#1a3c8a', edgecolor='#c8a415',
                          linewidth=3, zorder=1)
    ax.add_patch(circle_border)

    # Set up the background
    # Create a radial gradient for the background
    n = 100
    r = np.linspace(0, 1, n)
    theta = np.linspace(0, 2*np.pi, n)
    r_grid, theta_grid = np.meshgrid(r, theta)

    # Convert polar coordinates to Cartesian
    x = r_grid * np.cos(theta_grid)
    y = r_grid * np.sin(theta_grid)

    # Create a custom colormap for the face
    face_colors = [(0.96, 0.84, 0.65, 1), (0.94, 0.82, 0.63, 1)]  # Skin tone gradient
    face_cmap = LinearSegmentedColormap.from_list("face_cmap", face_colors)

    # Draw the face
    face = Circle((0, 0), 0.7, facecolor='#f5d6a7', edgecolor='#e8c591',
                 linewidth=2, zorder=3, alpha=1)
    ax.add_patch(face)

    # Add facial features

    # Eyes with more detail
    # Left eye
    eye_left_outer = Ellipse((-0.25, 0.1), 0.25, 0.15, facecolor='white',
                           edgecolor='#555555', linewidth=1, zorder=4)
    ax.add_patch(eye_left_outer)

    # Eye detail
    eye_left_iris = Circle((-0.25, 0.1), 0.08, facecolor='#5b7aa9',
                         edgecolor='#333333', linewidth=0.5, zorder=5)
    ax.add_patch(eye_left_iris)

    eye_left_pupil = Circle((-0.25, 0.1), 0.04, facecolor='#222222', zorder=6)
    ax.add_patch(eye_left_pupil)

    eye_left_highlight = Circle((-0.28, 0.13), 0.02, facecolor='white', zorder=7)
    ax.add_patch(eye_left_highlight)

    # Right eye
    eye_right_outer = Ellipse((0.25, 0.1), 0.25, 0.15, facecolor='white',
                            edgecolor='#555555', linewidth=1, zorder=4)
    ax.add_patch(eye_right_outer)

    # Eye detail
    eye_right_iris = Circle((0.25, 0.1), 0.08, facecolor='#5b7aa9',
                          edgecolor='#333333', linewidth=0.5, zorder=5)
    ax.add_patch(eye_right_iris)

    eye_right_pupil = Circle((0.25, 0.1), 0.04, facecolor='#222222', zorder=6)
    ax.add_patch(eye_right_pupil)

    eye_right_highlight = Circle((0.22, 0.13), 0.02, facecolor='white', zorder=7)
    ax.add_patch(eye_right_highlight)

    # Eyebrows with more natural shape
    # Left eyebrow
    eyebrow_left_verts = [
        (-0.4, 0.25), (-0.35, 0.28), (-0.25, 0.3), (-0.15, 0.28), (-0.1, 0.25)
    ]
    eyebrow_left_codes = [Path.MOVETO] + [Path.CURVE4] * (len(eyebrow_left_verts) - 1)
    eyebrow_left_path = Path(eyebrow_left_verts, eyebrow_left_codes)
    eyebrow_left = PathPatch(eyebrow_left_path, facecolor='none', edgecolor='#333333',
                           linewidth=3, zorder=4)
    ax.add_patch(eyebrow_left)

    # Right eyebrow
    eyebrow_right_verts = [
        (0.1, 0.25), (0.15, 0.28), (0.25, 0.3), (0.35, 0.28), (0.4, 0.25)
    ]
    eyebrow_right_codes = [Path.MOVETO] + [Path.CURVE4] * (len(eyebrow_right_verts) - 1)
    eyebrow_right_path = Path(eyebrow_right_verts, eyebrow_right_codes)
    eyebrow_right = PathPatch(eyebrow_right_path, facecolor='none', edgecolor='#333333',
                            linewidth=3, zorder=4)
    ax.add_patch(eyebrow_right)

    # Nose with more detail
    nose_bridge = plt.Line2D([0, 0], [0.1, -0.1], color='#555555', linewidth=1.5, zorder=4)
    ax.add_line(nose_bridge)

    # Nose tip and nostrils
    nose_tip_verts = [
        (0, -0.1), (0.05, -0.15), (0, -0.2), (-0.05, -0.15), (0, -0.1)
    ]
    nose_tip_codes = [Path.MOVETO] + [Path.CURVE4] * (len(nose_tip_verts) - 1)
    nose_tip_path = Path(nose_tip_verts, nose_tip_codes)
    nose_tip = PathPatch(nose_tip_path, facecolor='#f5d6a7', edgecolor='#555555',
                       linewidth=1, zorder=4)
    ax.add_patch(nose_tip)

    # Mouth with more detail - slight smile
    mouth_verts = [
        (-0.3, -0.3), (-0.15, -0.35), (0, -0.33), (0.15, -0.35), (0.3, -0.3),
        (0.25, -0.28), (0, -0.25), (-0.25, -0.28), (-0.3, -0.3)
    ]
    mouth_codes = [Path.MOVETO] + [Path.CURVE4] * (len(mouth_verts) - 2) + [Path.CLOSEPOLY]
    mouth_path = Path(mouth_verts, mouth_codes)
    mouth = PathPatch(mouth_path, facecolor='#e88a88', edgecolor='#333333',
                    linewidth=1, zorder=4, alpha=0.8)
    ax.add_patch(mouth)

    # Add more realistic hair
    # Hair color
    hair_color = '#222222'

    # Top hair with texture
    for i in range(20):
        hair_x = 0.1 * np.random.randn()
        hair_y = 0.5 + 0.1 * np.random.randn()
        hair_width = 0.8 + 0.2 * np.random.randn()
        hair_height = 0.4 + 0.1 * np.random.randn()
        hair_piece = Ellipse((hair_x, hair_y), hair_width, hair_height,
                           facecolor=hair_color, edgecolor='none', zorder=2, alpha=0.9)
        ax.add_patch(hair_piece)

    # Side hair
    for i in range(10):
        side = 1 if i % 2 == 0 else -1
        hair_x = side * (0.5 + 0.1 * np.random.randn())
        hair_y = 0.1 + 0.2 * np.random.randn()
        hair_width = 0.3 + 0.1 * np.random.randn()
        hair_height = 0.6 + 0.2 * np.random.randn()
        hair_piece = Ellipse((hair_x, hair_y), hair_width, hair_height,
                           facecolor=hair_color, edgecolor='none', zorder=2, alpha=0.9)
        ax.add_patch(hair_piece)

    # Add ears
    ear_left = Ellipse((-0.75, 0), 0.1, 0.2, facecolor='#f5d6a7',
                      edgecolor='#e8c591', linewidth=1, zorder=2.5)
    ax.add_patch(ear_left)

    ear_right = Ellipse((0.75, 0), 0.1, 0.2, facecolor='#f5d6a7',
                       edgecolor='#e8c591', linewidth=1, zorder=2.5)
    ax.add_patch(ear_right)

    # Add a Star College emblem/badge
    # Create a star shape
    star_points = 5
    star_outer_radius = 0.15
    star_inner_radius = star_outer_radius * 0.4
    star_center = (0, -0.6)

    theta = np.linspace(0, 2 * np.pi, 2 * star_points + 1)[:-1]
    radius = np.ones_like(theta)
    radius[1::2] = star_inner_radius / star_outer_radius

    x = star_center[0] + star_outer_radius * radius * np.sin(theta)
    y = star_center[1] + star_outer_radius * radius * np.cos(theta)

    star = plt.Polygon(np.column_stack([x, y]), closed=True, facecolor='#c8a415',
                      edgecolor='#1a3c8a', linewidth=2, zorder=8)
    ax.add_patch(star)

    # Add "StarBot" text using mplsoccer's FontManager
    # Try to use a nice font if available
    try:
        font_normal = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/'
                                'src/hinted/Roboto-Regular.ttf')
        font_bold = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/'
                              'src/hinted/Roboto-Bold.ttf')
    except:
        # Fall back to default font
        font_normal = None
        font_bold = None

    # Add text
    if font_bold:
        text = ax.text(0, -0.85, "StarBot", fontproperties=font_bold.prop,
                      ha='center', va='center', fontsize=24, color='white', zorder=9)
    else:
        text = ax.text(0, -0.85, "StarBot", ha='center', va='center',
                      fontsize=24, fontweight='bold', color='white', zorder=9)

    # Add a subtle shadow effect to the text
    text.set_path_effects([path_effects.withStroke(linewidth=4, foreground='#1a3c8a')])

    # Set axis limits
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.axis('off')

    # Save the figure
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    print(f"Advanced avatar saved to {output_path}")

def main():
    """
    Generate an advanced avatar
    """
    output_path = "static/images/advanced_avatar.png"
    generate_advanced_avatar(output_path)

    # Also save as avatar.png for the chatbot to use
    avatar_path = "static/images/avatar.png"
    generate_advanced_avatar(avatar_path)

if __name__ == "__main__":
    main()
