from io import BytesIO

from star_manager.utils.binary_reader import BinaryReader


AIS_CARD_MARKERS = {"\u3010AIS_Chara\u3011", "\u3010AIS_Clothes\u3011"}
MOD_ID_PATTERN = b"ModID"
PNG_IEND_MARKER = b"IEND"


def extract_png_extra_data(file_path):
    """Return the bytes stored after the PNG IEND chunk."""
    with open(file_path, "rb") as file:
        data = file.read()

    iend_type_pos = data.find(PNG_IEND_MARKER)
    if iend_type_pos == -1:
        return b""

    # Keep the CRC bytes in this slice. HS2/AIS card data starts after an
    # 8-byte block that the reader skips in read_card_marker().
    extra_data_start = iend_type_pos + len(PNG_IEND_MARKER)
    return data[extra_data_start:]


def read_card_marker(card_data):
    if len(card_data) < 100:
        return None

    reader = BinaryReader(BytesIO(card_data))
    reader.read_bytes(8)
    return reader.read_string()


def is_ais_card(file_path):
    try:
        marker = read_card_marker(extract_png_extra_data(file_path))
    except Exception:
        return False
    return marker in AIS_CARD_MARKERS


def extract_mod_guids_from_card(file_path):
    card_data = extract_png_extra_data(file_path)
    if read_card_marker(card_data) not in AIS_CARD_MARKERS:
        return set()
    return parse_mod_data(card_data)


def parse_mod_data(card_bytes):
    """Parse HS2 mod identifiers from card binary data."""
    mod_guids = set()
    data = bytearray(card_bytes)
    position = 0

    while position <= len(data) - len(MOD_ID_PATTERN):
        found = data.find(MOD_ID_PATTERN, position)
        if found == -1:
            break

        cursor = found + len(MOD_ID_PATTERN)
        if cursor >= len(data):
            break

        length_prefix = data[cursor]
        cursor += 1

        if length_prefix < 0xC0:
            length = length_prefix - 0xA0
        else:
            if cursor >= len(data):
                break
            length = data[cursor]
            cursor += 1

        if length <= 0 or cursor + length > len(data):
            break

        try:
            mod_guids.add(bytes(data[cursor:cursor + length]).decode("utf-8"))
        except UnicodeDecodeError:
            pass

        position = cursor + length

    return mod_guids
