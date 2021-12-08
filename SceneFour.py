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


class SceneFour(Component):
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

        cube = Component(Point((5, 0, 0)), DisplayableCube(shaderProg, 3, 1.5, 3))
        m1 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.3, 0.6, 0.3, 1)),
                      np.array((0.2, 0.9, 0.2, 1)), 64)
        cube.setMaterial(m1)
        cube.renderingRouting = "lighting"
        self.addChild(cube)

        sphere = Component(Point((0,0,0)), DisplayableSphere(shaderProg, 3, 18, 36))
        m2 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.4, 0.4, 0.4, 0.1)), 128)
        sphere.setMaterial(m2)
        sphere.renderingRouting = "lighting"
        self.addChild(sphere)

        torus = Component(Point((4, 0, -3.5)), DisplayableTorus(shaderProg, 0.25, 0.5, 36, 36))
        m3 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.1, 0.1, 0.1, 1)),
                      np.array((0, 0, 0.1, 0.1)), 128)
        torus.setMaterial(m3)
        torus.renderingRouting = "lighting"
        self.addChild(torus)

        l0 = Light(Point([0, 3, 2]),
                   np.array((*ColorType.PURPLE, 1.0)))
        lightCube0 = Component(Point((0, 3, 2)), DisplayableCube(shaderProg, 0.3, 0.3, 0.3, ColorType.PURPLE))
        lightCube0.renderingRouting = "vertex"

        l1 = Light(Point([0, 3, -2]),
                   np.array((*ColorType.BLUE, 1.0)))
        lightCube1 = Component(Point((0, 3, -2)), DisplayableCube(shaderProg, 0.3, 0.3, 0.3, ColorType.BLUE))
        lightCube1.renderingRouting = "vertex"

        l2 = Light(Point([-5, 5, 0]),
                   np.array((*ColorType.SILVER, 1.0)), Point((-0.5, 0.5, 0)))
        lightCube2 = Component(Point((-5, 5, 0)), DisplayableCube(shaderProg, 0.3, 0.3, 0.3, ColorType.SILVER))
        lightCube2.renderingRouting = "vertex"

        l3 = Light(Point([5, 2, 0]),
                   np.array((*ColorType.GREEN, 1.0)), None, Point((0, -1, 0)), np.array((0.0, 2, 0.0)), 3.0, 30)
        lightCube3 = Component(Point((5, 2, 0)), DisplayableCube(shaderProg, 0.3, 0.3, 0.3, ColorType.GREEN))
        lightCube3.renderingRouting = "vertex"

        self.addChild(lightCube0)
        self.addChild(lightCube1)
        self.addChild(lightCube2)
        self.addChild(lightCube3)
        self.lights = [l0, l1, l2, l3]
        self.lightMask = [l0, l1, l2, l3]
        self.materials = [m1, m2, m3]
        self.ambientMask = [np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.1, 0.1, 0.1, 0.1)),
                            np.array((0.1, 0.1, 0.1, 0.1))]
        self.diffuseMask = [np.array((0.3, 0.6, 0.3, 1)), np.array((0.2, 0.2, 0.2, 1)), np.array((0.1, 0.1, 0.1, 1))]
        self.specularMask = [np.array((0.2, 0.9, 0.2, 1)), np.array((0.4, 0.4, 0.4, 0.1)),
                             np.array((0, 0, 0.1, 0.1))]
        self.lightCubes = [lightCube0, lightCube1, lightCube2, lightCube3]

    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
