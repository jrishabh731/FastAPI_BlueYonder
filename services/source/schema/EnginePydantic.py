from pydantic import BaseModel, Field
from datetime import date



class EngineInspectionSchema(BaseModel):
    appointmentId: str
    inspectionDate: str
    inspectionStartTime: str
    year: int
    month: int
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


# class EngineInspectionResponse(BaseModel):
#     duplicates: list[str]
#     schema_failures: list[dict]
