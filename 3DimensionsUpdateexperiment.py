from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from random import * 

app = Ursina()
bg = Sky()
toolmode=True

player = FirstPersonController()
class Voxel(Button):
    def __init__(self, position = (0,0,0), color = color.green):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = 0.5,
            texture = 'white_cube',
            color = color,
            highlight_color = color,
                    )
    def update(self):
        if self.hovered:
            if toolmode != False:
                if mouse.left:
                    destroy(self)

                if mouse.right:
                    hit_info = raycast(camera.world_position, camera.forward, distance=5)
                    if hit_info.hit:
                        Voxel(position=hit_info.entity.position + hit_info.normal)

class Bullet(Entity):
    def __init__(self, position, direction):
        super().__init__(
            model='sphere',
            position=position,
            color=color.gold,
            scale = 0.1
        )
        self.speed = 30
        self.direction = direction

    def update(self):
        self.position += self.direction * time.dt * self.speed

class Player(Entity):
    def __init__(self,x,y,z):
        super().__init__(
            scale=1,
            model='cube',
            color=color.green,
            position = (x, y, z)
        )
        self.bullet_timer = 0
        self.cooldown = 0.2  # Adjust cooldown as needed

    def update(self):
        current_time = time.time()
        if not toolmode:
            if mouse.left and current_time - self.bullet_timer >= self.cooldown:
                bullet_direction = camera.forward
                bullet1 = Bullet(position=(self.x, self.y, self.z) + (0, 1, 0), direction=bullet_direction)
                self.bullet_timer = current_time

class Tool(Entity):
    def __init__(self,model):
        super().__init__(
            parent=player,
            model=model,
            scale=0.002,
            texture='white_cube',
            position = (0.1,1.3,0.1),
            
        )
        self.rotation_y = -90

    def update(self):
        if mouse.left:
            self.position = Vec3(0.1,1.3,0.6)
        else:
            self.position = (0.1,1.3,0.1)

def update():
    if player.y < -10:
        player.y = 10
        HP.value -= 10
    if held_keys['escape']:
        quit()
        
    playmodel.position = (player.X,player.Y,player.Z)
HP = HealthBar(100,Default)
playmodel = Player(player.X,player.Y,player.Z)
Weapon = Tool('models/drillV3.fbx')
locX = randint(10,20)
locZ = randint(10,20)
for z in range(locZ):
    for x in range(locX):
        voxel = Voxel(position=(x,0,z), color = color.green)
app.run()