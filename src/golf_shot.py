from dataclasses import dataclass, field


@dataclass
class BallData:
    ballspeed: float = field(default=None)
    spinaxis: float = field(default=None)
    totalspin: float = field(default=None)
    backspin: float = field(default=None)
    sidespin: float = field(default=None)
    hla: float = field(default=None)
    vla: float = field(default=None)
    carry: float = field(default=None)


@dataclass
class ClubHeadData:
    speed: float = field(default=0.0)
    angleofattack: float = field(default=0.0)
    facetotarget: float = field(default=0.0)
    lie: float = field(default=0.0)
    loft: float = field(default=0.0)
    path: float = field(default=0.0)
    speedatimpact: float = field(default=0.0)
    verticalfaceimpact: float = field(default=0)
    horizontalfaceimpact: float = field(default=0)
    closurerate: float = field(default=0)
