"""
This file draws a cylinder using ebo.
First version in 11/01/2021
Latest version in 12/07/2021

:author: micou(Zezhou Sun), Zack(Wanzhi Wang)
:version: 2021.12.07
"""
import math

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
import numpy as np
import ColorType

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")


class DisplayableCylinder(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cube's information, read-only
    radius = None
    height = None
    stacks = None
    slices = None
    color = None

    def __init__(self, shaderProg, radius=0.5, height=1, stacks=18, slices=36, color=ColorType.BLUE):
        super().__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(radius, height, stacks, slices, color)

    def generate(self, radius=1, height=1, stacks=18, slices=36, color=None):
        self.radius = radius
        self.height = height
        self.stacks = stacks
        self.slices = slices
        self.color = color

        self.vertices = np.zeros([4 * slices+2, 11])
        self.vertices[0, 0:9] = [0, height/2, 0, 0, 1, 0, *color]
        self.vertices[1, 0:9] = [0, -height/2, 0, 0, -1, 0, *color]
        for i in range(slices):
            theta = i / (slices) * 2 * math.pi
            # First store the vertices of two circles & sides
            self.vertices[i+2, 0:3] = self.vertices[i+2 + 2 * slices, 0:3] = [self.radius * math.cos(theta),
                                                                            self.height / 2,
                                                                            self.radius * math.sin(theta)]
            self.vertices[i+2 + slices, 0:3] = self.vertices[i+2 + 3 * slices, 0:3] = [self.radius * math.cos(theta),
                                                                                     -self.height / 2,
                                                                                     self.radius * math.sin(theta)]

            # The normal values on two circles are at opposite
            self.vertices[i + 2, 3:6] = [0, 1, 0]
            self.vertices[i + 2, 6:9] = [*color]
            self.vertices[i+2 + slices, 3:6] = [0, -1, 0]
            self.vertices[i + 2 + slices, 6:9] = [*color]
            self.vertices[i + 2 + 2 * slices, 3:6] = self.vertices[i + 2 + 3 * slices, 3:6] = [math.cos(theta), 0, math.sin(theta)]
            self.vertices[i + 2 + 2 * slices, 6:9] = self.vertices[i + 2 + 3 * slices, 6:9] = [*color]

        np.set_printoptions(threshold=np.inf)

        self.indices = np.zeros([12 * slices])
        for i in range(slices):
            if i == slices-1:
                self.indices[i * 3:i * 3 + 3] = [0, i + 2, 2]
                self.indices[(i+slices) * 3:(i+slices) * 3 + 3] = [1, i+ slices + 2, slices + 2]
                self.indices[(i + 2 * slices) * 3:(i + 2 * slices) * 3 + 3] = [i + 2*slices + 2, 2*slices + 2, i + 3*slices + 2]
                self.indices[(i + 3 * slices) * 3:(i + 3 * slices) * 3 + 3] = [i + 3*slices + 2, 3*slices + 2, 2*slices + 2]
            else:
                self.indices[i*3:i*3+3] = [0, i+2, i+3]
                self.indices[(i+slices) * 3:(i+slices) * 3 + 3] = [1, i + slices + 2, i + slices + 3]
                self.indices[(i + 2 * slices) * 3:(i + 2 * slices) * 3 + 3] = [i + 2*slices + 2, i + 2*slices + 3, i + 3*slices + 2]
                self.indices[(i + 3 * slices) * 3:(i + 3 * slices) * 3 + 3] = [i + 3*slices + 2, i + 3*slices + 3, i + 2*slices + 3]




    def draw(self):
        self.vao.bind()
        # TODO 1.1 is at here, switch from vbo to ebo
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems that don't enable a default VAO after GLProgram compilation
        """
        self.vao.bind()
        self.vbo.setBuffer(self.vertices, 11)
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPos"),
                                  stride=11, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexNormal"),
                                  stride=11, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexColor"),
                                  stride=11, offset=6, attribSize=3)
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        self.vao.unbind()
