import pygame
import random
import math
from user_settings import *

# Begin mob definitions
class Mob(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, color=(127, 127, 127)):  # Default to grey if no color is provided
        super().__init__()
        self.image = pygame.Surface((10, 10))  # Size of mob
        self.image.fill(color)  # Use the passed color (or grey)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.current_task = None  # Placeholder for the task, which can be set by specific mobs

    def update(self, dt):
        """Update the mob's position and task"""
        if self.current_task:
            #print(f"Updating task: {self.current_task.task_type}. Time left: {self.current_task.time_left}")
            self.current_task.update(dt)  # Update the task (e.g., decrement task time)
            self.current_task.perform_task(self)  # Perform the task

    def assign_task(self, task):
        #print(f"Assigning task: {task.task_type}. Mob position: ({self.rect.x}, {self.rect.y})")
        """Assign a valid task to the mob"""
        if not isinstance(task, Task):
            raise TypeError("Assigned task must be an instance of Task or its subclasses.")
        self.current_task = task
        task.mob = self  # Link the task back to this mob

    def remove_task(self):
        """Remove the current task"""
        self.current_task = None    


class Fairy(Mob):
    def __init__(self, x, y, color): 
        super().__init__(x, y, color)
        self.assign_task(Task('idle', random.randint(3, 5)))  # Assign an initial task for Fairy
        self.mob = 'fairy'

    def update(self, dt):
        """Update the fairy's position and task"""
        if self.current_task and self.current_task.time_left <= 0:
            #print(f"Task complete for Fairy at ({self.rect.x}, {self.rect.y}). Removing task.")
            self.remove_task()  # Clear the current task when it's complete
        
        if self.current_task:
            #print(f"Updating task: {self.current_task.task_type}. Time left: {self.current_task.time_left}")
            self.current_task.update(dt)
            self.current_task.perform_task(self)

        super().update(dt)
        # Additional fairy-specific behavior can be added here
        # E.g., React to environment, interact with other mobs, etc.

    def remove_task(self):
        """Specialized task removal for fairies"""
        if isinstance(self.current_task, MoveTask):
            #print(f"Fairy at ({self.rect.x}, {self.rect.y}) completed a move task!")
            pass
        elif isinstance(self.current_task, Task):
            print(f"Fairy at ({self.rect.x}, {self.rect.y}) finished task: {self.current_task.task_type}")

        # Assign a new idle task for the fairy
        self.assign_task(Task('idle', random.randint(3, 5)))
        


class TestFairy(Fairy):  # TestFairy is a subclass of fairy
    def __init__(self, x=None, y=None, color=(127, 127, 127)):
        # Make a random color
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # Generate random x and y within the screen bounds
        if x is None:
            x = random.randint(200, SCREEN_WIDTH - 10)  # Subtracting the fairy's size (10x10)
        if y is None:
            y = random.randint(0, SCREEN_HEIGHT - 10)  # Subtracting the fairy's size (10x10)

        super().__init__(x, y, color=random_color)
        self.special_attribute = "Test"
        


# Begin task definitions
class Task:
    def __init__(self, task_type, duration=0):
        self.task_type = task_type  # What the mob is doing (e.g., 'move', 'rest')
        self.duration = duration    # How long the task should last
        self.time_left = duration   # Time left to complete the task

    def update(self, dt):
        self.check_task_progress(dt)

    def check_task_progress(self, dt):
        """Update the task, decreasing the time left if necessary"""
        if self.time_left > 0:
            self.time_left -= dt
        else:
            self.complete_task()

    def perform_task(self, mob):
        """Perform the task based on the mob and task_type"""
        
        if self.task_type == 'idle':
            #Fairies idle by moving randomly within a small range
            if isinstance(mob, Fairy) and not isinstance(mob.current_task, MoveTask):
                target_x = random.randint(max(0, mob.rect.x - 20), min(SCREEN_WIDTH - 10, mob.rect.x + 20))
                target_y = random.randint(max(0, mob.rect.y - 20), min(SCREEN_HEIGHT - 10, mob.rect.y + 20))
                mob.assign_task(MoveTask(target_x, target_y, speed=1))  # Assign a MoveTask
            
            
        elif self.task_type == 'halt':
            pass  # Stay still, no movement
        elif self.task_type == 'move':
            # If the mob has a move task, move it towards the target
            pass

    def complete_task(self):
        #print(f"Completing task of type: {self.task_type}")
        """Handle what happens when the task is complete"""
        if self.task_type == 'move':
            #print("Move task completed.")
            pass
        elif self.task_type == 'idle':
            print("Idle task completed.")

        self.time_left = 0  # Reset time


class MoveTask(Task):
    def __init__(self, target_x, target_y, speed, path=None, duration=0):
        super().__init__('move', duration)
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.path = path if path else []  # Path is optional, will be calculated if not provided
        self.current_path_index = 0  # Start at the first point of the path

    def perform_task(self, mob):
        if self.path:
            self.follow_path(mob)
        else:
            self.move_towards_target(mob)

    def follow_path(self, mob):
        """Follow a pre-defined path"""
        if self.current_path_index < len(self.path):
            target = self.path[self.current_path_index]
            dx = target[0] - mob.rect.x
            dy = target[1] - mob.rect.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > self.speed:
                mob.rect.x += dx / distance * self.speed
                mob.rect.y += dy / distance * self.speed
            else:
                # Reached this point, move to the next point in the path
                self.current_path_index += 1
        else:
            # Path completed
            self.complete_task()

    def move_towards_target(self, mob):
        """Move towards the target position"""
        dx = self.target_x - mob.rect.x
        dy = self.target_y - mob.rect.y
        distance = math.sqrt(dx**2 + dy**2)
        #print(f"Moving towards target: ({self.target_x}, {self.target_y}). Current pos: ({mob.rect.x}, {mob.rect.y}). Distance: {distance}")

        if distance > self.speed:
            mob.rect.x = max(0, min(SCREEN_WIDTH - 10, mob.rect.x + dx / distance * self.speed))
            mob.rect.y = max(0, min(SCREEN_HEIGHT - 10, mob.rect.y + dy / distance * self.speed))
        else:
            # Reached the target
            self.complete_task()

    def complete_task(self):
        super().complete_task()
        #print(f"MoveTask completed. Mob reached ({self.target_x}, {self.target_y}).")