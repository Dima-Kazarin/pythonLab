from random import choice

AIRPORT_TYPE_DESCRIPTION = {
    'heliport': 'Can hold only helicopters',
    'small_airport': 'Can hold only passenger, non-combat planes',
    'seaplane_base': 'Can hold only Marine adopted planes',
    'medium_airport': 'Can hold only passengers planes',
    'large_airport': 'Can hold anything excluding helicopters'
}


class Airport:
    def __init__(self, id, ident, airport_type, name, coordinates, hangars):
        self.id = f'{id}_{ident}'
        self.airport_type = airport_type
        self.name = name
        self.coordinates = coordinates
        self.hangars = hangars

    def operate_aircraft_landing(self, aircraft):
        if self.check_if_aircraft_can_land(aircraft):
            self.put_vehicle(aircraft)
            return True
        return False

    def operate_aircraft_take_off(self, destination_airport='random'):
        if destination_airport == 'random':
            from despetcher_system import despetcher
            destination_airport = choice(despetcher.airports)
        if any(self.hangars):
            ac = [element for element in self.hangars if element is not None]
            aircraft_to_take_off = choice(ac)
            index = self.hangars.index(aircraft_to_take_off)
            self.hangars[index] = None
            destination_airport.put_vehicle(aircraft_to_take_off)

    def conduct_taking_off(self, destination_airport='random'):
        self.operate_aircraft_take_off(destination_airport)

    def put_vehicle(self, aircraft):
        if None in self.hangars:
            empty_hangar_index = self.hangars.index(None)
            self.hangars[empty_hangar_index] = aircraft
            aircraft.conduct_landing(self)

    def get_number_of_free_hangars(self):
        return self.hangars.count(None)

    def show_aircrafts(self):
        for i, hangar in enumerate(self.hangars):
            if hangar:
                print(f'Hangar {i + 1}: {hangar}')

    def show_airport_type_description(self):
        return AIRPORT_TYPE_DESCRIPTION.get(self.airport_type, 'Unknown type')

    def check_if_aircraft_can_land(self, aircraft):
        allowed_aircraft_types = {
            'heliport': ['helicopter'],
            'small_airport': ['jet', 'turboprop_aircraft', 'piston_aircraft',
                              'wide_body_plane', 'narrow_body_plane', 'cargo',
                              'maritime_patrol', 'water_plane', 'helicopter'],
            'seaplane_base': ['maritime_patrol', 'water_plane'],
            'medium_airport': ['jet', 'turboprop_aircraft', 'piston_aircraft',
                               'wide_body_plane', 'narrow_body_plane'],
            'large_airport': [aircraft.aircraft_type]
        }

        if aircraft.aircraft_type not in allowed_aircraft_types.get(self.airport_type, []):
            return False

        if hasattr(self, 'lines'):
            return int(self.lines[0]) >= aircraft.landing_length and \
                int(self.lines[1]) >= aircraft.width * 0.8

        return True

    def __str__(self):
        return f'Airport {self.name} ({self.airport_type}), ID: {self.id}'

    def __eq__(self, other):
        if isinstance(other, Airport):
            return self.id == other.id
        return False
