from turtle import *
import math

apple = turtle.Turtle()

def polygon(t, n, length):
    for i in range(n):
        left(360/n)
        forward(length)

def draw_circle(t, r):
    circumference = 2 * math.pi * r
    n = 50
    length = circumference / n
    polygon(t, n, length)
    exitonclick()

draw_circle(apple, 30)