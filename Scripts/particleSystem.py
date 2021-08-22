# Read a CSV with stellar data and initialize a star system
# Main difference with Unity & Blender: the x,y,z coordinate system
# Blender has no black magic to make the data "upright"


# SUPER helpful instructions: Editing individual particles
# https://devtalk.blender.org/t/manipulating-particles-in-python/7552/2


import bpy
# Pandas isn't automatically available with blender without work
# Unsure if we can use pandas with the compute cluster?
# However csv works so we'll use that
import csv
import os

####### Variables that change the output of the script

# Hardcoding the 47Tuc file. Would be best to have a wrapper to do this
dirname = os.path.dirname(__file__)
dataPath = dirname.replace("Blender/default.blend", "/Data Files/47Tuc.csv")

# Calculate total frames: 
# 30 frames per second
seconds = 10
totalFrames = 30 * seconds


####### Classes and functions

class StellarObject:
    def __init__ (self, objectData: list) -> None:
        '''
        objectData: list of strings from csv
        
        Expected list order
        objectData[0]: x (pc)     : float
        objectData[1]: y (pc)     : float
        objectData[2]: z (pc)     : float
        objectData[3]: vx (km/s)  : float
        objectData[4]: vy (km/s)  : float
        objectData[5]: vz (km/s)  : float
        objectData[6]: mass (solar mass)  : float
        objectData[7]: type       : string
        
        types of objects:
            1.0 - main sequence
            2.2 - evolved star # Rendered as main sequence
            3.0 - white dwarf
            4.0 - neutron star
            5.0 - black hole
        '''
        # Not updating variables directly hence _<varname>

        # Set positions
        if len(objectData) < 3:
            self._x = 1
            self._y = 1
            self._z = 1
        else:
            self._x = float(objectData[0])
            self._y = float(objectData[1])
            self._z = float(objectData[2])
        
        # Set velocities
        if len(objectData) < 6:
            self._vx = 0
            self._vy = 0
            self._vz = 0
        else:
            self._vx = float(objectData[3])
            self._vy = float(objectData[4])
            self._vz = float(objectData[5])
        
        # Set mass in solar mass
        if len(objectData) < 7:
            self._mass = 1
        else:
            self._mass = float(objectData[6])
        
        # Set star type
        if len(objectData) < 8:
            self._type = "1.0"
        else:
            # To Do: Map this to useful types: MS, ES, WD, NS, BH
            self._type = objectData[7] 
        
        
    # Change the positions
    def changePosition(self, x: float, y: float, z: float) -> None:
        self._x = x
        self._y = y
        self._z = z
            
    def getPosition(self) -> tuple: 
        return self._x, self._y, self._z
        
    def changeVelocity (self, vx: float, vy: float, vz: float) -> None:
        self._vx = vx
        self._vy = vy
        self._vz = vz
        
    def getVelocity (self) -> tuple:
        return self._vx, self._vy, self._vz
        
    def changeMass (self, mass) -> None:
        self._mass = mass
        
    def getMass (self) -> float:
        return self._mass

    def changeType (self, type) -> None:
        self._type = type
        
    def getType (self) -> str:
        return self._type
        
    def __str__(self) -> str: 
        return f"\
            Positions:\n\
            x: {self._x} pc\n\
            y: {self._y} pc\n\
            z: {self._z} pc\n\
            Velocities:\n\
            vx: {self._vx} km/s\n\
            vy: {self._vy} km/s\n\
            vz: {self._vz} km/s\n\
            Mass: {self._mass} solar mass\n\
            Type: {self._type}\n"
        
    def __repr__(self) -> str:
        return f"StellarObject([{ self._x }, { self._y }, { self._z }, \
            { self._vx }, { self._vy }, { self._vz }, { self._mass }, { self._type }])"
            
    

def getStellarData(dirPath: str) -> tuple:
    '''
    This is to grab the stellar data from the csv file,
    create the stellar objects, and pass back 
    '''
    
    # Create a list of the different stellar types
    mainSequenceStar = [] # also includes evolved sequence
    whiteDwarfStar = []
    neutronStar = []
    blackHole = []
    
    # Get the data from the csv file
    with open(dataPath, newline='') as csvfile:
        stellarReader = csv.reader(csvfile, delimiter=',')
        firstLine = True
        
        for row in stellarReader:
            # Don't need the header line
            if firstLine:
                firstLine = False
                continue
        
            # Create the star, and sort it to the stellar type
            star = StellarObject(row)    
            if star.getType() == "1.0":
                mainSequenceStar.append(star)
            elif star.getType() == "2.0":
                mainSequenceStar.append(star)
            elif star.getType() == "3.0":
                whiteDwarfStar.append(star)
            elif star.getType() == "4.0":
                neutronStar.append(star)
            elif star.getType() == "5.0":
                blackHole.append(star)
            else:
                print("Totally unexpected!")       

    return mainSequenceStar, whiteDwarfStar, neutronStar, blackHole
    


def createParticleSystems(stellarObjectList: list, type: str) -> None:
    '''
    This will create the proper number of particle systems for the different
    stellar types.
    
    Note: A particle system can only have 1,000,000 particles.
    '''
    
 
    particlesToGenerate = len(stellarObjectList)
    
    if type == "MS":
        particleSystemName = "mainSequence"
        duplicatingObject = "MainSequenceSphere"
    elif type == "WD":
        particleSystemName = "whiteDwarf"
        duplicatingObject = "whiteDwarfSphere"
    elif type == "NS":
        particleSystemName = "neutronStar"
        duplicatingObject = "neutronStar"
    elif type == "BH":
        particleSystemName = "blackHole"
        duplicatingObject = "blackHoleSphere"

    # Create the required number of particle systems   
    while  particlesToGenerate > 0:
        print("I'm in the WHILE!")
        if particlesToGenerate >= 1000000:
            particlesToGenerate -= 1000000
            totalSystemCount = 1000000
        else:
            totalSystemCount = particlesToGenerate
            particlesToGenerate -= 1000000
        
        # The Cube object is the emitter parent mesh object
        obj = bpy.data.objects["Cube"]
        
        print("Sweet a new particle system!")
        obj.modifiers.new(particleSystemName, type='PARTICLE_SYSTEM')
    
        # Update the dependency graph
        #degp = bpy.context.evaluated_depsgraph_get()

        # Get the particle systems attached to the "Cube"
        #particle_systems = obj.evaluated_get(degp).particle_systems   
        
        # Update the most recent particle system added 
        part = obj.particle_systems[-1]
        settings = part.settings
        settings.material_slot = "Material-Particles"
        settings.emit_from = 'VOLUME'
        settings.physics_type = 'NO'
        settings.particle_size = 0.1
        settings.render_type = 'HALO'
        #settings.instance_object = bpy.data.objects[duplicatingObject]
        settings.show_unborn = True
        settings.use_dead = True
        #settings.count = totalSystemCount
        settings.frame_start = 1
        settings.frame_end = totalFrames
        settings.lifetime = totalFrames

        # Update the position of the particles based on the StellarData
        # Get the particles associated to the particle system
        particles = part.particles
        
        for i in range(0,len(particles)):
            star = stellarObjectList.pop()
            particles[i].location = [star.getPosition()]

        # Apply the changes
        #bpy.ops.object.duplicates_make_real()



####### Main Execution

mainSequenceStar, whiteDwarfStar, neutronStar, blackHole = getStellarData(dataPath)

# Print to the console (or terminal: mac) 
print("Main Sequence Stars: " + str(len(mainSequenceStar)))
print("White Dwarf Stars: " + str(len(whiteDwarfStar)))
print("Neutron Stars: " + str(len(neutronStar)))
print("Black Holes: " + str(len(blackHole)))

if len(mainSequenceStar) > 0:
    createParticleSystems(mainSequenceStar, "MS")
    
#if len(whiteDwarfStar) > 0:
#    createParticleSystems(whiteDwarfStar, "WD")

#if len(neutronStar) > 0:
#    createParticleSystems(neutronStar, "NS")
    
#if len(blackHole) > 0:
#    createParticleSystems(blackHole, "BH")






