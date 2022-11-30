import pygame
import random
from equationfunction import generateEquation


class Question:

    def __init__(self, x, y, difficulty):
        q = generateEquation(difficulty)
        self.x = x
        self.y = y
        self.question = list(q.keys())[0]
        self.answer = list(q.values())[0]
        self.difficulty = difficulty
        self.icon = pygame.image.load('sprites\question.png')

    def details(self):
        return "Question ({} = {}) is at X={}, Y={}".format(self.question, self.answer, self.x, self.y)

    def hidequestion(self):
        self.icon.fill((0, 0, 0, 0))
