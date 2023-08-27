import random
from abc import ABC

from aircraft import Aircraft


class WaterLandingMixin:
    @staticmethod
    def do_water_landing():
        print('Performing water landing')


class BombThrowingMixin:
    @staticmethod
    def throw_bombs():
        print('Throwing bombs')


class PassengerAircraft(Aircraft, ABC):
    def __init__(self, aircraft_id, aircraft_type, width, landing_length, num_of_seats,
                 destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates):
        super().__init__(aircraft_id, aircraft_type, width, landing_length, num_of_seats,
                         destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates)
        self.is_passenger = True
        self.passengers = []

    def release_cabin(self, airport):
        if hasattr(airport, 'passengers'):
            airport.passengers.extend(self.passengers)
            [setattr(passenger, 'place', 'airport') for passenger in airport.passengers]
            self.passengers = []

    def fill_cabin(self, airport):
        num_passengers_to_fill = int(len(airport.passengers) * 0.15)
        passengers_to_fill = airport.passengers[:num_passengers_to_fill]
        [setattr(passenger, 'place', 'aircraft') for passenger in airport.passengers]
        self.passengers.extend(passengers_to_fill)
        airport.passengers = airport.passengers[num_passengers_to_fill:]


class CargoAircraft(Aircraft, ABC):
    def __init__(self, aircraft_id, aircraft_type, width, landing_length, num_of_seats,
                 destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates):
        super().__init__(aircraft_id, aircraft_type, width, landing_length, num_of_seats,
                         destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates)
        self.amount_of_cargo = 0

    def fill_cabin(self, airport):
        available_cargo = random.randint(1, airport.amount_of_cargo)
        self.amount_of_cargo += available_cargo
        airport.amount_of_cargo -= available_cargo

    def release_cabin(self, airport):
        if hasattr(airport, 'amount_of_cargo'):
            released_cargo = self.amount_of_cargo
            self.amount_of_cargo -= released_cargo
            airport.amount_of_cargo += released_cargo


class Jet(PassengerAircraft):
    def __init__(self, aircraft_id, width, landing_length, num_of_seats,
                 destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates):
        super().__init__(aircraft_id, 'jet', width, landing_length, num_of_seats,
                         destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates)

    def apply_aircraft_feature(self):
        print('Applying Jet Aircraft feature')


class TurbopropAircraft(PassengerAircraft):
    def __init__(self, aircraft_id, width, landing_length, num_of_seats,
                 destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates):
        super().__init__(aircraft_id, 'turboprop_aircraft', width, landing_length, num_of_seats,
                         destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates)

    def apply_aircraft_feature(self):
        print('Applying Turboprop Aircraft feature')


class PistonAircraft(PassengerAircraft):
    def __init__(self, aircraft_id, width, landing_length, num_of_seats,
                 destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates):
        super().__init__(aircraft_id, 'piston_aircraft', width, landing_length, num_of_seats,
                         destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates)

    def apply_aircraft_feature(self):
        print('Applying Piston Aircraft feature')


class WideBodyPlane(PassengerAircraft):
    def __init__(self, aircraft_id, width, landing_length, num_of_seats,
                 destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates):
        super().__init__(aircraft_id, 'wide_body_plane', width, landing_length, num_of_seats,
                         destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates)

    def apply_aircraft_feature(self):
        print('Applying Wide-body plane Aircraft feature')


class NarrowBodyPlane(PassengerAircraft):
    def __init__(self, aircraft_id, width, landing_length, num_of_seats,
                 destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates):
        super().__init__(aircraft_id, 'narrow_body_plane', width, landing_length, num_of_seats,
                         destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates)

    def apply_aircraft_feature(self):
        print('Applying Narrow-body plane Aircraft feature')


class Cargo(CargoAircraft):
    def __init__(self, aircraft_id, width, landing_length, num_of_seats,
                 destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates):
        super().__init__(aircraft_id, 'cargo', width, landing_length, num_of_seats,
                         destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates)

    def apply_aircraft_feature(self):
        print('Applying Cargo Aircraft feature')


class MaritimePatrol(Aircraft, WaterLandingMixin):
    def __init__(self, aircraft_id, width, landing_length, num_of_seats,
                 destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates):
        super().__init__(aircraft_id, 'maritime_patrol', width, landing_length, num_of_seats,
                         destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates)
        self.is_marine = True

    def apply_aircraft_feature(self):
        print('Applying Maritime Patrol Aircraft feature')


class WaterPlane(Aircraft, WaterLandingMixin):
    def __init__(self, aircraft_id, width, landing_length, num_of_seats,
                 destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates):
        super().__init__(aircraft_id, 'water_plane', width, landing_length, num_of_seats,
                         destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates)
        self.is_marine = True

    def apply_aircraft_feature(self):
        print('Applying Water-plane Aircraft feature')


class Helicopter(Aircraft):
    def __init__(self, aircraft_id, width, landing_length, num_of_seats,
                 destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates):
        super().__init__(aircraft_id, 'helicopter', width, landing_length, num_of_seats,
                         destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates)

    def apply_aircraft_feature(self):
        print('Applying Helicopter Aircraft feature')


class Fighter(Aircraft, BombThrowingMixin):
    def __init__(self, aircraft_id, width, landing_length, num_of_seats,
                 destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates):
        super().__init__(aircraft_id, 'fighter', width, landing_length, num_of_seats,
                         destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates)
        self.is_combat = True

    def apply_aircraft_feature(self):
        print('Applying Fighter Aircraft feature')


class CombatTransport(Aircraft, BombThrowingMixin):
    def __init__(self, aircraft_id, width, landing_length, num_of_seats,
                 destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates):
        super().__init__(aircraft_id, 'combat_transport', width, landing_length, num_of_seats,
                         destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates)
        self.is_combat = True

    def apply_aircraft_feature(self):
        print('Applying Combat transport Aircraft feature')
