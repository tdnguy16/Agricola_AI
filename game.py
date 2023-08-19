import random
from enum import Enum
from collections import namedtuple
import numpy as np


### improvement tiles
#   improvement_2, improvement_3a (no livestocks), improvement_3b, improvement_4a (no livestocks), improvement_4b, improvement_5
#   improvement_7, improvement_9, improvement_10, improvement_11, improvement_14
#   price [clay, reed, wood]
# improvement = {'price': [0,0,0], 'grain_wood_food': , 'sheep_food': , 'boar_food': , 'cow_food': , 'clay_food': , 'reed_food': , 'wood_food': , 'grain_food': , 'clay_point': , 'reed_point': , 'wood_point': , 'grain_point': , '3_random_point': }
improvement_2  = {'price': [2,0,0], 'grain_wood_food': 2, 'sheep_food': 2, 'boar_food': 2, 'cow_food': 3, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
improvement_3a = {'price': [3,0,0], 'grain_wood_food': 5, 'sheep_food': 0, 'boar_food': 0, 'cow_food': 0, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
improvement_3  = {'price': [3,0,0], 'grain_wood_food': 2, 'sheep_food': 2, 'boar_food': 2, 'cow_food': 3, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
improvement_4a = {'price': [4,0,0], 'grain_wood_food': 5, 'sheep_food': 0, 'boar_food': 0, 'cow_food': 0, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
improvement_4  = {'price': [4,0,0], 'grain_wood_food': 3, 'sheep_food': 2, 'boar_food': 3, 'cow_food': 4, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
improvement_5  = {'price': [5,0,0], 'grain_wood_food': 3, 'sheep_food': 2, 'boar_food': 3, 'cow_food': 4, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
improvement_7  = {'price': [3,0,1], 'grain_wood_food': 0, 'sheep_food': 0, 'boar_food': 0, 'cow_food': 0, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 3, 'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 1, '3_random_point': 0}
improvement_9  = {'price': [0,1,2], 'grain_wood_food': 0, 'sheep_food': 0, 'boar_food': 0, 'cow_food': 0, 'clay_food': 0, 'reed_food': 3, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0, 'reed_point': 1, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
improvement_10 = {'price': [1,2,0], 'grain_wood_food': 0, 'sheep_food': 0, 'boar_food': 0, 'cow_food': 0, 'clay_food': 2, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 1, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
improvement_11 = {'price': [2,0,1], 'grain_wood_food': 0, 'sheep_food': 0, 'boar_food': 0, 'cow_food': 0, 'clay_food': 0, 'reed_food': 0, 'wood_food': 2, 'grain_food': 0, 'clay_point': 0, 'reed_point': 0, 'wood_point': 1, 'grain_point': 0, '3_random_point': 0}
improvement_14 = {'price': [1,1,1], 'grain_wood_food': 0, 'sheep_food': 0, 'boar_food': 0, 'cow_food': 0, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 1}

# pasteur
pasteur_2 = {'price': [0,0,3], 'capacity': 2}
pasteur_4 = {'price': [0,0,5], 'capacity': 4}
pasteur_6 = {'price': [0,0,6], 'capacity': 6}
pasteur_8 = {'price': [0,0,7], 'capacity': 8}
pasteur_list = [pasteur_2, pasteur_4, pasteur_6, pasteur_8]

# actions
# action_a    = {'price': [0,0,0], 'clay': 1, 'reed': 1, 'wood': 1, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0, 'rooster': 0, 'clay_house': 0, 'farmer': 0, 'extra_room': 0, 'pasteur': 0, 'stable': 0, 'field': 0, 'sow': 0}
# action_b_1  = {'price': [0,0,0], 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0, 'rooster': 0, 'clay_house': 0, 'farmer': 0, 'extra_room': 0, 'pasteur': 1, 'stable': 0, 'field': 0, 'sow': 0}
def action_a():
    return {'clay': 1, 'reed': 1, 'wood': 1}

def action_b_1(pasteur_type):
    if AgricolaAI.reset(tiles):
        pass

    return {'price': [x],'pasteur': pasteur_number, 'stable': z}

class AgricolaAI:

    def __init__(self):
        self.reset()

    def reset(self):
        # initial game resouces
        self.board_resouce   = {'2_clay': 2, '1_clay': 1, 'reed': 1, '1_wood': 1, '2_wood': 2, '3_wood': 3, 'food': 1, 'sheep': 1, 'boar': 0, 'cow': 0, 'round': 1}
        self.reserve_resouce = {'clay': 27, 'reed': 19, 'wood': 34, 'grain': 31, 'food': 71, 'sheep': 25, 'boar': 19, 'cow': 17, 'begging': 5}

        self.improvements = [improvement_2, improvement_3a, improvement_3b, improvement_4a, improvement_4b, improvement_5]
        self.tiles = {'pasteur_2': 20, 'pasteur_4': 13, 'pasteur_6': 2, 'pasteur_8': 1, 'field': 20}

        # initial player resouces
        self.player1_state = {'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0, 'begging': 0, 'rooster': 0, 'clay_house': 0, 'farmer': 2, 'livestock_slot': 0, 'grain_on_field': 0, 'extra_room': 0, 'pasteur': 0, 'stable': 0, 'field': 0}
        self.player1_improvements = []



    # def _place_food(self):
    #     x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    #     y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    #     self.food = Point(x, y)
    #     if self.food in self.snake:
    #         self._place_food()
    #
    # def play_step(self, action):
    #     self.frame_iteration += 1
    #     # 1. collect user input
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             quit()
    #
    #     # 2. move
    #     self._move(action)  # update the head
    #     self.snake.insert(0, self.head)
    #
    #     # 3. check if game over
    #     reward = 0
    #     game_over = False
    #     if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
    #         game_over = True
    #         reward = -10
    #         return reward, game_over, self.score
    #
    #     # 4. place new food or just move
    #     if self.head == self.food:
    #         self.score += 1
    #         reward = 10
    #         self._place_food()
    #     else:
    #         self.snake.pop()
    #
    #     # 5. update ui and clock
    #     self._update_ui()
    #     self.clock.tick(SPEED)
    #     # 6. return game over and score
    #     return reward, game_over, self.score
    #
    # def is_collision(self, pt=None):
    #     if pt is None:
    #         pt = self.head
    #     # hits boundary
    #     if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
    #         return True
    #     # hits itself
    #     if pt in self.snake[1:]:
    #         return True
    #
    #     return False
    #
    # def _update_ui(self):
    #     self.display.fill(BLACK)
    #
    #     for pt in self.snake:
    #         pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
    #         pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
    #
    #     pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
    #
    #     text = font.render("Score: " + str(self.score), True, WHITE)
    #     self.display.blit(text, [0, 0])
    #     pygame.display.flip()
    #
    # def _move(self, action):
    #     # [straight, right, left]
    #
    #     clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
    #     idx = clock_wise.index(self.direction)
    #
    #     if np.array_equal(action, [1, 0, 0]):
    #         new_dir = clock_wise[idx]  # no change
    #     elif np.array_equal(action, [0, 1, 0]):
    #         next_idx = (idx + 1) % 4
    #         new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
    #     else:  # [0, 0, 1]
    #         next_idx = (idx - 1) % 4
    #         new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d
    #
    #     self.direction = new_dir
    #
    #     x = self.head.x
    #     y = self.head.y
    #     if self.direction == Direction.RIGHT:
    #         x += BLOCK_SIZE
    #     elif self.direction == Direction.LEFT:
    #         x -= BLOCK_SIZE
    #     elif self.direction == Direction.DOWN:
    #         y += BLOCK_SIZE
    #     elif self.direction == Direction.UP:
    #         y -= BLOCK_SIZE
    #
    #     self.head = Point(x, y)