from custom_components.aquameter.parser import parse_q_packet


def test_parse_q_packet():
    packet = "v=2|Q|68.47|95|25|0.00|28.60|0|194|0"

    data = parse_q_packet(packet)

    assert data is not None
    assert data.water == 68.47
    assert data.capacity == 95
    assert data.reserve == 25
    assert data.flow == 0.0
    assert data.today == 28.60