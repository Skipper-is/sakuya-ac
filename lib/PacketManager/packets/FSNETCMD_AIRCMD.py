from struct import pack, unpack
from .constants import AIRCMD_KEYWORDS

class FSNETCMD_AIRCMD: #30

    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.aircraft_id = None
        self.message = None
        self.command = None
        if should_decode:
            self.decode()

    def decode(self):
        self.aircraft_id = unpack("I", self.buffer[4:8])[0]
        self.message = self.buffer[8:].decode("utf-8").strip("\x00")
        if self.message.startswith('*'):
            self.command = self.get_command_from_message(self.message)

    def get_command_from_message(self, message:str):
        """
            If the messages are prefixed with a *, then it is usually an engine/.dat
            command, such as WEIGFUEL being the weight of the fuel.
            Command would be something like *43 1000
            """
        message = message[1:]
        engine_code = message.split(" ")[0]
        try:
            command = int(engine_code)
            command = AIRCMD_KEYWORDS[command]
        except ValueError:
            return None
        value = message.split(" ")[1]
        return command, value

    @staticmethod
    def encode(aircraft_id:int, message:str, with_size:bool=False):
        buffer = pack("I",30)+pack("I",aircraft_id)+message.encode("utf-8")
        buffer = buffer + b"\x00" #Last padding
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer

    @staticmethod
    def setPayload(aircraft_id:int, payload:int, units:str='kg', with_size:bool=False):
        """
        This will set the payload of the aircraft, useful if you want to
        load or unload passengers/cargo - for YSRP I use this to load and unload
        on mission start and end.
        """
        payload = str(payload)
        message = f"INITLOAD {payload} {units}"
        return FSNETCMD_AIRCMD.encode(aircraft_id, message, with_size)

    def __str__(self):
        return "Aircraft ID : {self.aircraft_id}; Message : {self.message}; Command : {self.command}"
