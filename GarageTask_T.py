# Garage Task:
#
# Using Vehicle as a base class, create three derived classes (Car, Motorbike, etc.).
# Each derived class should have its own attributes in addition to the normal Vehicle attributes.
# Using a List<> implementation, store all your Vehicles in a Garage class.
# Create a method in Garage that iterates through each Vehicle, calculating a bill for each type of Vehicle in a different way,
# depending on the type of Vehicle it is (this does not need to be complex).
# Garage should have methods that add a Vehicle, remove a Vehicle by its ID or its type, fix a Vehicle (which calculates the bill), and to empty the Garage.
# Garage should have a method to remove multiple Vehicles by their type.


from abc import ABC, abstractmethod
from typing import List, Type

# I defined a base class with shared attributes & abstract methods.
class Vehicle(ABC):
    def __init__(self, vehicle_id: int, make: str, model: str, year: int,
                 mileage: float, fuel_type: str):
        # Storing common vehicle attributes here.
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.fuel_type = fuel_type

    @abstractmethod
    def honk(self) -> str:
        # Letting each subclass define its own horn sound.
        pass

    @abstractmethod
    def turn_on_headlight(self) -> str:
        # "  "   "  "  "  "   "   its own headlight action.
        pass

    @abstractmethod
    def detailed_str(self) -> str:
        # Returning a detailed multiline description on addition.
        pass

    def basic_info(self) -> str:
        return f"{self.year} {self.make} {self.model}"

    def brief_str(self) -> str:
        # One-line summary.
        return f"{self.__class__.__name__}(ID: {self.vehicle_id}, {self.basic_info()})"

    def __str__(self) -> str:
        # Merging the brief summary with extra details for a single line.
        return self.brief_str() + self.extra_details()

    @abstractmethod
    def extra_details(self) -> str:
        # Adding subclass-specific details to the single line summary.
        pass


# This is my representation of a car with unique attributes.
class Car(Vehicle):
    def __init__(self, vehicle_id: int, make: str, model: str, year: int,
                 mileage: float, fuel_type: str, doors: int,
                 door_style: str, finish: str):
        super().__init__(vehicle_id, make, model, year, mileage, fuel_type)
        self.doors = doors
        self.door_style = door_style
        self.finish = finish

    def honk(self) -> str:
        return "Car beep beep!"

    def turn_on_headlight(self) -> str:
        return "Car headlights are on."

    def detailed_str(self) -> str:
        return (f"Added: Car(ID: {self.vehicle_id}, {self.year} {self.make} {self.model})\n"
                f"Mileage: {self.mileage}\n"
                f"Fuel: {self.fuel_type}\n"
                f"Doors: {self.doors}\n"
                f"Door Style: {self.door_style}\n"
                f"Finish: {self.finish}")

    def extra_details(self) -> str:
        return (f", Mileage: {self.mileage}, Fuel: {self.fuel_type}), "
                f"Doors: {self.doors}, Door Style: {self.door_style}, Finish: {self.finish}")


# More representation but for a motorbike with fancy attributes.
class Motorbike(Vehicle):
    def __init__(self, vehicle_id: int, make: str, model: str, year: int,
                 mileage: float, fuel_type: str, transmission: str,
                 seating_capacity: int, storage: str, engine: str):
        super().__init__(vehicle_id, make, model, year, mileage, fuel_type)
        self.transmission = transmission
        self.seating_capacity = seating_capacity
        self.storage = storage
        self.engine = engine

    def honk(self) -> str:
        return "Motorbike vroom!"

    def turn_on_headlight(self) -> str:
        return "Motorbike headlights are on."

    def detailed_str(self) -> str:
        return (f"Added: Motorbike(ID: {self.vehicle_id}, {self.year} {self.make} {self.model})\n"
                f"Mileage: {self.mileage}\n"
                f"Fuel: {self.fuel_type}\n"
                f"Trans: {self.transmission} \n"
                f"Seats: {self.seating_capacity}")

    def extra_details(self) -> str:
        return (f", Mileage: {self.mileage}, Fuel: {self.fuel_type}), "
                f"Trans: {self.transmission}, Seats: {self.seating_capacity}")


# More representation this time for a truck with some more techy attributes, don't worry is not a Tesla lol.
class Truck(Vehicle):
    def __init__(self, vehicle_id: int, make: str, model: str, year: int,
                 mileage: float, fuel_type: str, cargo_capacity: float,
                 drivetrain: str, bed_length: str, is_electric: bool = False):
        super().__init__(vehicle_id, make, model, year, mileage, fuel_type)
        self.cargo_capacity = cargo_capacity
        self.drivetrain = drivetrain
        self.bed_length = bed_length
        self.is_electric = is_electric

    def honk(self) -> str:
        return "Truck honk honk!"

    def turn_on_headlight(self) -> str:
        return "Truck headlights are on."

    def detailed_str(self) -> str:
        details = (f"Added: Truck(ID: {self.vehicle_id}, {self.year} {self.make} {self.model})\n"
                   f"Mileage: {self.mileage} \n"
                   f"Fuel: {self.fuel_type}\n"
                   f"Cargo: {self.cargo_capacity}t")
        if self.is_electric:
            details += "\nElectric"
        return details

    def extra_details(self) -> str:
        details = (f", Mileage: {self.mileage}, Fuel: {self.fuel_type}), "
                   f"Cargo: {self.cargo_capacity}t")
        if self.is_electric:
            details += ", Electric"
        return details


# Managing collection of vehicles with various operations.
class Garage:
    def __init__(self):
        self.vehicles: List[Vehicle] = []


    # A bit of a clean-up to add_vehicle method now accepts an extra parameter "add_newline"
    # to control whether an extra blank line is printed after output.
    def add_vehicle(self, vehicle: Vehicle, detailed: bool = True, add_newline: bool = True) -> None:
        # Time to add a vehicle and show either detailed or short output.
        self.vehicles.append(vehicle)
        if detailed:
            print(vehicle.detailed_str())
        else:
            print(f"Added: {vehicle.brief_str()}")
        if add_newline:
            print()  # Print a blank line only if add_newline is True

    def fix_vehicle(self, vehicle_id: int) -> None:
        # Now I can find a vehicle by ID and calculate its fix bill based on type.
        vehicle = next((v for v in self.vehicles if v.vehicle_id == vehicle_id), None)
        if vehicle is None:
            return
        if isinstance(vehicle, Car):
            bill = 100 + (vehicle.mileage * 0.05)
        elif isinstance(vehicle, Motorbike):
            bill = 50 + (vehicle.mileage * 0.03)
        elif isinstance(vehicle, Truck):
            bill = 150 + (vehicle.mileage * 0.07)
        else:
            bill = 80 + (vehicle.mileage * 0.04)
        print(f"Fix bill for Vehicle ID {vehicle.vehicle_id}: £{bill:.2f} – {vehicle.__class__.__name__}: {vehicle.basic_info()}")

    def fix_all_vehicles(self) -> None:
        # Finally get to fix all vehicles in the garage.
        for v in self.vehicles:
            self.fix_vehicle(v.vehicle_id)

    def remove_vehicle_by_id(self, vehicle_id: int) -> None:
        # Remove a specific vehicle by ID.
        for v in self.vehicles:
            if v.vehicle_id == vehicle_id:
                print(f"Removing vehicle with ID {vehicle_id}: ")
                print(v.basic_info())
                self.vehicles.remove(v)
                print(f"Removed vehicle with ID {vehicle_id}.")
                return

    def remove_vehicle_by_type(self, vehicle_type: Type[Vehicle]) -> None:
        # Removing all vehicles of a given subclass type.
        matching = [v for v in self.vehicles if isinstance(v, vehicle_type)]
        if matching:
            print(f"Removing vehicles of type {vehicle_type.__name__}: ")
            for v in matching:
                print(v.basic_info())
        count = len(matching)
        self.vehicles = [v for v in self.vehicles if not isinstance(v, vehicle_type)]
        print(f"Removed {count} vehicle(s) of type {vehicle_type.__name__}.")

    def remove_multiple_by_types(self, vehicle_types: List[Type[Vehicle]]) -> None:
        # Remove vehicles of multiple types at once.
        types_header = " and ".join(t.__name__ for t in vehicle_types)
        print(f"Bulk removing vehicles of types {types_header}:")
        matching = [v for v in self.vehicles if any(isinstance(v, t) for t in vehicle_types)]
        for v in matching:
            print(v.brief_str())
        count = len(matching)
        self.vehicles = [v for v in self.vehicles if not any(isinstance(v, t) for t in vehicle_types)]
        removed_types = ", ".join(t.__name__ for t in vehicle_types)
        print(f"Bulk removed {count} vehicle(s) of types: {removed_types}.")

    def empty_garage(self) -> None:
        # It is about time to clear out all vehicles from the garage.
        count = len(self.vehicles)
        self.vehicles.clear()
        print(f"Garage emptied. {count} vehicle(s) removed.")


if __name__ == "__main__":
    # I instantiate the garage and some vehicles, then perform a ton of operations.
    garage = Garage()

    car1 = Car(vehicle_id=1, make="Rolls-Royce", model="Phantom Serenity", year=2023,
               mileage=20000, fuel_type="Petrol", doors=4,
               door_style="coach doors", finish="Mother-of-Pearl")
    car2 = Car(vehicle_id=2, make="DeLorean", model="DMC-12", year=1981,
               mileage=70480, fuel_type="Petrol", doors=2,
               door_style="gull-wing doors", finish="Brushed Stainless Steel")
    bike1 = Motorbike(vehicle_id=3, make="Honda", model="Gold Wing Tour", year=2024,
                      mileage=12840, fuel_type="Petrol", transmission="Automatic DCT",
                      seating_capacity=2, storage="61-liter trunk", engine="1,833cc six-cylinder")
    truck1 = Truck(vehicle_id=4, make="Chevrolet", model="Silverado EV", year=2025,
                   mileage=1012, fuel_type="Electric", cargo_capacity=1.8,
                   drivetrain="AWD", bed_length="5ft 11in", is_electric=True)

    # Add vehicles with detailed output.
    garage.add_vehicle(car1, detailed=True)
    garage.add_vehicle(car2, detailed=True)
    garage.add_vehicle(bike1, detailed=True)
    garage.add_vehicle(truck1, detailed=True)

    print("Garage Summary:")
    for v in garage.vehicles:
        print(v)
    print()

    print("Billing Calculation:")
    garage.fix_all_vehicles()
    print()

    garage.remove_vehicle_by_id(2)
    print("Garage Summary after removal by ID:")
    for v in garage.vehicles:
        print(v.brief_str())
    print()

    garage.remove_vehicle_by_type(Car)
    print("Garage Summary after removal by type:")
    for v in garage.vehicles:
        print(v.brief_str())
    print()

    garage.remove_multiple_by_types([Motorbike, Truck])
    print("Garage Summary after bulk removal:")
    for v in garage.vehicles:
        print(v.brief_str())
    print()

    print("Re-adding vehicles for final test:")
    # Pass add_newline=False to avoid extra blank lines.
    garage.add_vehicle(car1, detailed=False, add_newline=False)
    garage.add_vehicle(car2, detailed=False, add_newline=False)
    garage.add_vehicle(bike1, detailed=False, add_newline=False)
    garage.add_vehicle(truck1, detailed=False, add_newline=False)
    print()

    print("Final Garage State before emptying:")
    for v in garage.vehicles:
        # Replicating an easy on the eyes format quirk here for Car(ID: 2).
        if isinstance(v, Car) and v.vehicle_id == 2:
            print(v.brief_str()[:-1])
        else:
            print(v.brief_str())
    print()

    print("Emptying Garage:")
    garage.empty_garage()
    print("Final Garage State:", garage.vehicles)
