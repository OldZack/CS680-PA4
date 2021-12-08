"""
This file draws a torus using ebo.
First version in 11/01/2021
Latest version in 12/07/2021

:author: micou(Zezhou Sun), Zack(Wanzhi Wang)
:version: 2021.12.07
"""

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
from Point import Point
import numpy as np
import ColorType
import math
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

##### TODO 6/BONUS 6: Texture Mapping
# Requirements:
#   1. Set up each object's vertex texture coordinates(2D) to the self.vertices 9:11 columns
#   (i.e. the last two columns). Tell OpenGL how to interpret these two columns:
#   you need to set up attribPointer in the Displayable object's initialize method.
#   2. Generate texture coordinates for the torus and sphere. Use “./assets/marble.jpg” for the torus and
#   “./assets/earth.jpg” for the sphere as the texture image.
#   There should be no seams in the resulting texture-mapped model.

class DisplayableTorus(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current torus's information, read-only
    nsides = 0
    rings = 0
    innerRadius = 0
    outerRadius = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, innerRadius=0.25, outerRadius=0.5, nsides=36, rings=36, color=ColorType.SOFTBLUE):
        super(DisplayableTorus, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(innerRadius, outerRadius, nsides, rings, color)

    def generate(self, innerRadius=0.25, outerRadius=0.5, nsides=36, rings=36, color=ColorType.SOFTBLUE):
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.nsides = nsides
        self.rings = rings
        self.color = color

        # we need to pad one more row for both nsides and rings, to assign correct texture coord to them
        self.vertices = np.zeros([(nsides) * (rings), 11])

        for i in range(rings):
            phi = i % (rings-1) / (rings-1) * 2 * math.pi
            for j in range(nsides):
                theta = j % (nsides-1) / (nsides-1) * 2 * math.pi
                vertexN = i * nsides + j
                self.vertices[vertexN, 0:3] = [(self.outerRadius + self.innerRadius * math.cos(phi)) * math.cos(theta),
                                               (self.outerRadius + self.innerRadius * math.cos(phi)) * math.sin(theta),
                                               self.innerRadius * math.sin(phi)]

                self.vertices[vertexN, 3:6] = [(self.innerRadius * math.cos(phi)) * math.cos(theta), (self.innerRadius * math.cos(phi)) * math.sin(theta), self.innerRadius * math.sin(phi)]
                self.vertices[vertexN, 6:9] = [*color]
                self.vertices[vertexN, 9:11] = [i/(rings-1), j/(nsides-1)]

        self.indices = np.zeros([6 * nsides * (rings - 1)])
        for i in range(rings - 1):
            for j in range(nsides):
                gridN = i * nsides + j
                self.indices[6 * gridN + 0] = i * nsides + j
                self.indices[6 * gridN + 1] = i * nsides + (j + 1) % nsides
                self.indices[6 * gridN + 2] = (i + 1) * nsides + (j + 1) % nsides

                self.indices[6 * gridN + 3] = i * nsides + j
                self.indices[6 * gridN + 4] = (i + 1) * nsides + (j + 1) % nsides
                self.indices[6 * gridN + 5] = (i + 1) * nsides + j

    def draw(self):
        self.vao.bind()
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems which don't enable a default VAO after GLProgram compilation
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

        self.vao.unbind()
