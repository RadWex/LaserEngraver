import OpenGL.GL as gl
import OpenGL.GLU as glu
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import uic, QtOpenGL
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QImage, QKeyEvent
from PyQt5.QtOpenGL import QGL, QGLFormat, QGLWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtCore
import sys
import os
from PIL import Image as Image
import numpy
from os import listdir
from os.path import isfile, join
import os
from PIL import Image as Image
import numpy
import operator
from objloader import *
       


class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(QGLFormat(QGL.SampleBuffers), parent)
        self.setFocusPolicy(Qt.StrongFocus) #keyboard support 
        self.startTimer(1000/144)
        self.camera = True
        self.w = self.width()
        self.h = self.height()
        self.zoom = 20
        self.xRot = 0 # roll
        self.yRot = 0 # pitch 
        self.zRot = 0 # yaw 
        
        self.R_MIN = 4.5
        self.R_MAX = 60
        
        self.lastPos = QPoint()
        #self.clearColor = QColor()

    def wheelEvent(self,event):
        self.zoom-=event.angleDelta().y()/100
        if(self.zoom < self.R_MIN):
            self.zoom = self.R_MIN
        if(self.zoom > self.R_MAX):
            self.zoom = self.R_MAX
        self.updateGL()

    def keyPressEvent(self, e):
        if(e.key()==68):
            self.zoom+=0.3
        if(e.key()==65):
            self.zoom-=0.3
        if(e.key()==53):
            if self.camera: 
                self.camera = False
            else:
                self.camera = True
        print('Key release {}'.format(e.key()) )

    def mouseReleaseEvent(self, event):
        pass

    def mousePressEvent(self, event):
        self.lastPos = event.pos()
    
    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
            
        #if(False): # ORG 
        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + .5 * dy)
            self.setYRotation(self.yRot + .5 * dx)
        self.lastPos = event.pos()     
        self.update()

    def setXRotation(self, angle):
        if angle != self.xRot:
            self.xRot = angle
            #self.xRotationChanged.emit(angle)
            self.update()
            
    def setYRotation(self, angle):
        if angle != self.yRot:
            self.yRot = angle
            #self.yRotationChanged.emit(angle)
            self.updateGL()

    def getImg(self, fname):
        im = QImage(fname)
        im = im.convertToFormat(QImage.Format_RGBA8888)
        ptr = im.bits()
        ptr.setsize(im.byteCount())
        return ptr.asstring()

    def load_graphics(self, path):
        graphics = []
        list_of_files = [f for f in listdir(path) if isfile(join(path, f))]

        for i in list_of_files:
            im =QImage(path+'/'+i)
            im =im.convertToFormat(QImage.Format_RGBA8888)
            ptr=im.bits()
            ptr.setsize(im.byteCount())
            graphics.append(ptr.asstring())

        return graphics
    
    def changeTexture(self, texture_id, image):
        # this is the texture we will manipulate
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 64, 64, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, image)  # load bitmap to texture

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        self.w = w; self.h = h
        self.camera_settings()

    def wireCube(self):
        #self.qglColor(Qt.black)
        cubeVertices = ((1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1),
                        (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1))
        cubeEdges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5),
                     (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7))
    
        glLineWidth(3.0)
        glBegin(GL_LINES)
        glColor3fv((.8,.1,.3))
        for cubeEdge in cubeEdges:
            for cubeVertex in cubeEdge:
                glVertex3fv(cubeVertices[cubeVertex])
        glEnd()

    def drawSiatka(self, gridSize, gridThickness):
        size = gridSize
        if gridSize%2==0:
            size = gridSize + 1
        coord = size//2
        size2 = size//2
        coord2 = size2//2
        glLineWidth(1.0)
        glBegin(GL_LINES)
        glColor3fv((.3,.3,.3))
        for i in range(size):
            obliczenia = -coord+i
            if(obliczenia==0):
                glColor3fv((1,0,0))
            else:
                glColor3fv((.3,.3,.3))
            glVertex3f(obliczenia, 0.0, -coord)
            glVertex3f(obliczenia, 0.0, coord)
            if(obliczenia==0):
                glColor3fv((0,1,0))
            else:
                glColor3fv((.3,.3,.3))
            glVertex3f(coord, 0.0, obliczenia)
            glVertex3f(-coord, 0.0, obliczenia)
        glEnd()

        glLineWidth(3.0)
        glBegin(GL_LINES)
        for i in range(0,size,5):
            obliczenia = -coord+i
            glVertex3f(obliczenia, 0.0, -coord)
            glVertex3f(obliczenia, 0.0, coord)
            glVertex3f(coord, 0.0, obliczenia)
            glVertex3f(-coord, 0.0, obliczenia)
        glEnd()
    
    def solidCube(self, path, swapyz):
        obj = OBJ(path, swapyz)
        self.faces_list = glGenLists(2)


        glNewList(self.faces_list, GL_COMPILE)
        glFrontFace(GL_CCW)
        glBegin(GL_TRIANGLES)
        glColor3f(.8,.8,.8)
        for j in range(len(obj.faces)):
            for i in range(len(obj.faces[j])):
                if obj.normals2[j][i] > 0:
                    glNormal3fv(obj.normals[obj.normals2[j][i] - 1])
                glVertex3fv(obj.vertices[obj.faces[j][i] - 1])
        glEnd()
        glEndList()

        glColor3f(1,0,0)
        glLineWidth(.1)
        #edges_list = glGenLists(2)
    
        glNewList(self.faces_list+1, GL_COMPILE)
        glBegin(GL_LINES)
        for face in obj.faces:
            a,b,c = face
            try:
                glVertex3fv(obj.vertices[a-1])
                glVertex3fv(obj.vertices[b-1])
                glVertex3fv(obj.vertices[b-1])
                glVertex3fv(obj.vertices[c-1])
                glVertex3fv(obj.vertices[c-1])
                glVertex3fv(obj.vertices[a-1])
            except:
                pass
        glEnd()
        glEndList()


    def timerEvent(self, event):
        self.update()

    def paintGL(self):
        self.camera_settings()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #?
        gl.glLoadIdentity()
        glu.gluLookAt(self.zoom, self.zoom, 0, 0, 0, 0, 0, 1, 0)
        glPushMatrix() #?
        
        glRotatef(self.xRot,0.0,0.0,-1.0)            # Rotate The Cube On It's X Axis
        glRotatef(self.yRot,0.0,1.0,0.0)            # Rotate The Cube On It's Y Axis

        #glScalef(.5, .5, .5)
        self.drawSiatka(23,1)

        for i in range(10):
            glPushMatrix()
            glTranslatef(-15+i*3,0.0,0.0)
            glColor3f(1,1,1)
            glCallList(self.faces_list)
            glColor3f(1,0,0)
            glLineWidth(2.0)
            glPolygonOffset(-1.0, -1.0)
            glEnable(GL_POLYGON_OFFSET_LINE)
            glEnable(GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            glCallList(self.faces_list+1)
            glDisable(GL_POLYGON_OFFSET_LINE)
            glDisable(GL_BLEND)
            glPopMatrix()

        glPopMatrix() #?
    
    def initializeGL(self):
        glClearDepth(1.0)              
        glDepthFunc(GL_LESS)
        #glEnable(GL_TEXTURE_2D)
        #gl.glEnable(gl.GL_CULL_FACE) #nie dziala za dobrze
        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(GL_MULTISAMPLE)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        gl.glClearColor(.1, .1, .1, .0) 
        glLoadIdentity()   

        glEnable(GL_LINE_SMOOTH)
        self.solidCube("test.obj", swapyz=True)

        

        #self.graphics = self.load_graphics("images")
        #self.baseimages = []
        #self.tex_id = glGenTextures(len(self.graphics))
        #for nr, i in enumerate(self.graphics):
        #    #self.tex_id.append(glGenTextures(nr+1))
        #    self.baseimages.append(i)
        #    self.changeTexture(self.tex_id[nr], self.baseimages[nr])

    def camera_settings(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        if(self.camera):
            glu.gluPerspective(
                45,  # field of view in degrees
                self.w / float(self.h or 1),  # aspect ratio
                .25,  # near clipping plane
                200,  # far clipping plane
            )
        else:
            glOrtho(-self.w/50, self.w/50, -self.h/50, self.h/50, 0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GLWidget()
    window.resize(800, 450)
    window.show()
    sys.exit(app.exec_())

