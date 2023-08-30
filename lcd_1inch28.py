from machine import Pin, SPI, PWM
import framebuf
import time

DC = 8
CS = 9
SCK = 10
MOSI = 11
RST = 12
BL = 25


class Lcd1inch28(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 240

        self.cs = Pin(CS, Pin.OUT)
        self.rst = Pin(RST, Pin.OUT)

        self.cs(1)
        self.spi = SPI(1, 100_000_000, polarity=0, phase=0, sck=Pin(SCK), mosi=Pin(MOSI), miso=None)
        self.dc = Pin(DC, Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        self.red = self.colour(255, 0, 0)
        self.green = self.colour(0, 255, 0)
        self.blue = self.colour(0, 0, 255)
        self.white = self.colour(255, 255, 255)

        self.fill(self.white)
        self.show()

        self.pwm = PWM(Pin(BL))
        self.pwm.freq(5000)
        self.font = {}
        #with open('font.json', 'r') as f:
            #self.font = json.load(f)

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def set_bl_pwm(self, duty):
        self.pwm.duty_u16(duty)  # max 65535

    def init_display(self):
        """Initialize display"""
        self.rst(1)
        time.sleep(0.01)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        time.sleep(0.05)

        self.write_cmd(0xEF)
        self.write_cmd(0xEB)
        self.write_data(0x14)

        self.write_cmd(0xFE)
        self.write_cmd(0xEF)

        self.write_cmd(0xEB)
        self.write_data(0x14)

        self.write_cmd(0x84)
        self.write_data(0x40)

        self.write_cmd(0x85)
        self.write_data(0xFF)

        self.write_cmd(0x86)
        self.write_data(0xFF)

        self.write_cmd(0x87)
        self.write_data(0xFF)

        self.write_cmd(0x88)
        self.write_data(0x0A)

        self.write_cmd(0x89)
        self.write_data(0x21)

        self.write_cmd(0x8A)
        self.write_data(0x00)

        self.write_cmd(0x8B)
        self.write_data(0x80)

        self.write_cmd(0x8C)
        self.write_data(0x01)

        self.write_cmd(0x8D)
        self.write_data(0x01)

        self.write_cmd(0x8E)
        self.write_data(0xFF)

        self.write_cmd(0x8F)
        self.write_data(0xFF)

        self.write_cmd(0xB6)
        self.write_data(0x00)
        self.write_data(0x20)

        self.write_cmd(0x36)
        self.write_data(0x98)

        self.write_cmd(0x3A)
        self.write_data(0x05)

        self.write_cmd(0x90)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08)

        self.write_cmd(0xBD)
        self.write_data(0x06)

        self.write_cmd(0xBC)
        self.write_data(0x00)

        self.write_cmd(0xFF)
        self.write_data(0x60)
        self.write_data(0x01)
        self.write_data(0x04)

        self.write_cmd(0xC3)
        self.write_data(0x13)
        self.write_cmd(0xC4)
        self.write_data(0x13)

        self.write_cmd(0xC9)
        self.write_data(0x22)

        self.write_cmd(0xBE)
        self.write_data(0x11)

        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)

        self.write_cmd(0xDF)
        self.write_data(0x21)
        self.write_data(0x0c)
        self.write_data(0x02)

        self.write_cmd(0xF0)
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF1)
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37)
        self.write_data(0x6F)

        self.write_cmd(0xF2)
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF3)
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37)
        self.write_data(0x6F)

        self.write_cmd(0xED)
        self.write_data(0x1B)
        self.write_data(0x0B)

        self.write_cmd(0xAE)
        self.write_data(0x77)

        self.write_cmd(0xCD)
        self.write_data(0x63)

        self.write_cmd(0x70)
        self.write_data(0x07)
        self.write_data(0x07)
        self.write_data(0x04)
        self.write_data(0x0E)
        self.write_data(0x0F)
        self.write_data(0x09)
        self.write_data(0x07)
        self.write_data(0x08)
        self.write_data(0x03)

        self.write_cmd(0xE8)
        self.write_data(0x34)

        self.write_cmd(0x62)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x71)
        self.write_data(0xED)
        self.write_data(0x70)
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x0F)
        self.write_data(0x71)
        self.write_data(0xEF)
        self.write_data(0x70)
        self.write_data(0x70)

        self.write_cmd(0x63)
        self.write_data(0x18)
        self.write_data(0x11)
        self.write_data(0x71)
        self.write_data(0xF1)
        self.write_data(0x70)
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x13)
        self.write_data(0x71)
        self.write_data(0xF3)
        self.write_data(0x70)
        self.write_data(0x70)

        self.write_cmd(0x64)
        self.write_data(0x28)
        self.write_data(0x29)
        self.write_data(0xF1)
        self.write_data(0x01)
        self.write_data(0xF1)
        self.write_data(0x00)
        self.write_data(0x07)

        self.write_cmd(0x66)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0xCD)
        self.write_data(0x67)
        self.write_data(0x45)
        self.write_data(0x45)
        self.write_data(0x10)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_cmd(0x67)
        self.write_data(0x00)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x54)
        self.write_data(0x10)
        self.write_data(0x32)
        self.write_data(0x98)

        self.write_cmd(0x74)
        self.write_data(0x10)
        self.write_data(0x85)
        self.write_data(0x80)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x4E)
        self.write_data(0x00)

        self.write_cmd(0x98)
        self.write_data(0x3e)
        self.write_data(0x07)

        self.write_cmd(0x35)
        self.write_cmd(0x21)

        self.write_cmd(0x11)
        time.sleep(0.12)
        self.write_cmd(0x29)
        time.sleep(0.02)

        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xef)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)

        self.write_cmd(0x2C)

        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

    def draw_char(self, c, top, left, scale=1, color=0xffff):
        code_width = 16
        if c not in self.font:
            c = 'invalid'
        arr = self.font[c]
        for row in range(26):
            code = arr[row]
            for col in range(code_width, -1, -1):
                if code & (1 << col):
                    x, y = left + scale * (code_width - col), top + scale * row
                    for a in range(scale):
                        for b in range(scale):
                            self.pixel(x + a, y + b, color)

    def text_plus(self, s: str, x: int, y: int, c: int, scale=1):
        letter_width = 14 * scale
        for char in s:
            self.draw_char(char, y, x, scale, c)
            x += letter_width

    @staticmethod
    def colour(r, g, b):  # Convert RGB888 to RGB565
        return (((g & 0b00011100) << 3) + ((b & 0b11111000) >> 3) << 8) + (r & 0b11111000) + ((g & 0b11100000) >> 5)
