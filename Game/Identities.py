from .GameVars import GameTime, WitchPotion, OriginWolfInfectResult, PlayerIdentity
from .Players import Player, only_when_period_is, NightProperty, UserMethod, GroupUserMethod
from .GameError import GameGuardSamePlayerError


class HiddenWolf(Player):
    def __init__(self, game, sid):
        super().__init__(game, sid)
        self.kill_target = NightProperty(game)
        self.changed = False
        self.evil = False  # 隐狼一开始不是狼

    @only_when_period_is(GameTime.night)
    @UserMethod.command("杀")
    def plan_kill(self, target_sid):
        self.kill_target = target_sid

    def change_to_wolf(self):
        self.changed = True
        self.evil = True

    # change to wolf不能立即检查执行，因为需要考虑同步问题。该检查必须在游戏的夜晚判定之后进行。


class WhiteWolf(Player):
    def __init__(self, game, sid):
        super().__init__(game, sid)
        self.kill_target = self._night_property()

    @only_when_period_is(GameTime.night)
    @UserMethod.command("杀")
    def plan_kill(self, target_sid):
        self.kill_target = target_sid

    @only_when_period_is(GameTime.day)
    @GroupUserMethod.command("自爆")
    def kill(self, target_sid):
        self.game.instant_kill(target_sid)
        self.game.next_period()


class OriginWolf(Player):
    def __init__(self, game, sid):
        super().__init__(game, sid)
        self.kill_target = self._night_property()
        self.infect_target = self._night_property()

    @only_when_period_is(GameTime.night)
    @UserMethod.command("杀")
    def plan_kill(self, target_sid):
        self.kill_target = target_sid

    @only_when_period_is(GameTime.night)
    @UserMethod.command("感染")
    def plan_infect(self, target_sid):
        self.infect_target = target_sid

    # 一觉醒来，如果他感染的是民，则感染成功，否则感染失败。
    # 如果民被感染，则自动变狼，这个逻辑处理写在民的代码中。
    def after_night(self):
        if self.game.get_identity_by_sid(self.infect_target) == PlayerIdentity.Survivor:
            self.game.player_dm(self.sid, "感染成功")
        else:
            self.game.player_dm(self.sid, "感染失败")


class Guardian(Player):
    def __init__(self, game, sid):
        super().__init__(game, sid)
        self.last_guard = None
        self.guard_target = self._night_property()

    @only_when_period_is(GameTime.night)
    @UserMethod.command("守")
    def guard(self, target_sid):
        if self.last_guard == target_sid:
            raise GameGuardSamePlayerError()
        else:
            self.guard_target = target_sid

    def after_night(self):
        self.last_guard = self.guard_target


class Witch(Player):
    def __init__(self, game, sid):
        super().__init__(game, sid)
        self.cure_used = False
        self.poison_used = False
        self.use_target = self._night_property()
        self.use_type = self._night_property()

    @only_when_period_is(GameTime.night)
    @UserMethod.command("救")
    def use_cure(self, sid):
        self.use_target = sid
        self.use_type = WitchPotion.cure

    @only_when_period_is(GameTime.night)
    @UserMethod.command("毒")
    def use_cure(self, sid):
        self.use_target = sid
        self.use_type = WitchPotion.poison

    def after_night(self):
        # 夜晚过后，将女巫所用的药水减去。
        self.cure_used = self.cure_used or self.use_type == WitchPotion.cure
        self.poison_used = self.poison_used or self.use_type == WitchPotion.poison


class Seer(Player):
    def __init__(self, game, sid):
        super().__init__(game, sid)
        self.check_target = self._night_property()

    @only_when_period_is(GameTime.night)
    @UserMethod.command("查")
    def check(self, sid):
        self.check_target = sid

    # 夜晚过后，返回所查玩家是好人还是坏人。
    def after_night(self):
        target_player = self.game.get_player_by_sid(self.check_target)
        if target_player:
            if target_player.evil:
                self.game.player_dm(self.sid, f"{target_player.sid}号玩家是好人")
            else:
                self.game.player_dm(self.sid, f"{target_player.sid}号玩家是坏人")
        else:
            self.game.player_dm(self.sid, f"{target_player.sid}号玩家不存在")


class Knight(Player):
    def __init__(self, game, sid):
        super().__init__(game, sid)

    @only_when_period_is(GameTime.day)
    @GroupUserMethod.command("决斗")
    def duel(self, target_sid):
        target_player = self.game.get_player_by_sid(target_sid)
        if target_player:
            if target_player.evil:
                self.game.instant_kill(target_sid)
                self.game.group_broadcast(f"决斗成功，{target_player.sid}号玩家死亡。")
            else:
                self.game.instant_kill(self.sid)
                self.game.group_broadcast(f"决斗失败，{self.sid}号玩家死亡。")
        else:
            self.game.player_dm(self.sid, f"{target_player.sid}号玩家不存在")


class Hunter(Player):
    def __init__(self, game, sid):
        super().__init__(game, sid)
        self.deathrattle_active = False

    @GroupUserMethod.command("杀")
    def kill(self, target_sid):
        if not self.survive:
            if not self.deathrattle_active:
                self.game.instant_kill(target_sid)
                self.game.group_broadcast(f"发动亡语，{target_sid}号玩家被杀。")
                self.deathrattle_active = True
            else:
                self.game.group_broadcast("您已经发动过亡语。")
        else:
            self.game.group_broadcast("您目前不能发动亡语。")