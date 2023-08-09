from machine import Pin, I2C

I2C_SDA = 6
I2C_SDL = 7


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
