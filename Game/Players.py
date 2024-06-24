from GameVars import GameTime
from logging import Logger


class Player:
    def __init__(self, game, sid):
        self.survive = True
        # 控制被预言家查出来的结果。
        self.evil = False
        self.sid = sid
        self.game = game
        pass

    def _night_property(self, value=None):
        return NightProperty(self.game, value)

    # 在晚上结束之后，结算之后完成的操作。注意这个时候回合数还没有+1，所以NightProperty还有效。
    # 注意after_night不应该处理游戏逻辑，只应该处理一些报告事件。真正的游戏逻辑必须在Game中完成。
    # 在每晚结束之后，将这一晚所有的玩家的动作整合起来，并统一修改游戏和玩家的状态。
    # 这是为了避免出现同步问题。比如，如果女巫药了
    def after_night(self):
        pass


def only_when_period_is(value):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            if self.game.period == value:
                return method(self, *args, **kwargs)
            else:
                print(f"Action cannot be performed. The period is not {value}.")

        return wrapper

    return decorator


# 这个属性只在当晚生效，白天自动恢复默认值。
# 直接通过value访问就可以。
class NightProperty:
    def __init__(self, game, default_value=None):
        self.game = game
        self.default_value = default_value
        self.record_value = default_value
        self.record_turn = game.record_turn

    @property
    def value(self):
        if self.game.record_turn == self.record_turn:
            return self.record_value
        else:
            return self.default_value

    @value.setter
    def value(self, value):
        self.record_value = value
        self.record_turn = self.game.record_turn

    # value可以直接被用来比较。
    def __eq__(self, other):
        return self.value == other


# 用户调用方法时，检查方法是否为用户可以执行的方法。如果是，则执行。
class UserMethod:
    def __init__(self, func, command_str):
        self.func = func
        self.command_str = command_str

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @staticmethod
    def command(command_str):
        def make(func):
            return UserMethod(func, command_str)

        return make


# 用户在私聊中调用方法时，检查方法是否为群组方法，如果是，则不执行。
class GroupUserMethod(UserMethod):
    def __init__(self, func, command_str):
        super().__init__(func, command_str)

    @staticmethod
    def command(command_str):
        def make(func):
            return GroupUserMethod(func, command_str)

        return make
