from enum import Enum


class GameTime(Enum):
    day = 1
    night = 2


class GamePeriodStage(Enum):
    night = 1
    discuss = 2
    vote = 3
    extra_vote = 4
    deathrattle = 5


class WitchPotion(Enum):
    cure = 1
    poison = 2


class OriginWolfInfectResult(Enum):
    success = 1
    fail = 2


class PlayerIdentity(Enum):
    HiddenWolf = 1
    WhiteWolf = 2
    OriginWolf = 3
    Guardian = 4
    Witch = 5
    Seer = 6
    Knight = 7
    Hunter = 8
    Survivor = 9
