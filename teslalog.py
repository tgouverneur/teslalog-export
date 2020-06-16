#!/usr/bin/python3

import csv
import requests
import sys
import jsonpickle
import simplejson
import datetime

class TeslaCar(object):
    def __init__(self, data):
        if 'id' in data:
            self.id = data['id']

        if 'vin' in data:
            self.vin = data['vin']

        if 'vehicle_name' in data:
            self.vehicle_name = data['vehicle_name']

        if 'option_codes' in data:
            self.option_codes = data['option_codes']

        if 'monitor_state' in data:
            self.monitor_state = data['monitor_state']

        if 'monitor_drive' in data:
            self.monitor_drive = data['monitor_drive']

        if 'keep_climate_on_until' in data:
            self.keep_climate_on_until = data['keep_climate_on_until']

        if 'gui_distance_units' in data:
            self.gui_distance_units = data['gui_distance_units']

        if 'gui_temperature_units' in data:
            self.gui_temperature_units = data['gui_temperature_units']

        if 'odometer' in data:
            self.odometer = data['odometer']

        if 'battery_range' in data:
            self.battery_range = data['battery_range']

        if 'ideal_battery_range' in data:
            self.ideal_battery_range = data['ideal_battery_range']

        if 'source' in data:
            self.source = data['source']

        self.trips = []
        self.charges = []

    def isCharge(self, id):
        for charge in self.charges:
            if charge.id == id:
                return True
        return False

    def isTrip(self, id):
        for trip in self.trips:
            if trip.id == id:
                return True
        return False

    def __str__(self):
        return '[' + str(self.id) + '][VIN: ' + self.vin + '][Name: ' + self.vehicle_name + ']'

class TeslaCharge(object):
    def __init__(self, data):
        if 'id' in data:
            self.id = data['id']

        if 'car_id' in data:
            self.car_id = data['car_id']

        if 'type' in data:
            self.type = data['type']

        if 'start_timestamp' in data:
            self.start_timestamp = data['start_timestamp']

        if 'end_timestamp' in data:
            self.end_timestamp = data['end_timestamp']

        if 'charge_limit_soc' in data:
            self.charge_limit_soc = data['charge_limit_soc']

        if 'charge_soc' in data:
            self.charge_soc = data['charge_soc']

        if 'name' in data:
            self.name = data['name']

        if 'fast_charger_type' in data:
            self.fast_charger_type = data['fast_charger_type']

        if 'charge_energy_added' in data:
            self.charge_energy_added = data['charge_energy_added']

        if 'charging_state' in data:
            self.charging_state = data['charging_state']

        if 'outlet_kwh' in data:
            self.outlet_kwh = data['outlet_kwh']

        if 'charger_voltage' in data:
            self.charger_voltage = data['charger_voltage']

        if 'charger_actual_current' in data:
            self.charger_actual_current = data['charger_actual_current']

        if 'charger_phases' in data:
            self.charger_phases = data['charger_phases']

        if 'date' in data:
            self.date = data['date']

        self.data = []
        self.streaming = []

    def __str__(self):
        return '[' + datetime.date.fromtimestamp(self.date).isoformat() + '][' + str(self.id) + '][' + self.charge_energy_added + ' Kwh added][' +  str(len(self.data)) + ' data points]'

    def add_data(self, data):
        if 'start_timestamp_ts' in data:
            self.start_timestamp_ts = data['start_timestamp_ts']

        if 'end_timestamp_ts' in data:
            self.end_timestamp_ts = data['end_timestamp_ts']

        if 'charge_km_added_rated' in data:
            self.charge_km_added_rated = data['charge_km_added_rated']

        if 'charge_km_added_ideal' in data:
            self.charge_km_added_ideal = data['charge_km_added_ideal']

        if 'fast_charger_present' in data:
            self.fast_charger_present = data['fast_charger_present']

        if 'max_range_charge_counter' in data:
            self.max_range_charge_counter = data['max_range_charge_counter']

        if 'charge_to_max_range' in data:
            self.charge_to_max_range = data['charge_to_max_range']

        self.data = data['charging_data']

    def add_streaming(self, data):
        self.streaming = data['streaming_data']


class TeslaTrip(object):
    def __init__(self, data):
        if 'id' in data:
            self.id = data['id']

        if 'car_id' in data:
            self.car_id = data['car_id']

        if 'type' in data:
            self.type = data['type']

        if 'start_timestamp' in data:
            self.start_timestamp = data['start_timestamp']

        if 'end_timestamp' in data:
            self.end_timestamp = data['end_timestamp']

        if 'distance' in data:
            self.distance = data['distance']

        if 'odometer_start' in data:
            self.odometer_start = data['odometer_start']

        if 'name' in data:
            self.name = data['name']

        if 'odometer_end' in data:
            self.odometer_end = data['odometer_end']

        if 'whperkm' in data:
            self.whperkm = data['whperkm']

        if 'end_loc' in data:
            self.end_loc = data['end_loc']

        if 'date' in data:
            self.date = data['date']

        self.data = []
        self.climate = []
        self.charging = []

    def end_loc_str(self):
        ret = ''
        if 'pretty' in self.end_loc:
            return self.end_loc['pretty']

        if 'route' in self.end_loc:
            ret = ret + self.end_loc['route'] + ' '

        if 'city' in self.end_loc:
            ret = ret + self.end_loc['city'] + ' '

        if 'country' in self.end_loc:
            ret = ret + self.end_loc['country'] + ' '

        return ret.strip()


    def __str__(self):
        return '[' + datetime.date.fromtimestamp(self.date).isoformat() + '][' + str(self.id) + '][' + self.end_loc_str() + '][' + str(len(self.data)) + ' data points]'


    def add_data(self, data):
        if 'start_timestamp_ts' in data:
            self.start_timestamp_ts = data['start_timestamp_ts']

        if 'end_timestamp_ts' in data:
            self.end_timestamp_ts = data['end_timestamp_ts']

        if 'start_streaming_id' in data:
            self.start_streaming_id = data['start_streaming_id']

        if 'end_streaming_id' in data:
            self.end_streaming_id = data['end_streaming_id']

        if 'kml_key' in data:
            self.kml_key = data['kml_key']

        if 'name' in data:
            self.name = data['name']

        if 'next_trip_id' in data:
            self.next_trip_id = data['next_trip_id']

        if 'prev_trip_id' in data:
            self.prev_trip_id = data['prev_trip_id']

        self.data = data['trip_data']

    def add_charging(self, data):
        self.charging = data['charging_data']

    def add_climate(self, data):
        self.climate = data['climate_data']

class Teslalog(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.r_cookie = None

        self.login()
        self.cars = []

    def login(self):
        if self.r_cookie is not None:
            raise Exception('r_cookie is already set, aborting')


        p_login = {'req': 'login', 'username': self.username}
        d_login = {'password': self.password}

        r = requests.post('https://teslalog.com/mocengine/api.php', params=p_login, data=d_login)
        if r.status_code != requests.codes.ok:
            raise Exception('Cannot login to teslalog')

        r_data = r.json()
        if 'result' not in r_data or 'cookie' not in r_data['result']:
            raise Exception('Cannot find cookie in response')

        self.r_cookie = r_data['result']['cookie']

        p_check = {'req': 'check', 'auth_cookie': self.r_cookie}

        r = requests.get('https://teslalog.com/mocengine/api.php', params=p_check)

        if r.status_code != requests.codes.ok:
            raise Exception('Error while running API check')

    def isCar(self, id):
        for car in self.cars:
            if car.id == id:
                return True
        return False


    def car_list(self, resume=False):
        if self.r_cookie is None:
            raise Exception('r_cookie is not set, aborting')

        headers = {'Cookie': '_tlkk=' + self.r_cookie}
        p_list = {'req': 'car_list'}

        r = requests.get('https://teslalog.com/api.php', headers=headers, params=p_list)
        if r.status_code != requests.codes.ok:
            print('[!] Cannot fetch logs')
            sys.exit(2)

        r_data = r.json()
        if 'status' not in r_data or r_data['status'] != 'success':
            print('[!] Unsuccessful fetching')
            sys.exit(3)

        l_data = r_data['result']['list']

        for car in l_data:
            co = TeslaCar(car)
            if not resume or not self.isCar(co.id):
                self.cars.append(co)

    def fetch_logs(self, car, debug=False, resume=False):
        if self.r_cookie is None:
            raise Exception('r_cookie is not set, aborting')

        d_carid = car.id
        headers = {'Cookie': '_tlkk=' + self.r_cookie}

        p_list = {'req': 'list_day', 'car_id': d_carid, 'offset': -120, 'max_days': '', 'geo_action_id': ''}

        if debug: print('[-] Fetching logs for carid ' + str(d_carid) + '...')

        r = requests.get('https://teslalog.com/api-logs.php', headers=headers, params=p_list)

        if r.status_code != requests.codes.ok:
            raise Exception('Cannot fetch logs')

        r_data = r.json()
        if 'status' not in r_data or r_data['status'] != 'success':
            raise Exception('Unsuccessful fetching')

        l_data = r_data['result']['list_data']

        for day in l_data:
            t_date = day['t_date']

            if debug: print('\t + Fetching logs for day ' + t_date + '...')

            p_listday = {'req': 'list', 'date': t_date, 'car_id': d_carid, 'offset': -120, 'geo_action_id': '' }
            r = requests.get('https://teslalog.com/api-logs.php', headers=headers, params=p_listday)

            if r.status_code != requests.codes.ok:
                raise Exception('Cannot fetch ' + t_date)

            r_data = r.json()

            if debug: print('\t + ' + str(len(r_data['list_data'])) + ' items found for that day')
            for entry in r_data['list_data']:
                if entry['type'] == 'trip':

                    trip = TeslaTrip(entry)

                    if resume and car.isTrip(trip.id):
                        if debug: print('\t + Trip already there, skipping: ' + str(trip.id))
                        continue

                    p_trip = {'req': 'trip', 'car_id': d_carid, 'trip_id': trip.id, 'unit': 'metric'}
                    if debug: print('\t\t> Fetching details on trip_id: ' + str(trip.id))
                    r = requests.get('https://teslalog.com/api-logs.php', headers=headers, params=p_trip)

                    if r.status_code != requests.codes.ok:
                        if debug: print('Cannot fetch ' + t_date + ' / tripid: ' + str(trip_id))
                        continue

                    r_data = r.json()
                    trip.add_data(r_data)

                    p_trip = {'req': 'charging', 'car_id': d_carid, 'start': trip.start_timestamp, 'stop': trip.end_timestamp, 'unit': 'metric'}
                    if debug: print('\t\t> Fetching charging details on trip_id: ' + str(trip.id))
                    r = requests.get('https://teslalog.com/api-logs.php', headers=headers, params=p_trip)

                    if r.status_code != requests.codes.ok:
                        if debug: print('Cannot fetch charging details for ' + t_date + ' / tripid: ' + str(trip_id))
                        continue

                    r_data = r.json()
                    trip.add_charging(r_data)

                    p_trip = {'req': 'climate', 'car_id': d_carid, 'start': trip.start_timestamp, 'stop': trip.end_timestamp, 'unit': 'metric'}
                    if debug: print('\t\t> Fetching climate details on trip_id: ' + str(trip.id))
                    r = requests.get('https://teslalog.com/api-logs.php', headers=headers, params=p_trip)

                    if r.status_code != requests.codes.ok:
                        if debug: print('Cannot fetch climate details for ' + t_date + ' / tripid: ' + str(trip_id))
                        continue

                    r_data = r.json()
                    trip.add_climate(r_data)

                    car.trips.append(trip)
                    if debug: print('\t\t> Trip added: ' + str(trip))

                elif entry['type'] == 'charging':

                    charge = TeslaCharge(entry)

                    if resume and car.isCharge(charge.id):
                        if debug: print('\t + Charging Session already there, skipping: ' + str(charge.id))
                        continue

                    p_trip = {'req': 'charging_session', 'car_id': d_carid, 'charging_session_id': charge.id}

                    if debug: print('\t\t> Fetching details on charging_session_id: ' + str(charge.id))

                    r = requests.get('https://teslalog.com/api-logs.php', headers=headers, params=p_trip)

                    if r.status_code != requests.codes.ok:
                        if debug: print('Cannot fetch ' + t_date + ' / charging_session_id: ' + str(charge.id))
                        continue

                    r_data = r.json()
                    charge.add_data(r_data)

                    p_trip = {'req': 'streaming', 'car_id': d_carid, 'start': charge.start_timestamp, 'stop': charge.end_timestamp}

                    if debug: print('\t\t> Fetching streaming  on charging_session_id: ' + str(charge.id))

                    r = requests.get('https://teslalog.com/api-logs.php', headers=headers, params=p_trip)

                    if r.status_code != requests.codes.ok:
                        if debug: print('Cannot fetch ' + t_date + ' / charging_session_id: ' + str(charge.id))
                        continue

                    r_data = r.json()
                    charge.add_streaming(r_data)

                    car.charges.append(charge)
                    if debug: print('\t\t> Charge added: ' + str(charge))

                else:
                    raise Exception('Unknown type of log found: ' + r_data['list_data'][0]['type'])

    def loads(fname):
        f = open(fname ,'r')
        return jsonpickle.decode(f.read())

    def dumps(self, fname):
        """ Avoid passwords/username/token to be present in the dump... """
        username = self.username
        password = self.password
        token = self.r_cookie

        self.username = self.password = self.r_cookie = None
        content = jsonpickle.encode(self)
        self.username = username
        self.password = password
        self.r_cookie = token

        f = open(fname, 'w')
        f.write(simplejson.dumps(simplejson.loads(content), indent=4, sort_keys=True))
        f.close()

