class GameError(Exception):
    pass


# 两次不能守同一个人
class GameGuardSamePlayerError(GameError):
    pass
