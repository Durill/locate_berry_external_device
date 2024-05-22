import time
from dataclasses import dataclass
from typing import Dict, List, Optional

from helpers.logger import CustomLogger
from localization import ILocalization
from serial import Serial

__all__ = (
    "LocalizationPoint",
    "Localization",
)


@dataclass
class LocalizationPoint:
    longitude: float
    latitude: float


class Localization(ILocalization):
    class ATCommands:
        SET_PORT = 'AT+CGNSCFG=1'
        SUPPLY_POWER = 'AT+CGNSPWR=1'
        GET_ACTUAL_LOCALIZATION = 'AT+CGNSTST=1,1'

    details_names = [
        'timestamp',
        'latitude',
        'latitude_direction',
        'longitude',
        'longitude_direction',
        'quality_indicator',
        'number_of_satellites',
        'HDOP',
        'altitude',
        'geoidal_separation',
        'unit_of_geoidal_separation',
        'age_of_correction',
        'station_ID',
        'checksum'
    ]
    previous_update_ending_point: LocalizationPoint = None

    def __init__(self, logger: CustomLogger):
        self.serial_port = Serial(port='/dev/ttyS0', baudrate=9600, timeout=2)
        self.logger = logger

    def set_and_power_module(self) -> None:
        gnss_data_port_setted = self._send_command(self.ATCommands.SET_PORT)
        if self._parse_statuses(raw_response=gnss_data_port_setted)['status'] == 'OK':
            self.logger.log_to_file_and_screen('GNSS data port has been set')
        else:
            self.logger.log_to_file_and_screen('ERROR, while turning on GNSS, data port')

        gnss_power_supply = self._send_command(self.ATCommands.SUPPLY_POWER)
        if self._parse_statuses(raw_response=gnss_power_supply)['status'] == 'OK':
            self.logger.log_to_file_and_screen('GNSS supplied in power')
        else:
            self.logger.log_to_file_and_screen('ERROR, while supplying power to GNSS module')

    def get_actual_localization(self) -> Optional[List[LocalizationPoint]]:
        localization_points = []

        if self.previous_update_ending_point:
            localization_points.append(self.previous_update_ending_point)

        while len(localization_points) <= 3:
            gnss_localization_data = self._send_command(self.ATCommands.GET_ACTUAL_LOCALIZATION)

            listed_data = gnss_localization_data.split('\n')
            localization_raw: List[str] = []
            sorted_localization_data: Dict[str, str] = {}

            for data in listed_data:
                if data.startswith('$GNGGA'):
                    data = data.removeprefix('$GNGGA,')
                    localization_raw = data.split(',')
                    break

            for i in range(len(localization_raw)):
                sorted_localization_data[self.details_names[i]] = localization_raw[i]

            if len(sorted_localization_data['latitude']) < 1 or len(sorted_localization_data['longitude']) < 1:
                continue

            single_point = self._parse_localization_to_point(
                latitude=float(sorted_localization_data['latitude']),
                longitude=float(sorted_localization_data['longitude']),
            )
            if single_point:
                localization_points.append(single_point)

        return localization_points

    def _parse_localization_to_point(self, latitude: float, longitude: float) -> LocalizationPoint:
        latitude_degree = int(latitude // 100)
        latitude_minutes = latitude % 100
        latitude_decimal_degree = latitude_degree + (latitude_minutes / 60)

        longitude_degree = int(longitude // 100)
        longitude_minutes = longitude % 100
        longitude_decimal_degree = longitude_degree + (longitude_minutes / 60)

        result_point = LocalizationPoint(longitude=longitude_decimal_degree, latitude=latitude_decimal_degree)
        return result_point

    def _parse_statuses(self, raw_response: str) -> Dict[str, str]:
        formatted_data = raw_response.split('\n')

        return {'command': formatted_data[0].replace('\r', ''), 'status': formatted_data[1].replace('\r', '')}

    def _send_command(self, command: str):
        self.serial_port.write((command + '\r\n').encode())
        time.sleep(2.5)
        return self.serial_port.read_all().decode()
