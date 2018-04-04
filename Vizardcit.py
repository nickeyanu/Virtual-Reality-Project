import oculus
import vizcam
import vizfx
import viz
import vizconnect
import vizact
import vizproximity
import vizinfo

viz.phys.enable()
viz.go()

boxInfo = vizinfo.InfoPanel('Box Material Characteristics', align=viz.ALIGN_LEFT_TOP)
boxInfo.addSeparator()
boxScale = boxInfo.addLabelItem('Scale',viz.addSlider())
boxDensity = boxInfo.addLabelItem('Density',viz.addSlider())
boxFriction = boxInfo.addLabelItem('Friction',viz.addSlider())
boxHardness = boxInfo.addLabelItem('Hardness',viz.addSlider())
boxBounce = boxInfo.addLabelItem('Bounce',viz.addSlider())
boxForce = boxInfo.addLabelItem('Force',viz.addSlider())
#Initial material settings
boxScale.set( .5 )
boxDensity.set( .5 )
boxForce.set( .3 )

#Increase the Field of View
viz.MainWindow.fov(6)
count = 1


#add oculus as hmd(head mounted display)- headset device name
#hmd= oculus.Wift()
#viz.link(hmd.getSensor(), viz.MainView)
#
##add keyboard navigation

#Add lab
lab = viz.addChild('city2.dae')
lab.collideMesh()
lab.disable(viz.DYNAMICS)


#add environment
box = viz.addChild('mini.osg')

viz.setMultiSample(4)
vizconnect.go('configuration.py')

environment = viz.addChild('sky_day.osgb')

transport = vizconnect.getTransport('driving')
viz.link(transport.getNode3d(), box)

viz.MainView.move([0,0,-6])

#ground=viz.addchild('ground_grass.osgb')

#starting point
#viz.MainView.setPositon([0,400,0])
#viz.MainView.lookat(0,0,0)

#create a sunlight
#sun= vizfx.addDirectionalLight
#sun.color(1.0,1.0,0.0275)
#sun.setEuler(90,90,0)

mylight = viz.addLight() 
mylight.enable() 
mylight.position(0, 1, 0) 
mylight.spread(180) 
mylight.intensity(10)

#Change transport speed with key presses 
vizact.onkeydown(viz.KEY_F5,transport.setMovementSpeed,1)
vizact.onkeydown(viz.KEY_F6,transport.setMovementSpeed,3)
vizact.onkeydown(viz.KEY_F7,transport.setMovementSpeed,6)
vizact.onkeydown(viz.KEY_F8,transport.setMovementSpeed,8)

#adding avatars
male = viz.addAvatar('vcc_male.cfg')
male.setPosition([11, 0, 12])
male.setEuler([0,0,0])
walk_over = vizact.walkTo([-6,0,12])
walk_back = vizact.walkTo([11,0,12])
#This line calls that animation
while(count < 100):
   male.addAction(walk_over)
   male.addAction(walk_back)
   count = count + 1
   
count = 1;


male = viz.addAvatar('vcc_male2.cfg')
male.setPosition([11, 0, 25])
male.setEuler([0,0,0])
walk_over = vizact.walkTo([-6,0,20])
walk_back = vizact.walkTo([11,0,25])
#This line calls that animation
while(count < 100):
   male.addAction(walk_over)
   male.addAction(walk_back)
   count = count + 1
   
count = 1;
   
male = viz.addAvatar('vcc_female.cfg')
male.setPosition([11, 0, 37])
male.setEuler([0,0,0])
walk_over = vizact.walkTo([-6,0,37])
walk_back = vizact.walkTo([11,0,37])
#This line calls that animation
while(count < 100):
   male.addAction(walk_over)
   male.addAction(walk_back)
   count = count + 1

male = viz.addAvatar('vcc_male.cfg')
male.setPosition([11, 0, 15])
male.setEuler([0,0,0])

female = viz.addAvatar('vcc_female.cfg')
female.setPosition([11,0,17])
female.setEuler([180,0,0])
 
#Set the male and female to the talking state 
male.state(14)
female.state(14)

#viz.phys.enable()
#
#ground = viz.add('tut_ground.wrl')  # Add ground 
#ground.collidePlane()   # Make collideable plane 
#
#logo = viz.add('logo.wrl',pos=[0,0,0],euler=[0,0,30]) # Add logo 
#logo.collideBox() # Collide 
#logo.add('box.wrl',alpha=.2,scale=logo.getBoundingBox(viz.REL_LOCAL).size) # Show bounding area

def reset():

    #Reset box

    #Place object in its starting position
    boxStartPOS = [ -3, .75, 2 ]
    box.setPosition( boxStartPOS )
    box.setEuler( [0, 0, 0] )

    #Scale according to slider
    scaleFactor = boxScale.get() * 2
    box.setScale( [scaleFactor]*3 )

    #Tell the box to collide as if it were a box and get the handle to its physics object
    box.collideNone() #remove existing physical shapes
    boxPhysicalShape = box.collideBox() #create new physical shape

    #Set the material properties from the sliders
    boxPhysicalShape.density = boxDensity.get()
    boxPhysicalShape.friction = boxFriction.get()
    boxPhysicalShape.hardness = boxHardness.get()
    boxPhysicalShape.bounce = boxBounce.get()

    #Place object on collision course with speed determined by the force slider
    box.applyForce( dir = [ 10 * boxForce.get(), 0, 0 ], duration=0.1, pos = boxStartPOS )
reset()

vizact.onkeydown( ' ', reset )
def pushObject():
    info = viz.pick( True ) #Get object that cursor is pointing at
    if info.valid and ( info.object == ball or info.object ==box ):
        #Create a vector from the mouse position into the world
        line = viz.MainWindow.screenToWorld(viz.mouse.getPosition())
        vec = viz.Vector( line.dir )
        vec.setLength( 1 )
        info.object.applyForce( dir = vec, duration = 0.1, pos = info.point )
        return True