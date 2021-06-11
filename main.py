import pyglet
from pyglet import shapes
from pyglet.window import key

ball_vel_y = 1
ball_vel_x = 1

window = pyglet.window.Window(width=640, height=420)
batch = pyglet.graphics.Batch()

#ball = shapes.Rectangle(320, 210, 10, 10, batch=batch)
keys = key.KeyStateHandler()
window.push_handlers(keys)


class Ball:
    def __init__(self) -> None:
        self.ball = shapes.Rectangle(320, 210, 10, 10, batch=batch)
        self.ball_vel_x = -100
        self.ball_vel_y = 100

class Paddel:
    def __init__(self) -> None:
        self.paddel_pos_x = 0
        self.paddel_pos_y = 0
        self.paddel_size = 40
        self.paddel_vel = 400
        self.paddel = shapes.Rectangle(self.paddel_pos_x,self.paddel_pos_y,5,self.paddel_size, batch=batch)
    
    def setPos(self, pos_y, pos_x):
        self.paddel.y = pos_y
        self.paddel.x = pos_x
    
    def getPos(self):
        return (self.paddel.y,self.paddel.x)
    
    def up(self,dt):
        self.paddel.y += self.paddel_vel * dt

    def down(self,dt):
        self.paddel.y += -self.paddel_vel * dt

        

    
class Game:
    def __init__(self):
        self._ball = Ball()
        self.ball = self._ball.ball
        self.ball_vel_x = self._ball.ball_vel_x
        self.ball_vel_y = self._ball.ball_vel_y
        self.player_paddel = Paddel()
        self.player_paddel.setPos(210, 5)
        self.opponent_paddel = Paddel()
        self.opponent_paddel.setPos(210, 635)
        

 

    def update(self, dt):
        if keys[key.W]:
            game.player_paddel.up(dt)
        if keys[key.S]:
            game.player_paddel.down(dt)  
        self.ball.y += self.ball_vel_y * dt
        self.ball.x += self.ball_vel_x * dt

        if self.checkCollision(self.player_paddel):
            self.ball_vel_y = self.ball_vel_y * -1
            self.ball_vel_x = self.ball_vel_x * -1
        #check if upper wall
        if self.ball.y >= 419:
            self.ball_vel_y = self.ball_vel_y * -1
        #check if lower wall
        if self.ball.y <= 1:
            self.ball_vel_y = self.ball_vel_y * -1
        #check if with in p

    def checkCollision(self, paddel):
        self.ball_min_y = self.ball.y - 5
        self.ball_max_y = self.ball.y + 5

        self.ball_min_x = self.ball.x - 5
        self.ball_max_x = self.ball.x + 5

        self.paddel_pos_y, self.paddel_pos_x = paddel.getPos()


        self.paddel_size_half = paddel.paddel_size / 2

        self.paddel_min_x = self.paddel_pos_x - self.paddel_size_half
        self.paddel_min_y = self.paddel_pos_y - self.paddel_size_half

        self.paddel_max_y = self.paddel_pos_y + self.paddel_size_half
        self.paddel_max_x = self.paddel_pos_x + self.paddel_size_half

        if self.ball_max_x < self.paddel_min_x:
            return False
        if self.ball_min_x > self.paddel_max_x:
            return False
        if self.ball_max_y < self.paddel_min_y:
            return False
        if self.ball_min_y > self.paddel_max_y:
            return False
        return True
        
        






game = Game()
  
@window.event
def on_draw():
    window.clear()
    batch.draw()

def main():
    pyglet.clock.schedule_interval(game.update, 1/60)
    
    pyglet.app.run()
    

if __name__ == "__main__":
    main()