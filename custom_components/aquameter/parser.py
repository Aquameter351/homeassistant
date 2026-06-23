from dataclasses import dataclass


@dataclass
class AquaMeterData:
    water: float
    capacity: int
    reserve: int
    flow: float
    today: float
    is_calibrating: bool
    calibration_pulses: int
    language: int


def parse_q_packet(packet: str) -> AquaMeterData | None:
    try:
        parts = packet.strip().split("|")

        if len(parts) != 10:
            return None

        if parts[1] != "Q":
            return None

        return AquaMeterData(
            water=float(parts[2]),
            capacity=int(parts[3]),
            reserve=int(parts[4]),
            flow=float(parts[5]),
            today=float(parts[6]),
            is_calibrating=bool(int(parts[7])),
            calibration_pulses=int(parts[8]),
            language=int(parts[9]),
        )

    except Exception:
        return None