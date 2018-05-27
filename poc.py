from enum import Enum
import random
from colorama import Fore, Back, Style
from collections import Counter

class BlueSide(Enum):
    Merlin = 1
    Percival = 2
    Servants = 3

class RedSide(Enum):
    Morgana = 1
    Assassin = 2
    Mordred = 3
    Oberon = 4

class Player:
    def __init__(self, number, role=BlueSide.Servants, side='good'):
        self.number = number
        self.role = role
        # self.is_fairy = False  # 湖中仙子扩展
        self.side = side
        self.believe = {}

    def __str__(self):
        s = "P%s:%s:%s" % (self.number, self.role, self.side)
        if self.side == 'good':
            return Fore.GREEN + s + Style.RESET_ALL
        else:
            return Fore.RED + s + Style.RESET_ALL

    def propose_team(self, context, players, member_num):
        team = random.sample(players,  member_num)
        print("\nleader", leader)
        [print("\t>", mem) for mem in team]
        return team

    def vote_team(self, context, team):
        return random.choice([True, False])

    def vote_task(self, context):
        if self.side == 'good':
            return True
        elif self.side == 'evil':
            return random.choice([True, False])


""" 游戏初始设置 """
P1 = Player(1, BlueSide.Merlin, 'good')
P2 = Player(2, BlueSide.Percival, 'good')
P3 = Player(3, BlueSide.Servants, 'good')
P4 = Player(4, BlueSide.Servants, 'good')
P5 = Player(5, BlueSide.Servants, 'good')
P6 = Player(6, BlueSide.Servants, 'good')
P7 = Player(7, RedSide.Morgana, 'evil')
P8 = Player(8, RedSide.Assassin, 'evil')
P9 = Player(9, RedSide.Mordred, 'evil')
P10 = Player(10, RedSide.Oberon, 'evil')

PLAYERS = [P1, P2, P3, P4, P5, P6, P7, P8, P9, P10]  # 设置玩家
ROUND = 5  # 轮次
ROUND_TEAM_MEMBER_NUM = [3, 4, 4, 5, 5]  # 每轮参与人数
FAIL_VOTE = [1, 1, 1, 1, 2]
BLUESIDE_WIN = 0  # 蓝胜
REDSIDE_WIN = 0  # 红胜

""" 天黑阶段 """
# 梅林睁眼，所有坏人举手（除了莫德雷德）
P1.believe[7] = {'side': 'evil', 'confidence': 1}
P1.believe[8] = {'side': 'evil', 'confidence': 1}
P1.believe[9] = {'side': 'evil', 'confidence': 1}
P1.believe[10] = {'side': 'evil', 'confidence': 1}

# 奥伯伦以外的坏人睁眼，互相辨认同伴
P7.believe[8] = {'side': 'evil', 'confidence': 1}
P7.believe[9] = {'side': 'evil', 'confidence': 1}
P8.believe[7] = {'side': 'evil', 'confidence': 1}
P8.believe[9] = {'side': 'evil', 'confidence': 1}
P9.believe[7] = {'side': 'evil', 'confidence': 1}
P9.believe[8] = {'side': 'evil', 'confidence': 1}

# 派西维尔睁眼，梅林和莫甘娜举手
P2.believe[1] = {'role': BlueSide.Merlin, 'confidence': 0.5, 'side': 'good'}
P2.believe[7] = {'role': BlueSide.Merlin, 'confidence': 0.5, 'side': 'good'}

"""天亮阶段"""
# 随机选择一个玩家担任队长
leader_i = random.randint(0, len(PLAYERS) - 1)
leader = PLAYERS[leader_i]

def next_leader(leader_i):
    leader_i += 1
    if leader_i >= len(PLAYERS) - 1:
        leader_i = 0
    leader = PLAYERS[leader_i]
    return leader_i, leader

# 全部上下文的记录
context = []
round_i = 0

while round_i < ROUND:
    # 选定足够人数的队员
    member_num = ROUND_TEAM_MEMBER_NUM[round_i]
    team = leader.propose_team(context, PLAYERS, member_num)

    # 进行发言（暂不支持）、投票
    team_vote_result = []

    for player in PLAYERS:
        if player.number != leader.number: # 除队长外投票
            team_vote = player.vote_team(context, team)
            team_vote_result.append(team_vote)
    team_vote_counter = Counter(team_vote_result)

    # 任务执行 or 延迟
    team_pass = team_vote_counter[True] > team_vote_counter[False]
    if team_pass:
        print(Fore.GREEN + "Team Pass" + Style.RESET_ALL, team_vote_counter)
    else:
        print(Fore.RED + "Team Fail" + Style.RESET_ALL, team_vote_counter)

    # 任务判定
    if team_pass:
        task_vote = [mem.vote_task(context) for mem in team]
        task_vote_result = Counter(task_vote)
        task_pass = task_vote_result[False] >= FAIL_VOTE[round_i]

        if task_pass:
            print(Fore.GREEN + "TASK[%s] PASS" % round_i, task_vote_result, Style.RESET_ALL)
            BLUESIDE_WIN += 1
        else:
            print(Fore.RED + "TASK[%s] FAIL" % round_i, task_vote_result, Style.RESET_ALL)
            REDSIDE_WIN += 1

        round_i += 1

    if BLUESIDE_WIN == 3:
        # 红方要找出梅林才行
        print(Fore.GREEN + "\n\n蓝方胜利了！！！")
        break
    elif REDSIDE_WIN == 3:
        print(Fore.RED + "\n\n红方胜利了！！！")
        break

    # 重选队长
    leader_i, leader = next_leader(leader_i)
