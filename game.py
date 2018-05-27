"""
用 AI 跑 Avalon
"""
from colorama import Fore,Back,Style


class Game(object):
    """
    定义了游戏运行时，及各种运行模式
    train: 可自行训练出一个模型，掌握游戏规则
    cheat: 通过格式化输入，判断当前局势，给出建议
    single: 人机对战
    """
    def __init__(self, mode):
        super(Game, self).__init__()
        self.mode = mode
        self.round = 0

    def start(self):
        print("%s[start] %s mode" % (Fore.GREEN, self.mode))
        if self.mode == 'train':
            self.train_mode()
        elif self.mode == 'cheat':
            self.cheat_mode()
        elif self.mode == 'single':
            self.single_mode()


class AvalonGame(Game):
    """docstring for AvalonGame."""
    def __init__(self, mode):
        super(AvalonGame, self).__init__(mode)

    def train_mode(self):
        pass

    def cheat_mode(self):
        pass

    def single_mode(self):
        pass


if __name__ == '__main__':
    game = AvalonGame(mode='train') # train 训练模式 / cheat 作弊模式 / single 单人对战模式
    game.start()
