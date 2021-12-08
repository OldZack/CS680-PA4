"""
Define a fixed scene with rotating lights
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import math

import numpy as np

import ColorType
from Animation import Animation
from Component import Component
from Light import Light
from Material import Material
from Point import Point
import GLUtility

from DisplayableCube import DisplayableCube
from DisplayableSphere import DisplayableSphere
from DisplayableCylinder import DisplayableCylinder
from DisplayableEllipsoid import DisplayableEllipsoid
from DisplayableTorus import DisplayableTorus

##### TODO 1: Generate Triangle Meshes
# Requirements:
#   1. Use Element Buffer Object (EBO) to draw the cube. The cube provided in the start code is drawn with Vertex Buffer
#   Object (VBO). In the DisplayableCube class draw method, you should switch from VBO draw to EBO draw. To achieve
#   this, please first read through VBO and EBO classes in GLBuffer. Then you rewrite the self.vertices and self.indices
#   in the DisplayableCube class. Once you have all these down, then switch the line vbo.draw() to ebo.draw().
#   2. Generate Displayable classes for an ellipsoid, torus, and cylinder with end caps.
#   These classes should be like the DisplayableCube class and they should all use EBO in the draw method.
#   PS: You must use the ellipsoid formula to generate it, scaling the Displayable sphere doesn't count
#
#   Displayable object's self.vertices numpy matrix should be defined as this table:
#   Column | 0:3                | 3:6           | 6:9          | 9:11
#   Stores | Vertex coordinates | Vertex normal | Vertex Color | Vertex texture Coordinates
#
#   Their __init__ method should accept following input
#   arguments:
#   DisplayableEllipsoid(radiusInX, radiusInY, radiusInZ, slices, stacks)
#   DisplayableTorus(innerRadius, outerRadius, nsides, rings)
#   DisplayableCylinder(endRadius, height, slices, stacks)
#

##### TODO 5: Create your scenes
# Requirements:
#   1. We provide a fixed scene (SceneOne) for you with preset lights, material, and model parameters.
#   This scene will be used to examine your illumination implementation, and you should not modify it.
#   2. Create 3 new scenes (can be static scenes). Each of your scenes must have
#      * at least 3 differently shaped solid objects
#      * each object should have a different material
#      * at least 2 lights
#      * All types of lights should be used
#   3. Provide a keyboard interface that allows the user to toggle on/off each of the lights in your scene model:
#   Hit 1, 2, 3, 4, etc. to identify which light to toggle.


class test(Component):
    shaderProg = None
    glutility = None

    lights = None
    lightCubes = None

    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        cube = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 1.5, 1, 1.5))
        m1 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.4, 0.4, 0.4, 0.1)), 64)
        cube.setMaterial(m1)
        cube.renderingRouting = "lighting"
        self.addChild(cube)

        # sphere = Component(Point((0,0,0)), DisplayableSphere(shaderProg, 1, 18, 36))
        # m1 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
        #               np.array((0.4, 0.4, 0.4, 0.1)), 64)
        # sphere.setMaterial(m1)
        # sphere.renderingRouting = "texture, lighting"
        # sphere.setDefaultAngle(-90, sphere.uAxis)
        # sphere.setTexture(shaderProg, "./assets/earth.jpg")
        # self.addChild(sphere)
        #
        # cylinder = Component(Point((0,-2,0)), DisplayableCylinder(shaderProg, 0.5, 1, 18, 36))
        # cylinder.renderingRouting = "vertex"
        # self.addChild(cylinder)

        # ellipsoid = Component(Point((0, -2, 0)), DisplayableEllipsoid(shaderProg, 1, 0.5, 0.5, 18, 36))
        # m2 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.8, 0.8, 0.8, 1)),
        #               np.array((0.8, 0.8, 0.8, 1.0)), 240)
        # ellipsoid.renderingRouting = "lighting"
        # ellipsoid.setMaterial(m2)
        # self.addChild(ellipsoid)
        #
        # torus = Component(Point((0, 2, 0)), DisplayableTorus(shaderProg, 0.25, 0.5, 36, 36))
        # m3 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
        #               np.array((0.6, 0.6, 0.6, 0.1)), 240)
        # torus.setMaterial(m3)
        # torus.renderingRouting = "texture, lighting"
        # torus.setTexture(shaderProg, "./assets/marble.jpg")
        # self.addChild(torus)

        l0 = Light(Point([0, 1, 0]),
                   np.array((*ColorType.CYAN, 1.0)), None, Point((0, -1, 0.0)), np.array((0, 0, 3)), 3.0, 45)
        lightCube0 = Component(Point((0, 1, 0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.CYAN))
        lightCube0.renderingRouting = "vertex"

        # l1 = Light(Point([2.0, 1.5, 0.0]),
        #            np.array((*ColorType.GREEN, 1.0)))
        # lightCube1 = Component(Point((2.0, 1.5, 0.0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.GREEN))
        # lightCube1.renderingRouting = "vertex"

        self.addChild(lightCube0)
        self.lights = [l0]
        self.lightCubes = [lightCube0]

    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
