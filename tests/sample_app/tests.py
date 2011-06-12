import unittest

import life

class AnimalTests(unittest.TestCase):

    def test_animal_sets_name_in_constructor(self):
        name = 'steve'
        sample = life.Animal(name)
        self.assertEqual(name, sample.name)

    def test_animal_can_drink_milk(self):
        sample = life.Animal('carl')
        self.assertTrue(sample.can_drink('milk'))

class PlantTests(unittest.TestCase):

    def test_plant_can_drink_water(self):
        plant = life.Plant("tree")
        self.assertTrue(plant.can_drink('water'))

    def test_plant_can_not_drink_milk(self):
        plant = life.Plant("tree")
        self.assertFalse(plant.can_drink('milk'))

if __name__ == '__main__':
    unittest.main()