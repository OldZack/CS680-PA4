"""
This file draws a sphere using ebo.
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

class DisplayableSphere(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cube's information, read-only
    radius = None
    stacks = None
    slices = None
    color = None

    # Stores the texture picture path

    def __init__(self, shaderProg, radius=1, stacks=18, slices=36, color=ColorType.BLUE):
        super().__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(radius, stacks, slices, color)

    def generate(self, radius=1, stacks=18, slices=36, color=None):
        self.radius = radius
        self.stacks = stacks
        self.slices = slices
        self.color = color

        # first store all vertices coordinates in vertices
        self.vertices = np.zeros([stacks*slices, 11])
        for i in range(stacks):
            phi = i / (stacks - 1) * math.pi - math.pi / 2
            for j in range(slices):
                theta = (j % (slices-1)) / (slices-1) * 2 * math.pi
                self.vertices[i*slices+j, 0:3] = [self.radius * math.cos(phi) * math.cos(theta),
                                          self.radius * math.cos(phi) * math.sin(theta),
                                          self.radius * math.sin(phi)]

                x = -radius * math.cos(phi) * radius * math.cos(phi) * math.cos(theta)
                y = radius * math.cos(phi) * (-radius) * math.cos(phi) * math.sin(theta)
                z = (-radius) * math.sin(phi) * math.cos(theta) * radius * math.cos(phi) * math.cos(theta) + \
                    radius * math.sin(phi) * math.sin(theta) * (-radius) * math.cos(phi) * math.sin(theta)
                norm = math.sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2))
                self.vertices[i * slices + j, 3:6] = [-x / norm, -y / norm, -z / norm]
                self.vertices[i * slices + j, 6:9] = [*color]
                self.vertices[i * slices + j, 9:11] = [j/(slices-1), i/(stacks-1)]

        # then for every triangle on sphere, we put its corresponding vertices in indices based on its order
        self.indices = np.zeros([6 * (slices) * (stacks-1)])
        for i in range(stacks - 1):
            for j in range(slices):
                gridN = i * slices + j
                self.indices[6 * gridN + 0] = i*slices+j
                self.indices[6 * gridN + 1] = i*slices+(j + 1) % slices
                self.indices[6 * gridN + 2] = (i + 1)*slices + (j + 1) % slices

                self.indices[6 * gridN + 3] = i*slices+j
                self.indices[6 * gridN + 4] = (i + 1)*slices + (j + 1) % slices
                self.indices[6 * gridN + 5] = (i + 1)*slices + j

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
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexTexture"),
                                  stride=11, offset=9, attribSize=2)
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        self.vao.unbind()

