from math import cos, pi, pow, sin


def xyz2rgb(x, y, z, gamma):
    rgbHash = (
        '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0A', '0B', '0C', '0D', '0E', '0F',
        '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D', '1E', '1F',
        '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2A', '2B', '2C', '2D', '2E', '2F',
        '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B', '3C', '3D', '3E', '3F',
        '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
        '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5A', '5B', '5C', '5D', '5E', '5F',
        '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D', '6E', '6F',
        '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7A', '7B', '7C', '7D', '7E', '7F',
        '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B', '8C', '8D', '8E', '8F',
        '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
        'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF',
        'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF',
        'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF',
        'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF',
        'E0', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
        'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
    )
    rgb = ''
    for xW, yW, zW in ((3.2404542, -1.5371385, -0.4985314), (-0.9692660, 1.8760108, 0.0415560), (0.0556434, -0.2040259, 1.0572252)):
        i = x * xW + y * yW + z * zW
        i = 255.0 * (1.055 * pow(i, (1.0 / gamma)) - 0.055 if i > 0.0031308 else 12.92 * i)
        rgb += rgbHash[min(max(round(i), 0), 255)]
    return rgb


def hcl(n, minHue = 15.0, maxHue = 375.0, chroma = 100.0, luminance = 65.0):
    whiteX = 95.047
    whiteY = 100.0
    whiteZ = 108.883
    gamma = 2.4
    eps = 216.0 / 24389.0
    kappa = 24389.0 / 27.0

    white1x15y3z = whiteX + 15 * whiteY + 3 * whiteZ
    u = 4.0 * whiteX / white1x15y3z
    v = 9.0 * whiteY / white1x15y3z
    Y = pow((luminance + 16.0) / 116.0, 3) if (luminance > eps * kappa) else luminance / kappa
    B = - 5.0 * Y
    if not (maxHue - minHue) % 360:
        maxHue -= 360.0 / n
    hueStep = (maxHue - minHue) / (n - 1.0) if n > 1 else 0
    for i in range(n):
        hue = min(max(minHue + i * hueStep, 0), 360) * pi / 180.0
        A = 1.0 / 3.0 * (52.0 * luminance / (chroma * cos(hue) + 13.0 * luminance * u) - 1.0)
        X = (Y * (39.0 * luminance / (chroma * sin(hue) + 13.0 * luminance * v) - 5.0) - B) / (A + 1.0 / 3.0)
        Z = X * A + B
        yield '#' + xyz2rgb(X, Y, Z, gamma)
    return None


class HCL:

    def __init__(self, minHue = 15.0, maxHue = 375.0, chroma = 100.0, luminance = 65.0):
        assert luminance > 0.0, '"luminance" should be a positive float.'

        self.minHue = minHue
        self.maxHue = maxHue
        self.chroma = chroma
        self.luminance = luminance
        self.whiteX = 95.047
        self.whiteY = 100.0
        self.whiteZ = 108.883
        self.gamma = 2.4
        self.eps = 216.0 / 24389.0 # 0.008856452 #
        self.kappa = 24389.0 / 27.0 # 903.2963 #
        self.dec2hex = '0123456789ABCDEF'
        return None


    def xyz2rgb(self, x, y, z):
        for coef in (
            (3.2404542, -1.5371385, -0.4985314),
            (-0.9692660, 1.8760108, 0.0415560),
            (0.0556434, -0.2040259, 1.0572252)
        ):
            rgb = x * coef[0] + y * coef[1] + z * coef[2]
            rgb = 255.0 * (1.055 * pow(rgb, (1.0 / self.gamma)) - 0.055 if rgb > 0.0031308 else 12.92 * rgb)
            yield min(max(round(rgb), 0), 255)
        return None


    def outputColor(self, r, g, b):
        color = '#' + self.dec2hex[(r >> 4) & 15] + self.dec2hex[r & 15] + self.dec2hex[(g >> 4) & 15] + self.dec2hex[g & 15] + self.dec2hex[(b >> 4) & 15] + self.dec2hex[b & 15]
        return color


    def main(self, colors):
        assert colors > 0, '"colors" should be a positive integer.'

        white1x15y3z = self.whiteX + 15 * self.whiteY + 3 * self.whiteZ
        u = 4.0 * self.whiteX / white1x15y3z
        v = 9.0 * self.whiteY / white1x15y3z
        Y = pow((self.luminance + 16.0) / 116.0, 3) if (self.luminance > self.eps * self.kappa) else self.luminance / self.kappa
        B = - 5.0 * Y
        if not (self.maxHue - self.minHue) % 360:
            self.maxHue -= 360.0 / colors
        hueStep = (self.maxHue - self.minHue) / (colors - 1.0) if colors > 1 else 0
        for i in range(colors):
            hue = min(max(self.minHue + i * hueStep, 0), 360) * pi / 180.0
            A = 1.0 / 3.0 * (52.0 * self.luminance / (self.chroma * cos(hue) + 13.0 * self.luminance * u) - 1.0)
            X = (Y * (39.0 * self.luminance / (self.chroma * sin(hue) + 13.0 * self.luminance * v) - 5.0) - B) / (A + 1.0 / 3.0)
            Z = X * A + B
            yield self.outputColor(*self.xyz2rgb(X, Y, Z))
        return self
