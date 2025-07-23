import arcade

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Space Invaders Clone"
# Welcome to Space Invaders Clone!
# To move your tank, use the left and right arrow keys, and click your left mouse button to fire.
# If you kill all the invaders, you win! If all your buildings are destroyed, you lose!

PLAYER_SPEED = 5
BULLET_SPEED = 10

class SpaceInvaders(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_sprite = None
        self.player_list = None
        self.bullet_list = None
        self.invader_list = None
        self.building_list = None
        self.invader_direction = 1
        self.invader_speed = 1
        self.time_since_last_shot = 0
        self.shoot_cooldown = 0.3
        self.game_over = False
        self.game_won = False


    def setup(self):
        rows = 5
        columns = 10
        x_spacing = 60
        y_spacing = 50
        start_x = 80
        start_y = SCREEN_HEIGHT - 80
        spacing = SCREEN_WIDTH // 9
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.invader_list = arcade.SpriteList()
        self.building_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite("assets/tank.png", scale=0.10)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 40
        self.player_list.append(self.player_sprite)

        for row in range(rows):
            for column in range(columns):
                invader = arcade.Sprite("assets/invader.png", scale=0.08)
                invader.center_x = start_x + column * x_spacing
                invader.center_y = start_y - row * y_spacing
                self.invader_list.append(invader)

        for i in range(1, 9):
            building = arcade.Sprite("assets/building.png", scale=0.10 )
            building.center_x = spacing * i
            building.center_y = 120
            self.building_list.append(building)

    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.bullet_list.draw()
        self.invader_list.draw()
        self.building_list.draw()
        if self.game_over:
            arcade.draw_text(
                "You Win!" if self.game_won else "Game Over",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.WHITE,
                font_size=40,
                anchor_x="center",
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player_sprite.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if self.time_since_last_shot >= self.shoot_cooldown:
            bullet = arcade.SpriteSolidColor(4, 20, arcade.color.YELLOW)
            bullet.center_x = self.player_sprite.center_x
            bullet.center_y = self.player_sprite.center_y + 15
            bullet.change_y = BULLET_SPEED
            self.bullet_list.append(bullet)
            self.time_since_last_shot = 0

    def on_update(self, delta_time):
        if not self.game_over:
            self.player_list.update()
            self.bullet_list.update()
            move_distance = self.invader_speed
            descend_distance = 50
            change_direction = False
            self.time_since_last_shot += delta_time

            for bullet in self.bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.invader_list)
                if hit_list:
                    bullet.remove_from_sprite_lists()
                    for invader in hit_list:
                        invader.remove_from_sprite_lists()

            for bullet in self.bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.building_list)
                if hit_list:
                    bullet.remove_from_sprite_lists()
                    for building in hit_list:
                        building.remove_from_sprite_lists()

            if self.player_sprite.left < 0:
                self.player_sprite.left = 0
            if self.player_sprite.right > SCREEN_WIDTH:
                self.player_sprite.right = SCREEN_WIDTH

            for bullet in self.bullet_list:
                if bullet.top > SCREEN_HEIGHT:
                    bullet.remove_from_sprite_lists()

            remaining = len(self.invader_list)
            if remaining > 0:
                self.invader_speed = max(1, int(6 - remaining / 10))
            for invader in self.invader_list:
                invader.center_x += self.invader_direction * move_distance
                if invader.right > SCREEN_WIDTH or invader.left < 0:
                    change_direction = True
            if change_direction:
                self.invader_direction *= -1
                for invader in self.invader_list:
                    invader.center_y -= descend_distance

            for invader in self.invader_list:
                hit_list = arcade.check_for_collision_with_list(invader, self.building_list)
                for building in hit_list:
                    building.remove_from_sprite_lists()

            if len(self.invader_list) == 0 and not self.game_over:
                self.game_won = True
                self.game_over = True

            if len(self.building_list) == 0 and not self.game_won:
                self.game_over = True

if __name__ == "__main__":
    game = SpaceInvaders()
    game.setup()
    arcade.run()