import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in a Spinning Hexagon")
clock = pygame.time.Clock()

# Colors
BG_COLOR = (30, 30, 30)
HEX_COLOR = (200, 200, 200)
BALL_COLOR = (255, 100, 100)

# Hexagon settings
hex_center = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)
hex_radius = 250  # Distance from center to a vertex
hex_sides = 6
# Angular speed (radians per second)
hex_angular_speed = 0.5  
# Current rotation angle (radians)
hex_rotation = 0

# Ball settings
ball_radius = 15
ball_pos = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2 - 100)
ball_vel = pygame.math.Vector2(150, 0)  # initial velocity
gravity = pygame.math.Vector2(0, 500)  # pixels per second^2
# Global friction applied every frame (simulate energy loss)
global_friction = 0.999

# When bouncing, we add a bit of friction on the tangential component.
collision_friction = 0.95

# Button to end the game
BUTTON_WIDTH, BUTTON_HEIGHT = 120, 50
BUTTON_COLOR = (220, 220, 220)
BUTTON_POS = (WIDTH - BUTTON_WIDTH - 20, HEIGHT - BUTTON_HEIGHT - 20)  # Positioned at bottom right

def compute_hexagon_vertices(center, radius, sides, rotation):
    """Return a list of vertices for a regular polygon."""
    vertices = []
    for i in range(sides):
        angle = rotation + (2 * math.pi * i / sides)
        x = center.x + radius * math.cos(angle)
        y = center.y + radius * math.sin(angle)
        vertices.append(pygame.math.Vector2(x, y))
    return vertices

def point_to_segment_distance(pt, seg_a, seg_b):
    """Return the distance and the closest point on segment AB to pt."""
    ab = seg_b - seg_a
    if ab.length_squared() == 0:
        return (pt - seg_a).length(), seg_a
    t = max(0, min(1, (pt - seg_a).dot(ab) / ab.length_squared()))
    proj = seg_a + t * ab
    return (pt - proj).length(), proj

def get_wall_velocity(contact_point, center, angular_speed):
    """
    For a polygon rotating about its center, the instantaneous velocity at a contact point 
    is given by v = ω x r. In 2D, if r = (dx, dy) then v = (-ω*dy, ω*dx).
    """
    r = contact_point - center
    return pygame.math.Vector2(-angular_speed * r.y, angular_speed * r.x)

running = True
prev_time = pygame.time.get_ticks() / 1000  # seconds

while running:
    # Calculate time step
    current_time = pygame.time.get_ticks() / 1000
    dt = current_time - prev_time
    prev_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if (BUTTON_POS[0] <= mouse_pos[0] <= BUTTON_POS[0] + BUTTON_WIDTH and
                    BUTTON_POS[1] <= mouse_pos[1] <= BUTTON_POS[1] + BUTTON_HEIGHT):
                running = False

    # Update hexagon rotation
    hex_rotation += hex_angular_speed * dt

    # Update ball velocity with gravity
    ball_vel += gravity * dt

    # Update ball position
    ball_pos += ball_vel * dt

    # Get current hexagon vertices and edges
    vertices = compute_hexagon_vertices(hex_center, hex_radius, hex_sides, hex_rotation)
    edges = []
    for i in range(hex_sides):
        a = vertices[i]
        b = vertices[(i + 1) % hex_sides]
        edges.append((a, b))

    # Check for collision with each wall (edge)
    for a, b in edges:
        dist, closest_point = point_to_segment_distance(ball_pos, a, b)
        if dist < ball_radius:
            # Compute penetration depth
            penetration = ball_radius - dist
            # Normal from the wall (pointing from the wall to the ball)
            if (ball_pos - closest_point).length_squared() != 0:
                normal = (ball_pos - closest_point).normalize()
            else:
                # Fallback normal (should rarely happen)
                normal = pygame.math.Vector2(0, -1)
            # Push the ball out of the wall by the penetration depth
            ball_pos += normal * penetration

            # Compute wall velocity at the contact point
            wall_vel = get_wall_velocity(closest_point, hex_center, hex_angular_speed)
            # Compute the ball's velocity relative to the moving wall
            rel_vel = ball_vel - wall_vel

            # Reflect the relative velocity about the wall normal if it is moving into the wall
            if rel_vel.dot(normal) < 0:
                # Reflect: v' = v - 2*(v dot n)*n
                rel_vel = rel_vel - 2 * rel_vel.dot(normal) * normal
                # Apply friction on the tangential component
                rel_vel *= collision_friction

                # Update ball velocity to include the wall’s movement
                ball_vel = rel_vel + wall_vel

    # Apply some global friction
    ball_vel *= global_friction

    # Clear screen
    screen.fill(BG_COLOR)

    # Draw hexagon
    pygame.draw.polygon(screen, HEX_COLOR, [(v.x, v.y) for v in vertices], 3)

    # Draw ball
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_pos.x), int(ball_pos.y)), ball_radius)

    # Draw quit button
    pygame.draw.rect(screen, BUTTON_COLOR, (*BUTTON_POS, BUTTON_WIDTH, BUTTON_HEIGHT))
    font = pygame.font.Font(None, 36)
    text_surface = font.render('Quit', True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(BUTTON_POS[0] + BUTTON_WIDTH // 2, BUTTON_POS[1] + BUTTON_HEIGHT // 2))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()