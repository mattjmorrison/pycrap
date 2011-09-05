import re

class Life(object):

    def __init__(self, name):
        self.name = name

    def can_drink(self, liquid):
        return liquid in self.drinks

    def can_eat(self, food):
        return food in self.food

class Animal(Life):
    drinks = ('milk', 'water',)
    food = ('meat', 'potatoes')
    poisons = ('arsenic', )

    def __init__(self, *args, **kwargs):
        self.parents = kwargs.pop('parents', None)
        super(Animal, self).__init__(*args, **kwargs)

    def reproduce(self, mate):
        return Animal(parents=(self, mate))

class HouseCat(Animal):
    food = ('fish', 'birds', 'mice', )
    poisons = ('carnation', 'hyacinth', )

    def speak(self):
        return 'meow'

class Dog(Animal):

    def speak(self):
        return "woof"

class Fish(Animal):

    def speak(self):
        return "bloo dloop"

class Person(Animal):

    def speak(self):
        return "Something interesting"

class ComputerProgrammer(Person):

    def speak(self):
        return "Something nerdy"

    def think(self, problem):
        if isinstance(problem, int):
            return "Math is easy"
        if isinstance(problem, str):
            if problem.endswith("?") and re.match(r'who|what|when|where|why|how', problem):
                return "You have to give me more information."
            else:
                if problem.endswith("!") or problem.endswith("..."):
                    if len(problem) < 10:
                        return "Don't trail off or yell, please."
                    else:
                        raise Exception("Sounds complicated, go on.")
                else:
                    return "I don't know what you're getting at."
        else:
            raise Exception("Does not compute")

    def solve(self, problem):
        result = None
        for i in range(10):
            try:
                result = self.think(problem)
            except Exception:
                pass

        if result:
            return result
        else:
            raise Exception("This problem cannot be solved!")

class Plant(Life):
    drinks = ('water', )
    food = ('sunshine', )

    def __init__(self, *args, **kwargs):
        super(Plant, self).__init__(*args, **kwargs)
        self.plant_power = 1

    def photosynthesize(self):
        self.plant_power += 1

    def reproduce(self):
        return ["seed"]

    def is_posinous(self, animal):
        return self.name in animal.poisons

def create_new_plant(name):
    #comments should be ignored
    new_plant = Plant(name)

    for _ in range(10):
        new_plant.photosynthesize()

    return new_plant
