import arcade
#настройки
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Wolf"

PLAYER_MOVEMENT_SPEED = 10
UPDATES_PER_FRAME = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

RIGHT_FACING = 0
LEFT_FACING = 1

LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

class MyGame(arcade.Window):

    def __init__(self):
        #конструктора для инициализации атрибутов класса

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.wall_list = None
        self.player_sprite = None
        self.player_list = None
        self.player = None
        self.physics_engine = None
        self.scene = None
        self.camera = None
        self.setup()


        #звук собирания звезд
        self.coin_list = None
        self.collect_coin_sound = arcade.load_sound("E:\УНИК\программирование\игра\zvezda.wav")
        arcade.set_background_color(arcade.color.COOL_BLACK)

        self.score = 0


#тут добавляю спрайты, где они стоят, через сколько пикселей и т.д.
    def setup(self):
        self.camera = arcade.Camera(self.width, self.height)
        self.scene = arcade.Scene()
        self.score = 0

        image_source = "E:\УНИК\программирование\игра\спрайты\перс-стоит.png"
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        self.player_sprite = arcade.Sprite(image_source)
        self.player_sprite = arcade.AnimatedWalkingSprite()

        #стоит право
        self.player_sprite.stand_right_textures = []
        self.player_sprite.stand_right_textures.append(arcade.load_texture("E:\УНИК\программирование\игра\спрайты\перс-стоит.png"))
        #стоит лево
        self.player_sprite.stand_left_textures = []
        self.player_sprite.stand_left_textures.append(arcade.load_texture("E:\УНИК\программирование\игра\спрайты\перс-стоит.png"))
        #идёт право
        self.player_sprite.walk_right_textures = []
        self.player_sprite.walk_right_textures.append(arcade.load_texture("E:\УНИК\программирование\игра\спрайты\перс-идет.png"))
        #идёт лево
        self.player_sprite.walk_left_textures = []
        self.player_sprite.walk_left_textures.append(arcade.load_texture("E:\УНИК\программирование\игра\спрайты\перс-идет2.png"))


        self.player_sprite.center_x = 300
        self.player_sprite.center_y = 350
        self.scene.add_sprite("Player", self.player_sprite)

    # пол, по которому бегает персонаж
        for x in range(0, 9900, 900):
            wall = arcade.Sprite("E:\УНИК\программирование\игра\спрайты\пол.png")
            wall.center_x = x
            wall.center_y = -200
            self.scene.add_sprite("Walls", wall)
    # добавляю пеньки
        coordinate_list = [[1900, 350], [2900, 350], [3800, 350], [5300, 350], [7100, 350], [9900, 350]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite("E:\УНИК\программирование\игра\спрайты\пень.png")
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

    # добавляю звезды, которые будет собирать персонаж
        for x in range(600, 10000, 900):
            coin = arcade.Sprite("E:\УНИК\программирование\игра\спрайты\звезда.png")
            coin.center_x = x
            coin.center_y = 350
            self.coin_list.append(coin)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )


#теперь всё это "рисуем"
    def on_draw(self):

        self.camera.use()
        arcade.start_render()
        arcade.draw_text(SCREEN_TITLE, 50, 850, arcade.color.WHITE, 30)
        self.coin_list.draw()
        self.player_sprite.draw()

        score_text = f"Score: {self.score}"
        arcade.draw_text('stars: '+str(self.score),
                         self.player_sprite.center_x - 90,
                         self.player_sprite.center_y + 280,
                         arcade.csscolor.WHITE, 40, 10, 'left')
        self.scene.draw()

#прописываю кнопочки при нажатии, скорость
    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

# прописываю кнопочки при их отпускании
    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

#прописываю обновление состояния игры и всех объектов в ней, чтобы звездочки пропадали

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2
        )

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        self.player_sprite.update()
        self.player_sprite.update_animation()


        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score +=1

        changed = False

        self.physics_engine.update()
        self.center_camera_to_player()

#само окошко
def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()