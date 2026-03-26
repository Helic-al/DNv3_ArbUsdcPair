from enum import IntEnum


class Cross(IntEnum):
    goldenCross = 1
    deadCross = 2
    noCross = 3


class DynamicMACD:
    def __init__(self, shortSpan=12, longSpan=26, signalSpan=9):
        self._shortAlpha = 2 / (shortSpan + 1)
        self._longAlpha = 2 / (longSpan + 1)
        self._signalAlpha = 2 / (signalSpan + 1)

        self._emaShort = None
        self._emaLong = None
        self._macd = None
        self._signal = None
        self._hist = 0.0
        self._prevHist = 0.0

        self._count = 50

    def update(self, price):
        if self._emaShort is None:
            self._emaShort = price
            self._emaLong = price
            self._macd = 0.0
            self._signal = 0.0

            return

        self._prevHist = self._hist

        # EMAの更新
        self._emaShort = (
            self._shortAlpha * price + (1 - self._shortAlpha) * self._emaShort
        )
        self._emaLong = self._longAlpha * price + (1 - self._longAlpha) * self._emaLong

        # MACD, signal
        self._macd = self._emaShort - self._emaLong
        self._signal = (
            self._signalAlpha * self.macd + (1 - self._signalAlpha) * self.signal
        )
        self._hist = self.macd - self.signal

        # カウントの更新、最初の50レコードはクロス判定しない
        self._count = self._count - 1 if self._count > 0 else 0

    def crossDetection(self):
        if self._prevHist <= 0 and self.hist > 0 and self._count <= 0:
            # ゴールデンクロス
            return int(Cross.goldenCross)

        elif self._prevHist >= 0 and self.hist < 0 and self._count <= 0:
            # デッドクロス
            return int(Cross.deadCross)

        else:
            return int(Cross.noCross)

    @property
    def emaShort(self):
        """The  property."""
        if self._emaShort:
            return self._emaShort
        else:
            return 0.0

    @property
    def emaLong(self):
        if self._emaLong:
            return self._emaLong
        else:
            return 0.0

    @property
    def macd(self):
        if self._macd:
            return self._macd
        else:
            return 0.0

    @property
    def signal(self):
        if self._signal:
            return self._signal
        else:
            return 0.0

    @property
    def hist(self):
        if self._hist:
            return self._hist
        else:
            return 0.0
