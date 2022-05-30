import shelve
import os

import setting
import global_var


class SavingController:
    def __init__(self):
        self.data = None
        self.file_name = os.path.join(setting.save_data_path, "save.dat")
        self.save_path = os.path.join(setting.save_data_path, "save")

    def check_save_exist(self):
        return os.path.exists(self.file_name)

    def create_save(self):
        save_file = shelve.open(self.save_path)
        save_file.close()
        return save_file

    def save(self, data_set):
        save_file = shelve.open(self.save_path, writeback=True)
        for key, data in data_set.items():
            print(f'{key=} {data=}')
            save_file[key] = data
        save_file.close()
        return save_file

    def load_save(self):
        save_file = shelve.open(self.save_path)
        x = save_file['x']
        y = save_file['y']
        stage_no = save_file['stage_no']
        parabola = save_file['parabola']
        exponential = save_file['exponential']
        in_ground = save_file['in_ground']
        dropping = save_file['dropping']
        direction = save_file['direction']
        save_file.close()
        return x, y, stage_no, parabola, exponential, in_ground, dropping, direction

    def save_current_data(self, king_player):
        data = {
            'x': king_player.rect.centerx,
            'y': king_player.rect.centery,
            'stage_no': global_var.stage_no,
            'parabola': king_player.parabola,
            'exponential': king_player.exponential,
            'in_ground': king_player.in_ground,
            'dropping': king_player.dropping,
            'direction': king_player.right
        }
        self.save(data)
        return data

    def debug_save(self):
        save_file = shelve.open(self.save_path)
        for key, data in save_file.items():
            print(f'{key=} {data=}')
        save_file.close()