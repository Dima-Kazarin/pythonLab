from collections import namedtuple
from datetime import datetime, timedelta
from random import choice, sample
from csv import DictReader

from airport_heirs import SmallAirport, MediumAirport, LargeAirport, SeaplaneBase, Heliport
from aircraft_producing_company import AircraftProducingCompany
from seats_passengers import Passenger

Line = namedtuple('Line', ['distance', 'width'])

with open('airports_.csv', 'r', encoding='utf-8') as csv_file:
    reader = DictReader(csv_file)
    rows = list(reader)

airports = []
airports.extend(sample([row for row in rows if row['type'] == 'heliport'], 20))
airports.extend(sample([row for row in rows if row['type'] == 'small_airport'], 20))
airports.extend(sample([row for row in rows if row['type'] == 'seaplane_base'], 20))
airports.extend(sample([row for row in rows if row['type'] == 'medium_airport'], 20))
airports.extend(sample([row for row in rows if row['type'] == 'large_airport'], 20))

AP_TYPE_FILTER = ('small_airport', 'medium_airport', 'large_airport')


class DespetcherSystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DespetcherSystem, cls).__new__(cls)
            cls._instance.aircrafts = []
            cls._instance.airports = []
            cls._instance.passengers = []
            cls._instance.current_time = datetime.now()
        return cls._instance

    def describe_aircraft(self, aircraft_id):
        for aircraft in self.aircrafts:
            if aircraft.aircraft_id == aircraft_id:
                return aircraft

    def describe_passenger(self, passenger_id):
        for passenger in self.passengers:
            if passenger.id == passenger_id:
                return f'Passenger {passenger_id}: {passenger}'

    def describe_airport(self, airport_id):
        for airport in self.airports:
            if airport.id == airport_id:
                return airport

    def initial_setup(self):
        airport_objects = []
        airport_objects.extend(airports)

        for ap in airport_objects:
            if ap['type'] == 'heliport':
                airport = Heliport(ap['id'], ap['ident'], ap['name'],
                                   (ap['latitude_deg'], ap['longitude_deg']), [None] * int(ap['num_hangars']))
            elif ap['type'] == 'small_airport':
                airport = SmallAirport(ap['id'], ap['ident'], ap['name'],
                                       (ap['latitude_deg'], ap['longitude_deg']), [None] * int(ap['num_hangars']))
            elif ap['type'] == 'seaplane_base':
                airport = SeaplaneBase(ap['id'], ap['ident'], ap['name'],
                                       (ap['latitude_deg'], ap['longitude_deg']), [None] * int(ap['num_hangars']))
            elif ap['type'] == 'medium_airport':
                airport = MediumAirport(ap['id'], ap['ident'], ap['name'],
                                        (ap['latitude_deg'], ap['longitude_deg']), [None] * int(ap['num_hangars']))
            elif ap['type'] == 'large_airport':
                airport = LargeAirport(ap['id'], ap['ident'], ap['name'],
                                       (ap['latitude_deg'], ap['longitude_deg']), [None] * int(ap['num_hangars']))
            if hasattr(airport, 'lines'):
                airport.lines = Line(ap.get('runaway_length', None), ap.get('runaway_width', None))
            self.airports.append(airport)

        ac = AircraftProducingCompany()
        for _ in range(20):
            self.aircrafts.append(ac.produce_aircraft('jet'))
            self.aircrafts.append(ac.produce_aircraft('turboprop_aircraft'))
            self.aircrafts.append(ac.produce_aircraft('piston_aircraft'))
            self.aircrafts.append(ac.produce_aircraft('wide_body_plane'))
            self.aircrafts.append(ac.produce_aircraft('narrow_body_plane'))
            self.aircrafts.append(ac.produce_aircraft('cargo'))
            self.aircrafts.append(ac.produce_aircraft('maritime_patrol'))
            self.aircrafts.append(ac.produce_aircraft('water_plane'))
            self.aircrafts.append(ac.produce_aircraft('helicopter'))
            self.aircrafts.append(ac.produce_aircraft('fighter'))
            self.aircrafts.append(ac.produce_aircraft('combat_transport'))

        for aircraft in self.aircrafts:
            ap = choice(self.airports)
            aircraft.actual_coordinates = ap.coordinates
            ap.operate_aircraft_landing(aircraft)

        for _ in range(500):
            passenger = Passenger('airport')
            self.passengers.append(passenger)

        for passenger in self.passengers:
            if ap := choice([ap for ap in self.airports if ap.airport_type in AP_TYPE_FILTER]):
                ap.passengers.append(passenger)

    def show_situation(self):
        all_ap = []
        hangar = {}
        passenger_ap = {}

        for airport in self.airports:
            all_ap.append(airport.name)

        for airport in self.airports:
            non_none_hangars = list(filter(lambda h: h is not None, airport.hangars))
            if non_none_hangars:
                hangar[airport.name] = non_none_hangars

        for airport in self.airports:
            if hasattr(airport, 'passengers'):
                passenger_ap[airport.name] = airport.passengers

        print(f'All airports:\n{all_ap}\n')
        print(f'Aircrafts in airport hangars:\n{hangar}\n')
        print(f'Passengers in the airport:\n{passenger_ap}')

    def change_time(self, time_elapsed):
        if time_elapsed < 0:
            raise ValueError('Parameter cannot be negative')

        self.current_time += timedelta(hours=time_elapsed)

        for aircraft in self.aircrafts:
            if aircraft.status() == 'in air':
                aircraft.recalculate_position(time_elapsed)
                if aircraft.actual_coordinates == aircraft.destination_coordinates:
                    airport = next((ap for ap in self.airports if ap.coordinates == aircraft.destination_coordinates),
                                   None)
                    if airport:
                        airport.operate_aircraft_landing(aircraft)

        num_takeoffs = int(len(self.aircrafts) * 0.1)

        for _ in range(num_takeoffs):
            random_airport = choice(self.airports)
            if any(random_airport.hangars):
                random_airport.conduct_taking_off()


despetcher = DespetcherSystem()
