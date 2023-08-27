from datetime import timedelta

from pyproj import Geod
from abc import abstractmethod
from random import choice

from seats_passengers import Seats, Passenger

CLASS_TYPE = ('business', 'econom')


class Aircraft:
    geod = Geod(ellps='WGS84')

    def __init__(self, aircraft_id, aircraft_type, width, landing_length, num_of_seats,
                 destination_coordinates, departure_coordinates, departure_time, speed, actual_coordinates):
        self.aircraft_id = aircraft_id
        self.aircraft_type = aircraft_type
        self.width = width
        self.landing_length = landing_length
        self.num_of_seats = num_of_seats
        self.seats = [[Seats(choice(CLASS_TYPE), row, chr(ord('a') + pos), f'{row}_{chr(ord("a") + pos)}',
                             Passenger('airport')) for pos in range(6)]
                      for row in range(1, self.num_of_seats + 1)]
        self.destination_coordinates = destination_coordinates
        self.departure_coordinates = departure_coordinates
        self.departure_time = departure_time
        self.speed = speed
        self.actual_coordinates = actual_coordinates
        self.percent_distance = 0

    def status(self):
        return 'in airport' if self.actual_coordinates in (self.departure_coordinates, self.destination_coordinates) \
            else 'in air'

    def come_back(self):
        self.departure_coordinates, self.destination_coordinates = \
            self.destination_coordinates, self.departure_coordinates

    def update_percent_distance(self):
        _, _, distance_along_track = self.geod.inv(
            self.departure_coordinates[1], self.departure_coordinates[0],
            self.actual_coordinates[1], self.actual_coordinates[0]
        )

        _, _, total_distance = self.geod.inv(
            self.departure_coordinates[1], self.departure_coordinates[0],
            self.destination_coordinates[1], self.destination_coordinates[0]
        )

        self.percent_distance = (distance_along_track / total_distance) * 100

    def print_info(self, airport):
        print(f'Status: {self.status()}')
        if self.status() == 'in airport':
            print(f'Airport name - {airport.name}')
            print(f'Coordinates - {airport.coordinates}')
            hangars_with_aircraft = [hangar for hangar in airport.hangars if hangar == self]
            print(f'Hangar - {hangars_with_aircraft[0]}')
        elif self.status() == 'in air':
            print(f'Coordinates - {self.actual_coordinates}')
            self.update_percent_distance()
            print(f'Percent of passed distance - {self.percent_distance:.2f}%')

    def conduct_landing(self, airport):
        fields_to_reset = ['destination_coordinates', 'departure_coordinates']
        self.actual_coordinates = airport.coordinates
        for field in fields_to_reset:
            setattr(self, field, None)

        if hasattr(self, 'release_cabin'):
            self.release_cabin(airport)

    def conduct_taking_off(self, airport):
        self.actual_coordinates = self.departure_coordinates
        self.percent_distance = 0

        if hasattr(self, 'fill_cabin'):
            self.fill_cabin(airport)

    def recalculate_position(self, time_elapsed):
        if self.status() == 'in air' and self.destination_coordinates is not None:
            az12, az21, distance = self.geod.inv(
                self.actual_coordinates[1], self.actual_coordinates[0],
                self.destination_coordinates[1], self.destination_coordinates[0]
            )
            distance_to_travel = self.speed * time_elapsed
            self.departure_time += timedelta(hours=time_elapsed)
            if distance_to_travel >= distance:
                self.actual_coordinates = self.destination_coordinates
                self.percent_distance = 100.0
            else:
                lon, lat, _ = self.geod.fwd(
                    self.actual_coordinates[1], self.actual_coordinates[0],
                    az12, distance_to_travel
                )
                self.actual_coordinates = (lat, lon)
                self.update_percent_distance()

    @abstractmethod
    def apply_aircraft_feature(self):
        pass

    def __str__(self):
        return f'ID - {self.aircraft_id} (type - {self.aircraft_type})'
