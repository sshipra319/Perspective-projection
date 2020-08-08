# Shipra Saini
# sxs2152
# 2018-11-07

import sys

class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.m_Window   = []
    self.m_Viewport = []
    self.xmin = float("inf")
    self.ymin = float("inf")
    self.zmin = float("inf")
    self.xmax = float("-inf")
    self.ymax = float("-inf")
    self.zmax = float("-inf")
    self.s_Transform = ();
    self.distance = 0

    if inputFile is not None :
      # File name was given.  Read the data from the file.
      self.loadFile( inputFile )

  def loadFile( self, inputFile ) :
     
        with open(inputFile, 'r') as fp:
            lines = fp.read().replace('\r', '').split('\n')
            
        for (index, line) in enumerate(lines, start=1):
                line = line.strip()
                
                if line.startswith('v'):
                    t_vertices = tuple(map(float,line.replace('v','').split()))
                    
                    if len(t_vertices) != 3:
                        print("Line " + str(index) + " is a malformed vertex spec.")
                    else:
                        self.m_Vertices.append(t_vertices)                           
                        if t_vertices[0] < self.xmin:
                            self.xmin = t_vertices[0]    #min coordinates
                        if t_vertices[1] < self.ymin:
                            self.ymin = t_vertices[1]
                        if t_vertices[2] < self.zmin:
                            self.zmin = t_vertices[2]
                        if t_vertices[0] > self.xmax:   #max coordinates
                            self.xmax = t_vertices[0]
                        if t_vertices[1] > self.ymax:
                            self.ymax = t_vertices[1]                                
                        if t_vertices[2] > self.zmax:
                            self.zmax = t_vertices[2]                                 
                    
                elif line.startswith('f'):
                    
                    faces = tuple(map(int,line.replace('f','').split()))
                    l_faces = list()
                    for face in faces:
                        l_faces.append(face-1)
                        
                    t_faces = tuple(l_faces)
                    if len(t_faces) != 3:
                        print("Line " + str(index) + " is a malformed face spec.")
                    else:
                        self.m_Faces.append(t_faces)
                            
                elif line.startswith('w'):
                    
                        t_window = tuple(map(float,line.replace('w','').split()))
                        
                        if len(t_window) != 4:
                            print("Line " + str(index) + " is a malformed window spec.")
                        else:
                            self.m_Window = t_window
                            
                elif line.startswith('s'):
                    
                        t_viewport = tuple(map(float,line.replace('s','').split()))
                        
                        if len(t_viewport) != 4:
                            print("Line " + str(index) + " is a malformed viewport spec.")
                        else:
                            self.m_Viewport = t_viewport
                             
                
    ##################################################
    # TODO: Put your version of loadFile() from HMWK 01
    # here.  Enhance this routine to do a running computation
    # of the bounding box.
    ##################################################

  def getBoundingBox( self ) :      
      
      return (self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax)      
      
    ##################################################
    # TODO: Put your code to return the bounding box here.
    # Your routine should return a tuple with six
    # elements:
    #   ( xmin, xmax, ymin, ymax, zmin, zmax )
    ##################################################

  def specifyTransform( self, ax, ay, sx, sy, distance ) :   
      
     self.s_Transform = (ax, ay, sx, sy, distance)
     
    ##################################################
    # TODO: Put your code to remember the transformation here.
    ##################################################

  def getTransformedVertex( self, vNum, doPerspective ) :  
      
      ax = self.s_Transform[0]
      ay = self.s_Transform[1]
      sx = self.s_Transform[2]
      sy = self.s_Transform[3]
      d = self.s_Transform[4]
      x1 = self.m_Vertices[vNum][0]
      y1 = self.m_Vertices[vNum][1]
      z1 = self.m_Vertices[vNum][2]
      
      if doPerspective == 1:
          x = sx*(x1/(1-(z1/d))) + ax
          y = sy*(y1/(1-(z1/d))) + ay
          z = 0.0
          
      else:
          x = ax + (sx*x1)
          y = ay + (sy*y1)
          z = 0.0
      
      return (x, y ,z)
  
    ##################################################
    # TODO: Put your code to return a transformed version of
    # vertex n here.  Remember, vNum goes 0 .. n-1,
    # where n is the number of vertices.
    # Your routine should return a tuple with three
    # elements:
    #   ( x', y', z' )
    ##################################################

  def getFaces( self )    : return self.m_Faces
  def getVertices( self ) : return self.m_Vertices
  def getViewport( self ) : return self.m_Viewport
  def getWindow( self )   : return self.m_Window

#---------#---------#---------#---------#---------#--------#
def constructTransform( w, v, width, height ) :
    
    fx = -w[0]
    fy = -w[1]
    gx = width*v[0]
    gy = height*v[1]
    sx = (width*(v[2] - v[0]))/(w[2] - w[0])
    sy = (height*(v[3] - v[1]))/(w[3] - w[1])
    ax = (fx*sx) + gx
    ay = (fy*sy) + gy
    
    return (ax, ay, sx, sy)

  ##################################################
  # TODO: Put your code to return the transform here.
  # Your routine should use w, v, width, and height
  # parameters according to the description in
  #   "4303 Homework 02 Transform.pdf"
  # to compute the transform.
  # Your routine should return a tuple with four
  # elements:
  #   ( ax, ay, sx, sy )
  ##################################################

#---------#---------#---------#---------#---------#--------#
def _main() :
  # Get the file name to load and the canvas size.
  fName  = sys.argv[1]
  width  = int( sys.argv[2] )
  height = int( sys.argv[3] )

  # Create a ModelData object to hold the model data from
  # the supplied file name.
  model = ModelData( fName )

  # Now that it's loaded, print out a few statistics about
  # the model data that we just loaded.
  print( "%s: %d vert%s, %d face%s" % (
    fName,
    len( model.getVertices() ), 'ex' if len( model.getVertices() ) == 1 else 'ices',
    len( model.getFaces() ), '' if len( model.getFaces() ) == 1 else 's' ))

  print( 'First 3 vertices:' )
  for v in model.getVertices()[0:3] :
    print( '     ', v )

  print( 'First 3 faces:' )
  for f in model.getFaces()[0:3] :
    print( '     ', f )

  w = model.getWindow()
  v = model.getViewport()
  print( 'Window line:', w )
  print( 'Viewport line:', v )
  print( 'Canvas size:', width, height )

  print( 'Bounding box:', model.getBoundingBox() )

  ( ax, ay, sx, sy ) = constructTransform( w, v, width, height )
  print( f'Transform is {ax} {ay} {sx} {sy}' )

  model.specifyTransform( ax, ay, sx, sy )

  print( 'First 3 transformed vertices:' )
  for vNum in range( 3 ) :
    print( '     ', model.getTransformedVertex( vNum ) )

#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#
