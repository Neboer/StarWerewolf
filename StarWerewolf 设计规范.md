# StarWerewolf 设计规范

*星之狼人*

## 中英文对照表

- 狼 Wolf
  - 隐狼 HiddenWolf
  - 白狼 WhiteWolf
  - 种狼 OriginWolf
- 民 Human
  - 守卫 Guardian
  - 女巫 Witch
  - 预言 Seer
  - 骑士 Knight
  - 猎人 Hunter
  - 平民 Survivor

## 基本设计

命令：

所有的命令都是用来触发方法的，方法修改属性。

类：

- Player
  - ...
- Game

属性：

- Game
  - Players
    - HiddenWolf 谁是隐狼，没人就null
    - WhiteWolf
    - ...
    - Survivor Player[] 是个列表，只有村民可以有很多。
  - 命令列表（）
  - 玩家列表
  - 身份广播
  - Period白天黑夜
  - 

- Player

  - evil：当前是否为坏人。

  - survive

  - 长期属性K：女巫的药水。

  - 每晚属性T：狼的杀人目标。每晚属性会在下一晚开始前清空。

    方法的一般限制是白天/晚上使用，次数使用，特殊方法不受限制。

  - 白天方法D：骑士决斗

  - 夜晚方法N：狼选择杀人目标

  - 特殊方法S：有自己特殊的触发时间

所有的方法都只有一个Player做目标。每个夜晚方法都有每晚使用次数限制。可以跳过方法的执行。

- HiddenWolf
  - K changed 是否已转变成狼
  - T kill_target 要杀的人
  - N plan_kill 1 想要杀谁
- WhiteWolf
  - D Kill 自爆（不报身份）带走玩家，直接进入黑夜
  - T kill_target 要杀的人
  - N plan_kill 1 想要杀谁
- OriginWolf
  - T kill_target 要杀的人
  - T infect_target 要感染的人
  - N plan_kill 1 想要杀谁
  - N plan_infect 1 想要感染谁
- Guardian
  - K last_guard 上次守卫了谁
  - T guard 今晚守了谁
  - N guard 1 今晚守谁
- Witch
  - K cure_used 解药用了吗
  - K poison_used 毒药用了吗
  - N use_potion(cure/poison, player) 1 使用药水
- Seer
  - N check 1 查人。
- Knight
  - D fight 1 决斗
- Hunter
  - S kill 亡语：死亡时带走一名玩家。
- Survivor
  - K changed 是否转变为狼

## 游戏流程

昼夜交替。

白天：

1. 报告昨晚情况
2. 发言
3. 投票，最后一票投出后，以所有人投的最后一票为准。
4. 淘汰投票，票数多者淘汰，否则两人决一出局。
5. 淘汰
6. 计算胜利，进入黑夜或游戏结束。

晚上

1. 一旦进入晚上，就开始收集所有狼神的私聊
1. 广播顺序 吹笛者→丘比特→女仆→**守卫**→**狼人**→**女巫**→**预言家**→野孩子→禁言长老
1. 总结大家的行动，做出计算，进入白天或游戏结束。