import pyglet
from pyglet import shapes
from pyglet.window import key

window = pyglet.window.Window(width=640, height=420)
batch = pyglet.graphics.Batch()

keys = key.KeyStateHandler()
window.push_handlers(keys)


class Ball:
    def __init__(self) -> None:
        self.ball_start_pos_x = 320
        self.ball_start_pos_y = 200
        self.ball = shapes.Rectangle(self.ball_start_pos_x, self.ball_start_pos_y, 10, 10, batch=batch)
        self.ball_vel_x = -100
        self.ball_vel_y = 100
        
    def setPos(self, pos_x, pos_y):
        self.ball.x = pos_x
        self.ball.y = pos_y

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
        return (self.paddel.x,self.paddel.y)
    
    def up(self,dt):
        if not self.paddel.y >= 380:
            self.paddel.y += self.paddel_vel * dt

    def down(self,dt):
        if not self.paddel.y <= 0:
            self.paddel.y += -self.paddel_vel * dt

        

    
class Game:
    def __init__(self):
        self._ball = Ball()
        self.ball = self._ball.ball
        self.ball_vel_x = self._ball.ball_vel_x
        self.ball_vel_y = self._ball.ball_vel_y
        self.player_paddel = Paddel()
        self.player_paddel.setPos(190, 5)
        self.player_score = 0
        self.opponent_paddel = Paddel()
        self.opponent_paddel.setPos(190, 635)
        self.opponent_score = 0
        self.game_active = False

        

    def update(self, dt):
        #Controll the paddle
        if keys[key.W]:
            game.player_paddel.up(dt)
        if keys[key.S]:
            game.player_paddel.down(dt)
        #Turn on the game
        if keys[key.SPACE]:
            self.game_active = True

        self.chaseBall(self.ball,self.opponent_paddel,dt)

        if self.game_active:
            self.ball.y += self.ball_vel_y * dt
            self.ball.x += self.ball_vel_x * dt

        if self.checkCollision(self.player_paddel):
            self.ball_vel_y = self.ball_vel_y * -1
            self.ball_vel_x = self.ball_vel_x * -1
        if self.checkCollision(self.opponent_paddel):
            self.ball_vel_y = self.ball_vel_y * -1
            self.ball_vel_x = self.ball_vel_x * -1
            
        bScored, who_scored = self.checkScore(self.ball)    
        if bScored:
            self.game_active = False
            if who_scored == 0:
                self.player_score += 1
            else:
                self.opponent_score += 1
            self._ball.setPos(self._ball.ball_start_pos_x, self._ball.ball_start_pos_y)
            print("\nPlayer: %s\nOpponent: %s" %(self.player_score, self.opponent_score))

        #check if upper wall
        if self.ball.y >= 415:
            self.ball_vel_y = self.ball_vel_y * -1
        #check if lower wall
        if self.ball.y <= 5:
            self.ball_vel_y = self.ball_vel_y * -1
        #check if with in p

    def checkCollision(self, paddel):
        self.ball_min_y = self.ball.y - 5
        self.ball_max_y = self.ball.y + 5

        self.ball_min_x = self.ball.x - 5
        self.ball_max_x = self.ball.x + 5

        self.paddel_pos_x, self.paddel_pos_y = paddel.getPos()

        self.paddel_size_half = paddel.paddel_size / 2

        self.paddel_min_x = self.paddel_pos_x - 2.5
        self.paddel_min_y = self.paddel_pos_y 

        self.paddel_max_y = self.paddel_pos_y + self.paddel_size_half
        self.paddel_max_x = self.paddel_pos_x + 2.5

        if self.ball_max_x < self.paddel_min_x:
            return False
        if self.ball_min_x > self.paddel_max_x:
            return False
        if self.ball_max_y < self.paddel_min_y:
            return False
        if self.ball_min_y > self.paddel_max_y:
            return False
        return True
    
    def chaseBall(self, ball, paddel, dt):
        self.paddel_pos_x, self.paddel_pos_y = paddel.getPos()
        if self.paddel_pos_y < ball.y:
            if not self.paddel_pos_y >= 420:
                paddel.up(dt)
        if self.paddel_pos_y > ball.y:
            if not self.paddel_pos_y <= 0:
                paddel.down(dt)
    
    def checkScore(self,ball):
        if ball.x >= 640:
            return True, 0
        if ball.x <= 0:
            return True, 1
        return False, None

        

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