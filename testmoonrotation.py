import sys            
from OpenGL.GL import *            
from OpenGL.GLUT import *            
from OpenGL.GLU import *            
from PIL import Image            
    
# Rotation angles for the spheres            
rotation_angle_earth = 0.0            
rotation_angle_moon = 0.0            
rotation_angle_sun = 0.0            
    
texture_id_earth = None            
texture_id_moon = None            
texture_id_sun = None            
    
def load_texture(filename):            
    """Load a texture from a file."""            
    try:            
        image = Image.open(filename)            
        image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip the image vertically            
        width, height = image.size            
        image_data = image.convert("RGBA").tobytes()            
    
        # Generate a texture ID            
        texture_id = glGenTextures(1)            
        glBindTexture(GL_TEXTURE_2D, texture_id)            
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)            
    
        # Set texture parameters            
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)            
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)            
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)            
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)            
    
        print(f"Texture loaded: {filename} (Size: {width}x{height})")            
        return texture_id            
    except Exception as e:            
        print(f"Failed to load texture: {e}")            
        return None            
    
def init():            
    """Initialize lighting, material properties, and texture."""            
    glEnable(GL_LIGHTING)            
    glEnable(GL_LIGHT0)            
    glEnable(GL_TEXTURE_2D)  # Enable texturing            
    
    light_position = [1.0, 1.0, 1.0, 0.0]            
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)            
    
    # Set material properties to allow texture to show            
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])  # Darker ambient light            
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])  # White diffuse light            
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Specular light            
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)            
    
    # Load the textures            
    global texture_id_earth, texture_id_moon, texture_id_sun            
    texture_id_earth = load_texture("earth.jpg")  # Replace with your texture file path            
    texture_id_moon = load_texture("moon.jpg")    # Replace with your texture file path            
    texture_id_sun = load_texture("sun.jpg")      # Replace with your texture file path            
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)            
    
def draw_sphere(radius, slices, stacks, texture_id):            
    """Draw a textured sphere using OpenGL."""            
    if texture_id is not None:            
        glBindTexture(GL_TEXTURE_2D, texture_id)            
    else:            
        print("Texture ID is None, texture not applied.")            
    
    quadric = gluNewQuadric()            
    gluQuadricNormals(quadric, GLU_SMOOTH)            
    gluQuadricTexture(quadric, GL_TRUE)  # Enable texture mapping            
    gluSphere(quadric, radius, slices, stacks)            
    gluDeleteQuadric(quadric)            
    
def display():            
    global rotation_angle_earth, rotation_angle_moon, rotation_angle_sun            
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)            
    glEnable(GL_DEPTH_TEST)            
    
    glLoadIdentity()            
    gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)  # Adjusted camera position for better view            
    
    # Calculate the elapsed time in seconds            
    elapsed_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0  # Convert milliseconds to seconds            
    
    # Speed multiplier            
    speed_multiplier = 10000.0            
    
    # Calculate rotation angles based on actual periods with speed multiplier    
    rotation_angle_sun = (elapsed_time * speed_multiplier / (365.25 * 24 * 3600)) * 360.0  # 1 year for the Sun    
    rotation_angle_earth = (elapsed_time * speed_multiplier / (24 * 3600)) * 360.0  # 24 hours for the Earth    
    rotation_angle_moon = (elapsed_time * speed_multiplier / (27.3 * 24 * 3600)) * 360.0  # 27.3 days for the Moon    
    
    # Draw the Sun            
    glPushMatrix()            
    draw_sphere(1.0, 32, 32, texture_id_sun)  # Draw the Sun at the center            
    glPopMatrix()            
    
    # Draw the Earth            
    glPushMatrix()            
    glRotatef(rotation_angle_sun, 0, 1, 0)  # Rotate around the Sun            
    glTranslatef(3.0, 0, 0)  # Move Earth away from the Sun            
    glRotatef(rotation_angle_earth, 0, 1, 0)  # Rotate Earth on its axis            
    draw_sphere(0.3, 32, 32, texture_id_earth)  # Draw the Earth            
    
    # Draw the Moon            
    glPushMatrix()            
    glTranslatef(0.5, 0, 0)  # Move Moon away from Earth            
    glRotatef(rotation_angle_moon, 0, 1, 0)  # Rotate around the Earth (this should be removed)  
    draw_sphere(0.1, 32, 32, texture_id_moon)  # Draw the Moon            
    glPopMatrix()            
    
    glPopMatrix()  # Pop the Earth matrix    
    
    glutSwapBuffers()            
    
def reshape(width, height):            
    glViewport(0, 0, width, height)            
    glMatrixMode(GL_PROJECTION)            
    glLoadIdentity()            
    gluPerspective(45.0, float(width) / float(height), 0.1, 50.0)            
    glMatrixMode(GL_MODELVIEW)            
    
def main():            
    glutInit(sys.argv)            
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)            
    glutInitWindowSize(800, 600)            
    glutCreateWindow(b"Textured Earth and Moon Orbiting the Sun")            
    
    init()            
    glutDisplayFunc(display)            
    glutIdleFunc(display)            
    glutReshapeFunc(reshape)            
    
    glutMainLoop()            
    
if __name__ == "__main__":            
    main()            
