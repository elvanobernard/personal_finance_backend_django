class Car:
    def __init__(self, name):
        self.name = name
        self.type = 'Car'

    def __str__(self) -> str:
        return self.name

    def print_type(self):
        print('called from car')

class TypeCheck:
    def check_type(self):
        self.print_type()

class MyCar(Car, TypeCheck):
    def __init__(self, name):
        super().__init__(name)

if __name__ == '__main__':
    my_car = MyCar('Marchi')
    print(my_car)
    my_car.check_type()