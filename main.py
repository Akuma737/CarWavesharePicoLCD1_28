from machine import Pin, I2C, SPI, PWM, ADC, UART
import framebuf
import time
import json

I2C_SDA = 6
I2C_SDL = 7

DC = 8
CS = 9
SCK = 10
MOSI = 11
RST = 12
BL = 25
V_bat_Pin = 29


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
        #with open('font.json', 'r') as f:
            #self.font = json.load(f)
        self.font = {}

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


class QMI8658(object):
    def __init__(self, address=0X6B):
        self._address = address
        self._bus = I2C(id=1, scl=Pin(I2C_SDL), sda=Pin(I2C_SDA), freq=100_000)
        b_ret = self.who_am_i()
        if b_ret:
            self.read_revision()
        else:
            return NULL
        self.config_apply()

    def _read_byte(self, cmd):
        rec = self._bus.readfrom_mem(int(self._address), int(cmd), 1)
        return rec[0]

    def _read_block(self, reg, length=1):
        rec = self._bus.readfrom_mem(int(self._address), int(reg), length)
        return rec

    def _read_u16(self, cmd):
        lsb = self._bus.readfrom_mem(int(self._address), int(cmd), 1)
        msb = self._bus.readfrom_mem(int(self._address), int(cmd) + 1, 1)
        return (msb[0] << 8) + lsb[0]

    def _write_byte(self, cmd, val):
        self._bus.writeto_mem(int(self._address), int(cmd), bytes([int(val)]))

    def who_am_i(self):
        b_ret = False
        if 0x05 == self._read_byte(0x00):
            b_ret = True
        return b_ret

    def read_revision(self):
        return self._read_byte(0x01)

    def config_apply(self):
        # REG CTRL1
        self._write_byte(0x02, 0x60)
        # REG CTRL2 : QMI8658AccRange_8g  and QMI8658AccOdr_1000Hz
        self._write_byte(0x03, 0x23)
        # REG CTRL3 : QMI8658GyrRange_512dps and QMI8658GyrOdr_1000Hz
        self._write_byte(0x04, 0x53)
        # REG CTRL4 : No
        self._write_byte(0x05, 0x00)
        # REG CTRL5 : Enable Gyroscope And Accelerometer Low-Pass Filter
        self._write_byte(0x06, 0x11)
        # REG CTRL6 : Disables Motion on Demand.
        self._write_byte(0x07, 0x00)
        # REG CTRL7 : Enable Gyroscope And Accelerometer
        self._write_byte(0x08, 0x03)

    def read_raw_xyz(self):
        xyz = [0, 0, 0, 0, 0, 0]
        # raw_timestamp = self._read_block(0x30, 3)
        # raw_acc_xyz = self._read_block(0x35, 6)
        # raw_gyro_xyz = self._read_block(0x3b, 6)
        raw_xyz = self._read_block(0x35, 12)
        # timestamp = (raw_timestamp[2] << 16) | (raw_timestamp[1] << 8) | (raw_timestamp[0])
        for i in range(6):
            # xyz[i]=(raw_acc_xyz[(i*2)+1]<<8)|(raw_acc_xyz[i*2])
            # xyz[i+3]=(raw_gyro_xyz[((i+3)*2)+1]<<8)|(raw_gyro_xyz[(i+3)*2])
            xyz[i] = (raw_xyz[(i * 2) + 1] << 8) | (raw_xyz[i * 2])
            if xyz[i] >= 32767:
                xyz[i] = xyz[i] - 65535
        return xyz

    def read_xyz(self):
        xyz = [0, 0, 0, 0, 0, 0]
        raw_xyz = self.read_raw_xyz()
        # QMI8658AccRange_8g
        acc_lsb_div = (1 << 12)
        # QMI8658GyrRange_512dps
        gyro_lsb_div = 64
        for i in range(3):
            xyz[i] = raw_xyz[i] / acc_lsb_div  # (acc_lsb_div/1000.0)
            xyz[i + 3] = raw_xyz[i + 3] * 1.0 / gyro_lsb_div
        return xyz


if __name__ == '__main__':

    LCD = Lcd1inch28()
    LCD.set_bl_pwm(65535)
    qmi8658 = QMI8658()
    V_bat = ADC(Pin(V_bat_Pin))
    uart1 = UART(1, baudrate=9600, tx=Pin(4))
    x = 0
    #with open('image.json', 'r') as f:
    #    image = json.load(f)["image"]
    #for i in image:
    #    LCD.pixel(x % 240, x // 240, LCD.color(i // 0x10000, i // 0x100 % 0x100, i % 0x100))
    #    x += 1

    while True:
        # read QMI8658
        # xyz = qmi8658.read_xyz()

        LCD.fill(LCD.white)

        LCD.fill_rect(0, 0, 240, 80, LCD.blue)
        #LCD.text_plus("!!RDKS!!", 120 - (4 * 14 * 1), 30, LCD.red, 1)

        LCD.fill_rect(0, 80, 60, 40, LCD.red)
        LCD.fill_rect(60, 80, 60, 40, LCD.green)
        LCD.fill_rect(120, 80, 60, 40, LCD.blue)
        LCD.fill_rect(180, 80, 60, 40, LCD.white)
        for i in range(0, 16):
            LCD.fill_rect(i * 15, 120, 15, 40, 1 << i)

        LCD.fill_rect(0, 160, 120, 40, 0x0007)
        LCD.fill_rect(120, 160, 120, 40, 0xE007)

        LCD.set_bl_pwm(65535)

        # LCD.fill_rect(0, 80, 120, 120, 0x1805)
        # LCD.text("ACC_X={:+.2f}".format(xyz[0]), 20, 100 - 3, LCD.white)
        # LCD.text("ACC_Y={:+.2f}".format(xyz[1]), 20, 140 - 3, LCD.white)
        # LCD.text("ACC_Z={:+.2f}".format(xyz[2]), 20, 180 - 3, LCD.white)
        #
        # LCD.fill_rect(120, 80, 120, 120, 0xF073)
        # LCD.text("GYR_X={:+3.2f}".format(xyz[3]), 125, 100 - 3, LCD.white)
        # LCD.text("GYR_Y={:+3.2f}".format(xyz[4]), 125, 140 - 3, LCD.white)
        # LCD.text("GYR_Z={:+3.2f}".format(xyz[5]), 125, 180 - 3, LCD.white)
        #
        # LCD.fill_rect(0, 200, 240, 40, 0x180f)
        # reading = V_bat.read_u16() * 3.3 / 65535 * 2
        # LCD.text("V-bat={:.2f}".format(reading), 80, 215, LCD.white)

        LCD.show()
        time.sleep(0.1)
        try:
            with open('test.fb', 'wb') as f:
                f.write(LCD.buffer)
        except:
            print("Error! Could not save")
        break
        
