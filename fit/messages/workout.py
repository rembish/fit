from fit.messages import Message
from fit.types.extended import Sport, WorkoutCapabilities, MessageIndex, \
    Intensity, WktStepTarget, WktStepDuration
from fit.types.general import UInt16, String, UInt32


class Workout(Message):
    msg_type = 26

    sport = Sport(4)
    capabilities = WorkoutCapabilities(5)
    num_valid_steps = UInt16(6)
    wkt_name = String(8)


class WorkoutStep(Message):
    msg_type = 27

    message_index = MessageIndex(254)
    wkt_step_name = String(0)
    duration_type = WktStepDuration(1)
    duration_value = UInt32(2)  # variants
    target_type = WktStepTarget(3)
    target_value = UInt32(4)  # variants
    custom_target_value_low = UInt32(5)  # variants
    custom_target_value_high = UInt32(6)  # variants
    intensity = Intensity(7)
