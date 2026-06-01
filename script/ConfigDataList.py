



class ConfigDataList:
    def __init__(self):
        self.mod_names = set() #依赖mod列表
        self.missing_mods =set() #缺失mod列表
        self.missing_abdata =set() #缺失abdata列表
        self.card_path = set()
        self.game_dir = "" #游戏目录
        self.input_dir = "" #png文件夹
        self.output_dir = "" #mods输出文件夹
    def set_game_dir(self,game_dir):
        self.game_dir = game_dir
    def set_input_dir(self,input_dir):
        self.input_dir = input_dir
    def set_output_dir(self,output_dir):
        self.output_dir = output_dir
    def set_dir(self,game_dir,input_dir,output_dir):
        self.set_game_dir(game_dir)
        self.set_input_dir(input_dir)
        self.set_output_dir(output_dir)
    










