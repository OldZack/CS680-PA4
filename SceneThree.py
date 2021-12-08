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


class SceneThree(Component):
    shaderProg = None
    glutility = None

    lights = None
    lightMask = None
    materials = None
    ambientMask = None
    diffuseMask = None
    specularMask = None
    toggleflag = [False, False, False]
    lightCubes = None

    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        # cube = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 1.5, 1, 1.5))
        # m1 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
        #               np.array((0.4, 0.4, 0.4, 0.1)), 64)
        # cube.setMaterial(m1)
        # cube.renderingRouting = "normal"
        # self.addChild(cube)

        sphere = Component(Point((-2, -1, 0)), DisplayableSphere(shaderProg, 1, 18, 36))
        m1 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.4, 0.4, 0.4, 0.1)), 64)
        sphere.setMaterial(m1)
        sphere.renderingRouting = "normal, lighting"
        sphere.setDefaultAngle(-90, sphere.uAxis)
        sphere.setTexture(shaderProg, "./assets/earth.jpg")
        self.addChild(sphere)
        #
        # cylinder = Component(Point((0,-2,0)), DisplayableCylinder(shaderProg, 0.5, 1, 18, 36))
        # cylinder.renderingRouting = "vertex"
        # self.addChild(cylinder)

        ellipsoid = Component(Point((2, -1, 0)), DisplayableEllipsoid(shaderProg, 1, 0.5, 0.5, 18, 36))
        m2 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.8, 0.8, 0.8, 1)),
                      np.array((0.8, 0.8, 0.8, 1.0)), 240)
        ellipsoid.renderingRouting = "lighting"
        ellipsoid.setMaterial(m2)
        self.addChild(ellipsoid)

        cylinder = Component(Point((0, 2, 0)), DisplayableCylinder(shaderProg, 0.5, 2, 36, 36))
        m3 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.6, 0.6, 0.6, 0.1)), 240)
        cylinder.setMaterial(m3)
        cylinder.renderingRouting = "lighting"
        self.addChild(cylinder)

        l0 = Light(Point([-2.0, 0, 2]),
                   np.array((*ColorType.RED, 1.0)))
        lightCube0 = Component(Point((-2.0, 0, 2)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.RED))
        lightCube0.renderingRouting = "vertex"

        l1 = Light(Point([2.0, 0, -2]),
                   np.array((*ColorType.BLUE, 1.0)), None, Point((0, 0, 2)), np.array((0, 0, 0.2)), 3.0, 45)
        lightCube1 = Component(Point((2.0, 0, -2)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.BLUE))
        lightCube1.renderingRouting = "vertex"

        l2 = Light(Point([0, -1, 0.0]),
                   np.array((*ColorType.YELLOW, 1.0)), Point((0, -1, 0)))
        lightCube2 = Component(Point((0, -1, 0.0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.YELLOW))
        lightCube2.renderingRouting = "vertex"

        self.addChild(lightCube0)
        self.addChild(lightCube1)
        self.addChild(lightCube2)
        self.lights = [l0, l1, l2]
        self.lightMask = [l0, l1, l2]
        self.materials = [m1, m2, m3]
        self.ambientMask = [np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.1, 0.1, 0.1, 0.1)),
                            np.array((0.1, 0.1, 0.1, 0.1))]
        self.diffuseMask = [np.array((0.2, 0.2, 0.2, 1)), np.array((0.8, 0.8, 0.8, 1)), np.array((0.2, 0.2, 0.2, 1))]
        self.specularMask = [np.array((0.4, 0.4, 0.4, 0.1)), np.array((0.8, 0.8, 0.8, 1.0)),
                             np.array((0.6, 0.6, 0.6, 0.1))]
        self.lightCubes = [lightCube0, lightCube1, lightCube2]

    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
