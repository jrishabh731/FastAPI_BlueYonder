import enum
import re

from pydantic import BaseModel, validator, conint, constr
from datetime import datetime


class FuelTypeEnum(enum.Enum):
    Petrol = "Petrol"
    Diesel = "Diesel"
    PC = "Petrol + CNG"


class EngineInspectionSchema(BaseModel):
    appointmentId: str
    inspectionDate: constr(strip_whitespace=True, min_length=10, max_length=10)
    inspectionStartTime: str
    year: int
    month: conint(gt=0, lt=13)
    engineTransmission_battery_value: str
    engineTransmission_battery_cc_value_0: str
    engineTransmission_battery_cc_value_1: str
    engineTransmission_battery_cc_value_2: str
    engineTransmission_battery_cc_value_3: str
    engineTransmission_battery_cc_value_4: str
    engineTransmission_engineoilLevelDipstick_value: str
    engineTransmission_engineOilLevelDipstick_cc_value_0: str
    engineTransmission_engineOil: str
    engineTransmission_engineOil_cc_value_0: str
    engineTransmission_engineOil_cc_value_1: str
    engineTransmission_engineOil_cc_value_2: str
    engineTransmission_engineOil_cc_value_3: str
    engineTransmission_engineOil_cc_value_4: str
    engineTransmission_engineOil_cc_value_5: str
    engineTransmission_engineOil_cc_value_6: str
    engineTransmission_engineOil_cc_value_7: str
    engineTransmission_engineOil_cc_value_8: str
    engineTransmission_engineOil_cc_value_9: str
    engineTransmission_engine_value: str
    engineTransmission_engine_cc_value_0: str
    engineTransmission_engine_cc_value_1: str
    engineTransmission_engine_cc_value_2: str
    engineTransmission_engine_cc_value_3: str
    engineTransmission_engine_cc_value_4: str
    engineTransmission_engine_cc_value_5: str
    engineTransmission_engine_cc_value_6: str
    engineTransmission_engine_cc_value_7: str
    engineTransmission_engine_cc_value_8: str
    engineTransmission_engine_cc_value_9: str
    engineTransmission_engine_cc_value_10: str
    engineTransmission_coolant_value: str
    engineTransmission_coolant_cc_value_0: str
    engineTransmission_coolant_cc_value_1: str
    engineTransmission_coolant_cc_value_2: str
    engineTransmission_coolant_cc_value_3: str
    engineTransmission_engineMounting_value: str
    engineTransmission_engineMounting_cc_value_0: str
    engineTransmission_engineSound_value: str
    engineTransmission_engineSound_cc_value_0: str
    engineTransmission_engineSound_cc_value_1: str
    engineTransmission_engineSound_cc_value_2: str
    engineTransmission_engineSound_cc_value_3: str
    engineTransmission_engineSound_cc_value_4: str
    engineTransmission_engineSound_cc_value_5: str
    engineTransmission_exhaustSmoke_value: str
    engineTransmission_exhaustSmoke_cc_value_0: str
    engineTransmission_engineBlowByBackCompression_value: str
    engineTransmission_engineBlowByBackCompression_cc_value_0: str
    engineTransmission_clutch_value: str
    engineTransmission_clutch_cc_value_0: str
    engineTransmission_clutch_cc_value_1: str
    engineTransmission_clutch_cc_value_2: str
    engineTransmission_clutch_cc_value_3: str
    engineTransmission_clutch_cc_value_4: str
    engineTransmission_clutch_cc_value_5: str
    engineTransmission_clutch_cc_value_6: str
    engineTransmission_gearShifting_value: str
    engineTransmission_gearShifting_cc_value_0: str
    engineTransmission_gearShifting_cc_value_1: str
    engineTransmission_gearShifting_cc_value_2: str
    engineTransmission_comments_value_0: str
    engineTransmission_comments_value_1: str
    engineTransmission_comments_value_2: str
    engineTransmission_comments_value_3: str
    engineTransmission_comments_value_4: str
    fuel_type: str
    odometer_reading: int
    rating_engineTransmission: float

    def __repr__(self):
        return f"AppointmentID: {self.appointmentId}"

    @validator("inspectionDate", pre=True)
    def date_to_mdy_format(cls, value):
        try:
            value = datetime.strptime(
                    value,
                    "%d-%m-%Y"
                ).strftime("%Y-%m-%d")
        except ValueError as err:
            raise ValueError(
                f"inspectionDate : {value} doesn't match %d-%m-%Y time format"
            ) from err

        return value

    @validator("inspectionStartTime")
    def validate_inspection_starttime(cls, value):
        value = value.split(" ")[-1]
        result = re.match("^([01]?[0-9]|2[0-3]):[0-5][0-9]$", value)
        if result is None:
            raise ValueError(f"inspectionStartTime : {value} doesn't match 24hr time format")
        return value
