from datetime import datetime
from random import randint, uniform

from aircraft_heirs import (Jet, TurbopropAircraft, PistonAircraft, Cargo,
                            Helicopter, WideBodyPlane, NarrowBodyPlane,
                            WaterPlane, Fighter, CombatTransport, MaritimePatrol)


class AircraftProducingCompany:
    def __init__(self):
        self.aircraft_count = 0

    def produce_aircraft(self, aircraft_type):
        self.aircraft_count += 1
        unique_id = self.aircraft_count

        aircraft_type_details = {
            'jet':
                {
                    'width_range': (1, 5),
                    'num_of_seats_range': (5, 7),
                    'speed_range': (640, 960),
                    'landing_distance_range': (1000, 1800)
                },
            'turboprop_aircraft':
                {
                    'width_range': (3, 7),
                    'num_of_seats_range': (50, 100),
                    'speed_range': (300, 550),
                    'landing_distance_range': (2000, 3000)
                },
            'piston_aircraft':
                {
                    'width_range': (5, 5),
                    'num_of_seats_range': (20, 50),
                    'speed_range': (200, 320),
                    'landing_distance_range': (500, 1500)
                },
            'wide_body_plane':
                {
                    'width_range': (20, 35),
                    'num_of_seats_range': (230, 350),
                    'speed_range': (700, 900),
                    'landing_distance_range': (3000, 4000)
                },
            'narrow_body_plane':
                {
                    'width_range': (10, 20),
                    'num_of_seats_range': (140, 210),
                    'speed_range': (800, 1000),
                    'landing_distance_range': (2000, 3500)
                },
            'cargo':
                {
                    'width_range': (5, 20),
                    'num_of_seats_range': (0, 0),
                    'speed_range': (400, 600),
                    'landing_distance_range': (2000, 3000)
                },
            'maritime_patrol':
                {
                    'width_range': (0, 0),
                    'num_of_seats_range': (0, 0),
                    'speed_range': (100, 250),
                    'landing_distance_range': (0, 0)
                },
            'water_plane':
                {
                    'width_range': (0, 0),
                    'num_of_seats_range': (0, 0),
                    'speed_range': (70, 150),
                    'landing_distance_range': (0, 0)
                },
            'helicopter':
                {
                    'width_range': (0, 0),
                    'num_of_seats_range': (0, 0),
                    'speed_range': (150, 450),
                    'landing_distance_range': (0, 0)
                },
            'fighter':
                {
                    'width_range': (2, 7),
                    'num_of_seats_range': (0, 0),
                    'speed_range': (700, 1200),
                    'landing_distance_range': (0, 0)
                },
            'combat_transport':
                {
                    'width_range': (10, 20),
                    'num_of_seats_range': (0, 0),
                    'speed_range': (400, 600),
                    'landing_distance_range': (0, 0)
                }
        }

        air_class = {
            'jet': Jet,
            'turboprop_aircraft': TurbopropAircraft,
            'piston_aircraft': PistonAircraft,
            'wide_body_plane': WideBodyPlane,
            'narrow_body_plane': NarrowBodyPlane,
            'cargo': Cargo,
            'maritime_patrol': MaritimePatrol,
            'water_plane': WaterPlane,
            'helicopter': Helicopter,
            'fighter': Fighter,
            'combat_transport': CombatTransport
        }

        details = aircraft_type_details[aircraft_type]
        aircraft_class = air_class[aircraft_type]

        width = randint(*details['width_range'])
        num_of_seats = randint(*details['num_of_seats_range'])
        speed = randint(*details['speed_range'])
        landing_distance = randint(*details['landing_distance_range'])

        destination_coordinates = (uniform(-90, 90), uniform(-180, 180))
        departure_coordinates = (uniform(-90, 90), uniform(-180, 180))
        departure_time = datetime.now()
        actual_coordinates = (None, None)

        aircraft = aircraft_class(unique_id, width, landing_distance, num_of_seats,
                                  destination_coordinates, departure_coordinates,
                                  departure_time, speed, actual_coordinates)

        return aircraft
