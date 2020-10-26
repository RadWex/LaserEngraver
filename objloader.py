from OpenGL.GL import *

class OBJ:
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.faces = []
        self.normals = []
        self.normals2 = []
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = tuple(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = tuple(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'f':
                face = []
                norms = []
                for v in values[1:]:
                    w = v.split('//')
                    face.append(int(w[0]))
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append(face)
                self.normals2.append(norms)
        '''
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glFrontFace(GL_CCW)
        glBegin(GL_TRIANGLES)
        glColor3f(1,1,1)
        for j in range(len(self.faces)):
            for i in range(len(self.faces[j])):
                if self.normals2[j][i] > 0:
                    glNormal3fv(self.normals[self.normals2[j][i] - 1])
                glVertex3fv(self.vertices[self.faces[j][i] - 1])
        glEnd()
        glEndList()
        '''     

if __name__ == "__main__":
    obj = OBJ("test.obj", swapyz=True)
    for i in obj.normals:
        print(i)