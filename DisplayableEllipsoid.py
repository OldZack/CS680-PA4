"""
This file draws a Ellipsoid using ebo.
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


class DisplayableEllipsoid(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cube's information, read-only
    radiusX = None
    radiusY = None
    radiusZ = None
    stacks = None
    slices = None
    color = None

    def __init__(self, shaderProg, radiusX=1, radiusY=0.5, radiusZ=0.5, stacks=18, slices=36, color=ColorType.BLUE):
        super().__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(radiusX, radiusY, radiusZ, stacks, slices, color)

    def generate(self, radiusX=1, radiusY=0.5, radiusZ=0.5, stacks=18, slices=36, color=None):
        self.radiusX = radiusX
        self.radiusY = radiusY
        self.radiusZ = radiusZ
        self.stacks = stacks
        self.slices = slices
        self.color = color

        # self.vertices = np.zeros([6 * (slices) * (stacks - 1), 11])
        self.vertices = np.zeros([slices * stacks, 11])
        for i in range(stacks):
            phi = i / (stacks-1) * math.pi - math.pi / 2
            for j in range(slices):
                theta = j / slices * 2 * math.pi
                vertexN = i * slices + j
                self.vertices[vertexN, 0:3] = [self.radiusX * math.cos(phi) * math.cos(theta),
                                               self.radiusY * math.cos(phi) * math.sin(theta),
                                               self.radiusZ * math.sin(phi)]

                x = -radiusZ * math.cos(phi) * radiusY * math.cos(phi) * math.cos(theta)
                y = radiusZ * math.cos(phi) * (-radiusX) * math.cos(phi) * math.sin(theta)
                z = (-radiusX) * math.sin(phi) * math.cos(theta) * radiusY * math.cos(phi) * math.cos(theta) + \
                    radiusY * math.sin(phi) * math.sin(theta) * (-radiusX) * math.cos(phi) * math.sin(theta)
                norm = math.sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2))
                self.vertices[vertexN, 3:6] = [-x / norm, -y / norm, -z / norm]
                self.vertices[vertexN, 6:9] = [*color]

        self.indices = np.zeros([6 * slices * (stacks - 1)])
        for i in range(stacks - 1):
            for j in range(slices):
                gridN = i * slices + j
                self.indices[6 * gridN + 0] = i * slices + j
                self.indices[6 * gridN + 1] = i * slices + (j + 1) % slices
                self.indices[6 * gridN + 2] = (i + 1) * slices + (j + 1) % slices

                self.indices[6 * gridN + 3] = i * slices + j
                self.indices[6 * gridN + 4] = (i + 1) * slices + (j + 1) % slices
                self.indices[6 * gridN + 5] = (i + 1) * slices + j

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
