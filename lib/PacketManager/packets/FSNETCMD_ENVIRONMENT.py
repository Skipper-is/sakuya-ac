from struct import pack, unpack

class FSNETCMD_ENVIRONMENT: #33
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.day_night = None # 0 is day, 1 is night
        self.flags = {
            "fog":False,
            "blackout":False,
            "midair":False,
            "can_land_anywhere":False
        }
        self.wind = [0,0,0]
        self.visibility = None
        if should_decode:
            self.decode()

    def decode(self):
        variables = unpack("IHHIffff", self.buffer[0:28])
        #0 is the packet type, 1 is just padding.
        self.day_night = variables[2]
        flags = variables[3]
        self.wind = list(variables[4:7])
        self.visibility = variables[7]
        self.flags["fog"] = bool(flags & 1)
        if flags&8 == 1: #Server controls blackout:
            self.flags["blackout"] = bool(flags & 4)
        if flags&32 == 1: #Server controls midair:
            self.flags["midair"] = bool(flags & 16)
        if flags&128 == 1: #Server controls can_land_anywhere:
            self.flags["can_land_anywhere"] = bool(flags & 64)
     
    @staticmethod
    def encode(day_night, fog, blackout, midair, can_land_anywhere, wind, visibility, with_size:bool=False):
        flags = 0
        if fog:
            flags |= 1
        if blackout:
            flags |= 4
            flags |=8
        if midair:
            flags += 16
            flags += 32
        if can_land_anywhere:
            flags += 64
            flags += 128
        buffer = pack("IHHIffff", 33, 0, day_night, flags, *wind, visibility)
        if with_size:
            return pack("I", len(buffer))+buffer
        return buffer

