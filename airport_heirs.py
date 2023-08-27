from airport import Airport


class RegularAirport(Airport):
    def __init__(self, id, ident, airport_type, name, coordinates, hangars):
        super().__init__(id, ident, airport_type, name, coordinates, hangars)
        self.passengers = []
        self.amount_of_cargo = 0
        self.lines = []

    def take_passengers(self, passengers):
        self.passengers.extend(passengers)

    def move_passengers_to_aircraft(self, aircraft, passengers):
        if self.passengers and self.hangars.count(None) > 0:
            num_passengers_to_move = min(len(self.passengers), passengers, self.hangars.count(None))
            passengers_to_move = self.passengers[:num_passengers_to_move]
            self.passengers = self.passengers[num_passengers_to_move:]
            aircraft.passengers.extend(passengers_to_move)

    def take_cargo(self, amount):
        self.amount_of_cargo += amount

    def ship_cargo_to_aircraft(self, aircraft, amount):
        if self.amount_of_cargo >= amount and self.hangars.count(None) > 0:
            self.amount_of_cargo -= amount
            aircraft.amount_of_cargo += amount


class Heliport(Airport):
    def __init__(self, id, ident, name, coordinates, hangars):
        super().__init__(id, ident, 'heliport', name, coordinates, hangars)


class SmallAirport(RegularAirport):
    def __init__(self, id, ident, name, coordinates, hangars):
        super().__init__(id, ident, 'small_airport', name, coordinates, hangars)


class SeaplaneBase(Airport):
    def __init__(self, id, ident, name, coordinates, hangars):
        super().__init__(id, ident, 'seaplane_base', name, coordinates, hangars)


class MediumAirport(RegularAirport):
    def __init__(self, id, ident, name, coordinates, hangars):
        super().__init__(id, ident, 'medium_airport', name, coordinates, hangars)


class LargeAirport(RegularAirport):
    def __init__(self, id, ident, name, coordinates, hangars):
        super().__init__(id, ident, 'large_airport', name, coordinates, hangars)
