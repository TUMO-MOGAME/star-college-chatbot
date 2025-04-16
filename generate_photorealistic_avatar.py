"""
Generate a photorealistic avatar using matplotlib and mplsoccer
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle, Arc, PathPatch, FancyBboxPatch, Wedge
from matplotlib.path import Path
import matplotlib.colors as mcolors
from mplsoccer.pitch import Pitch
from mplsoccer.utils import FontManager
import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec

def generate_photorealistic_avatar(output_path, size=(600, 600), dpi=100):
    """
    Generate a photorealistic avatar using matplotlib and mplsoccer
    
    Args:
        output_path: Path to save the avatar image
        size: Size of the avatar image (width, height)
        dpi: DPI of the avatar image
    """
    # Calculate figure size in inches
    fig_width = size[0] / dpi
    fig_height = size[1] / dpi
    
    # Create figure with a specific aspect ratio
    fig = plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
    
    # Create a grid layout
    gs = gridspec.GridSpec(1, 1, figure=fig)
    ax = fig.add_subplot(gs[0, 0])
    
    # Set background
    ax.set_facecolor('#1a3c8a')
    fig.patch.set_facecolor('#1a3c8a')
    
    # Create a circular border with gold trim
    border_outer = Circle((0.5, 0.5), 0.48, transform=ax.transAxes, 
                         facecolor='none', edgecolor='#c8a415', linewidth=5, 
                         zorder=10, alpha=1)
    ax.add_patch(border_outer)
    
    border_inner = Circle((0.5, 0.5), 0.47, transform=ax.transAxes, 
                         facecolor='none', edgecolor='#1a3c8a', linewidth=3, 
                         zorder=11, alpha=1)
    ax.add_patch(border_inner)
    
    # Create a more realistic face shape
    # Base face shape
    face_color = '#f5d6a7'  # Base skin tone
    face_outline = '#e8c591'  # Slightly darker for outline
    
    # Main face shape
    face = Ellipse((0.5, 0.5), 0.7, 0.85, transform=ax.transAxes, 
                  facecolor=face_color, edgecolor=face_outline, 
                  linewidth=1.5, zorder=2, alpha=1)
    ax.add_patch(face)
    
    # Add jaw definition
    jaw_left = Wedge((0.35, 0.3), 0.25, 180, 270, transform=ax.transAxes, 
                    width=0.02, facecolor=face_outline, edgecolor=face_outline, 
                    linewidth=0, zorder=2.1, alpha=0.5)
    ax.add_patch(jaw_left)
    
    jaw_right = Wedge((0.65, 0.3), 0.25, 270, 360, transform=ax.transAxes, 
                     width=0.02, facecolor=face_outline, edgecolor=face_outline, 
                     linewidth=0, zorder=2.1, alpha=0.5)
    ax.add_patch(jaw_right)
    
    # Add cheekbones
    cheek_left = Circle((0.35, 0.45), 0.08, transform=ax.transAxes, 
                       facecolor='#f7c4c4', edgecolor='none', 
                       linewidth=0, zorder=2.2, alpha=0.3)
    ax.add_patch(cheek_left)
    
    cheek_right = Circle((0.65, 0.45), 0.08, transform=ax.transAxes, 
                        facecolor='#f7c4c4', edgecolor='none', 
                        linewidth=0, zorder=2.2, alpha=0.3)
    ax.add_patch(cheek_right)
    
    # Add facial features
    
    # Eyes with realistic detail
    # Left eye
    eye_left_shape = Ellipse((0.35, 0.58), 0.12, 0.05, transform=ax.transAxes, 
                            facecolor='white', edgecolor='#555555', 
                            linewidth=1, zorder=3)
    ax.add_patch(eye_left_shape)
    
    # Eye details
    eye_left_iris = Circle((0.35, 0.58), 0.03, transform=ax.transAxes, 
                          facecolor='#5b7aa9', edgecolor='#333333', 
                          linewidth=0.5, zorder=3.1)
    ax.add_patch(eye_left_iris)
    
    eye_left_pupil = Circle((0.35, 0.58), 0.015, transform=ax.transAxes, 
                           facecolor='#222222', zorder=3.2)
    ax.add_patch(eye_left_pupil)
    
    eye_left_highlight = Circle((0.345, 0.585), 0.005, transform=ax.transAxes, 
                               facecolor='white', zorder=3.3)
    ax.add_patch(eye_left_highlight)
    
    # Eyelids
    eye_left_lid = Arc((0.35, 0.58), 0.12, 0.05, theta1=0, theta2=180, 
                      transform=ax.transAxes, linewidth=1.5, color='#555555', zorder=3.4)
    ax.add_patch(eye_left_lid)
    
    eye_left_lower_lid = Arc((0.35, 0.58), 0.12, 0.03, theta1=180, theta2=360, 
                            transform=ax.transAxes, linewidth=1, color='#555555', zorder=3.4)
    ax.add_patch(eye_left_lower_lid)
    
    # Right eye
    eye_right_shape = Ellipse((0.65, 0.58), 0.12, 0.05, transform=ax.transAxes, 
                             facecolor='white', edgecolor='#555555', 
                             linewidth=1, zorder=3)
    ax.add_patch(eye_right_shape)
    
    # Eye details
    eye_right_iris = Circle((0.65, 0.58), 0.03, transform=ax.transAxes, 
                           facecolor='#5b7aa9', edgecolor='#333333', 
                           linewidth=0.5, zorder=3.1)
    ax.add_patch(eye_right_iris)
    
    eye_right_pupil = Circle((0.65, 0.58), 0.015, transform=ax.transAxes, 
                            facecolor='#222222', zorder=3.2)
    ax.add_patch(eye_right_pupil)
    
    eye_right_highlight = Circle((0.645, 0.585), 0.005, transform=ax.transAxes, 
                                facecolor='white', zorder=3.3)
    ax.add_patch(eye_right_highlight)
    
    # Eyelids
    eye_right_lid = Arc((0.65, 0.58), 0.12, 0.05, theta1=0, theta2=180, 
                       transform=ax.transAxes, linewidth=1.5, color='#555555', zorder=3.4)
    ax.add_patch(eye_right_lid)
    
    eye_right_lower_lid = Arc((0.65, 0.58), 0.12, 0.03, theta1=180, theta2=360, 
                             transform=ax.transAxes, linewidth=1, color='#555555', zorder=3.4)
    ax.add_patch(eye_right_lower_lid)
    
    # Eyebrows with natural shape
    # Left eyebrow
    eyebrow_left_verts = [
        (0.25, 0.64), (0.3, 0.65), (0.35, 0.655), (0.4, 0.65), (0.45, 0.64)
    ]
    eyebrow_left_codes = [Path.MOVETO] + [Path.CURVE4] * (len(eyebrow_left_verts) - 1)
    eyebrow_left_path = Path(eyebrow_left_verts, eyebrow_left_codes)
    eyebrow_left = PathPatch(eyebrow_left_path, transform=ax.transAxes, 
                            facecolor='none', edgecolor='#333333', 
                            linewidth=2, zorder=3.5)
    ax.add_patch(eyebrow_left)
    
    # Right eyebrow
    eyebrow_right_verts = [
        (0.55, 0.64), (0.6, 0.65), (0.65, 0.655), (0.7, 0.65), (0.75, 0.64)
    ]
    eyebrow_right_codes = [Path.MOVETO] + [Path.CURVE4] * (len(eyebrow_right_verts) - 1)
    eyebrow_right_path = Path(eyebrow_right_verts, eyebrow_right_codes)
    eyebrow_right = PathPatch(eyebrow_right_path, transform=ax.transAxes, 
                             facecolor='none', edgecolor='#333333', 
                             linewidth=2, zorder=3.5)
    ax.add_patch(eyebrow_right)
    
    # Nose with realistic shape
    # Bridge
    nose_bridge = plt.Line2D([0.5, 0.5], [0.58, 0.45], transform=ax.transAxes, 
                            color='#555555', linewidth=1, zorder=3.6)
    ax.add_line(nose_bridge)
    
    # Nose tip and nostrils
    nose_tip_verts = [
        (0.47, 0.45), (0.5, 0.43), (0.53, 0.45), (0.51, 0.46), (0.49, 0.46), (0.47, 0.45)
    ]
    nose_tip_codes = [Path.MOVETO] + [Path.CURVE4] * (len(nose_tip_verts) - 2) + [Path.CLOSEPOLY]
    nose_tip_path = Path(nose_tip_verts, nose_tip_codes)
    nose_tip = PathPatch(nose_tip_path, transform=ax.transAxes, 
                        facecolor=face_color, edgecolor='#555555', 
                        linewidth=1, zorder=3.6)
    ax.add_patch(nose_tip)
    
    # Nostrils
    nostril_left = Ellipse((0.48, 0.45), 0.02, 0.01, transform=ax.transAxes, 
                          facecolor='#333333', edgecolor='none', 
                          linewidth=0, zorder=3.7, alpha=0.7)
    ax.add_patch(nostril_left)
    
    nostril_right = Ellipse((0.52, 0.45), 0.02, 0.01, transform=ax.transAxes, 
                           facecolor='#333333', edgecolor='none', 
                           linewidth=0, zorder=3.7, alpha=0.7)
    ax.add_patch(nostril_right)
    
    # Mouth with realistic shape and subtle smile
    # Lips
    lip_upper_verts = [
        (0.4, 0.4), (0.45, 0.41), (0.5, 0.415), (0.55, 0.41), (0.6, 0.4),
        (0.55, 0.395), (0.5, 0.39), (0.45, 0.395), (0.4, 0.4)
    ]
    lip_upper_codes = [Path.MOVETO] + [Path.CURVE4] * (len(lip_upper_verts) - 2) + [Path.CLOSEPOLY]
    lip_upper_path = Path(lip_upper_verts, lip_upper_codes)
    lip_upper = PathPatch(lip_upper_path, transform=ax.transAxes, 
                         facecolor='#e88a88', edgecolor='#333333', 
                         linewidth=0.5, zorder=3.8, alpha=0.8)
    ax.add_patch(lip_upper)
    
    lip_lower_verts = [
        (0.4, 0.4), (0.45, 0.39), (0.5, 0.385), (0.55, 0.39), (0.6, 0.4),
        (0.55, 0.37), (0.5, 0.36), (0.45, 0.37), (0.4, 0.4)
    ]
    lip_lower_codes = [Path.MOVETO] + [Path.CURVE4] * (len(lip_lower_verts) - 2) + [Path.CLOSEPOLY]
    lip_lower_path = Path(lip_lower_verts, lip_lower_codes)
    lip_lower = PathPatch(lip_lower_path, transform=ax.transAxes, 
                         facecolor='#e88a88', edgecolor='#333333', 
                         linewidth=0.5, zorder=3.8, alpha=0.9)
    ax.add_patch(lip_lower)
    
    # Add realistic hair
    hair_color = '#222222'
    
    # Create a hair base
    hair_base = Ellipse((0.5, 0.7), 0.75, 0.5, transform=ax.transAxes, 
                       facecolor=hair_color, edgecolor='none', 
                       linewidth=0, zorder=1.5, alpha=0.95)
    ax.add_patch(hair_base)
    
    # Add hair texture with multiple overlapping shapes
    for i in range(30):
        # Randomize position, size, and opacity for natural look
        hair_x = 0.5 + 0.2 * np.random.randn()
        hair_y = 0.7 + 0.15 * np.random.randn()
        hair_width = 0.1 + 0.05 * np.random.randn()
        hair_height = 0.3 + 0.1 * np.random.randn()
        hair_alpha = 0.7 + 0.3 * np.random.random()
        
        # Create hair strand
        hair_strand = Ellipse((hair_x, hair_y), hair_width, hair_height, 
                             transform=ax.transAxes, facecolor=hair_color, 
                             edgecolor='none', linewidth=0, zorder=1.6, 
                             alpha=hair_alpha)
        ax.add_patch(hair_strand)
    
    # Add side hair
    for i in range(15):
        side = 1 if i % 2 == 0 else -1
        hair_x = 0.5 + side * (0.3 + 0.05 * np.random.randn())
        hair_y = 0.5 + 0.1 * np.random.randn()
        hair_width = 0.15 + 0.05 * np.random.randn()
        hair_height = 0.4 + 0.1 * np.random.randn()
        hair_alpha = 0.7 + 0.3 * np.random.random()
        
        hair_strand = Ellipse((hair_x, hair_y), hair_width, hair_height, 
                             transform=ax.transAxes, facecolor=hair_color, 
                             edgecolor='none', linewidth=0, zorder=1.6, 
                             alpha=hair_alpha)
        ax.add_patch(hair_strand)
    
    # Add ears
    ear_left = Ellipse((0.25, 0.5), 0.05, 0.1, transform=ax.transAxes, 
                      facecolor=face_color, edgecolor=face_outline, 
                      linewidth=1, zorder=1.8)
    ax.add_patch(ear_left)
    
    ear_right = Ellipse((0.75, 0.5), 0.05, 0.1, transform=ax.transAxes, 
                       facecolor=face_color, edgecolor=face_outline, 
                       linewidth=1, zorder=1.8)
    ax.add_patch(ear_right)
    
    # Add a Star College emblem
    # Create a star shape
    star_points = 5
    star_outer_radius = 0.08
    star_inner_radius = star_outer_radius * 0.4
    star_center = (0.5, 0.2)
    
    theta = np.linspace(0, 2 * np.pi, 2 * star_points + 1)[:-1]
    radius = np.ones_like(theta)
    radius[1::2] = star_inner_radius / star_outer_radius
    
    x = star_center[0] + star_outer_radius * radius * np.sin(theta)
    y = star_center[1] + star_outer_radius * radius * np.cos(theta)
    
    star = plt.Polygon(np.column_stack([x, y]), transform=ax.transAxes, 
                      closed=True, facecolor='#c8a415', edgecolor='#1a3c8a', 
                      linewidth=1.5, zorder=5)
    ax.add_patch(star)
    
    # Add a circular background for the star
    star_bg = Circle((0.5, 0.2), 0.12, transform=ax.transAxes, 
                    facecolor='#1a3c8a', edgecolor='#c8a415', 
                    linewidth=2, zorder=4.5, alpha=0.9)
    ax.add_patch(star_bg)
    
    # Add "StarBot" text
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
        text = ax.text(0.5, 0.08, "StarBot", transform=ax.transAxes, 
                      fontproperties=font_bold.prop, ha='center', va='center', 
                      fontsize=16, color='white', zorder=5)
    else:
        text = ax.text(0.5, 0.08, "StarBot", transform=ax.transAxes, 
                      ha='center', va='center', fontsize=16, fontweight='bold', 
                      color='white', zorder=5)
    
    # Add a subtle shadow effect to the text
    text.set_path_effects([path_effects.withStroke(linewidth=3, foreground='#1a3c8a')])
    
    # Add a subtle glow effect around the avatar
    for i in range(5):
        glow = Circle((0.5, 0.5), 0.48 + i*0.01, transform=ax.transAxes, 
                     facecolor='none', edgecolor='#c8a415', 
                     linewidth=1, zorder=0.5, alpha=0.2-i*0.03)
        ax.add_patch(glow)
    
    # Set axis limits
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Save the figure
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    
    print(f"Photorealistic avatar saved to {output_path}")

def main():
    """
    Generate a photorealistic avatar
    """
    output_path = "static/images/photorealistic_avatar.png"
    generate_photorealistic_avatar(output_path)
    
    # Also save as avatar.png for the chatbot to use
    avatar_path = "static/images/avatar.png"
    generate_photorealistic_avatar(avatar_path)

if __name__ == "__main__":
    main()
