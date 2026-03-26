from enum import IntEnum


class Cross(IntEnum):
    goldenCross = 1
    deadCross = 2
    noCross = 3


class DynamicMACD:
    def __init__(self, shortSpan=12, longSpan=26, signalSpan=9):
        self.shortAlpha = 2 / (shortSpan + 1)
        self.longAlpha = 2 / (longSpan + 1)
        self.signalAlpha = 2 / (signalSpan + 1)

        self.emaShort = None
        self.emaLong = None
        self.macd = None
        self.signal = None
        self.hist = 0.0
        self.prevHist = 0.0

        self.count = 50

    def update(self, price):
        if self.emaShort is None:
            self.emaShort = price
            self.emaLong = price
            self.macd = 0.0
            self.signal = 0.0

            return

        self.prevHist = self.hist

        # EMAの更新
        self.emaShort = self.shortAlpha * price + (1 - self.shortAlpha) * self.emaShort
        self.emaLong = self.longAlpha * price + (1 - self.longAlpha) * self.emaLong

        # MACD, signal
        self.macd = self.emaShort - self.emaLong
        self.signal = (
            self.signalAlpha * self.macd + (1 - self.signalAlpha) * self.signal
        )
        self.hist = self.macd - self.signal

        # カウントの更新、最初の50レコードはクロス判定しない
        self.count = self.count - 1 if self.count > 0 else 0

    def crossDetection(self):
        if self.prevHist <= 0 and self.hist > 0 and self.count <= 0:
            # ゴールデンクロス
            return int(Cross.goldenCross)

        elif self.prevHist >= 0 and self.hist < 0 and self.count <= 0:
            # デッドクロス
            return int(Cross.deadCross)

        else:
            return int(Cross.noCross)

    @property
    def emaShort(self):
        """The  property."""
        if self.emashort:
            return self.emaShort
        else:
            return 0.0

    @property
    def emaLong(self):
        if self.emaLong:
            return self.emaShort
        else:
            return 0.0

    @property
    def macd(self):
        if self.macd:
            return self.macd
        else:
            return 0.0

    @property
    def signal(self):
        if self.signal:
            return self.signal
        else:
            return 0.0

    @property
    def hist(self):
        if self.hist:
            return self.hist
        else:
            return 0.0
