from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# 初始化窗口
app = Ursina()

# 设置窗口大小
window.size = (1280, 720)

# 定义方块类，继承自Button
class Voxel(Button):
    def __init__(self, position=(0,0,0), color=color.white):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color,
            collider = 'box'  # 添加碰撞器
        )

    # 当玩家左键点击方块时，挖掘方块
    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)
            if key == 'right mouse down':
                voxel = Voxel(position=self.position + mouse.normal, color=player.player_place_color)

# 自定义FirstPersonController以添加蹲下功能
class CustomFirstPersonController(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_crouching = False
        self.crouch_height = 1.5
        self.stand_height = 2
        self.collider = BoxCollider(self, size=(1, 1.5, 1))  # 初始化碰撞体
        self.player_place_color = color.gray  # 默认放置方块颜色
        self.chat_box = None

    def input(self, key):
        super().input(key)
        if key == 'shift down':
            self.crouch()
        if key == 'shift up':
            self.stand_up()
        if key == 't':
            self.toggle_chat_box()

    def crouch(self):
        if not self.is_crouching:
            self.camera_pivot.y = self.crouch_height
            self.collider.size = (1, 0.5, 1)  # 蹲下时调整碰撞体大小
            self.is_crouching = True

    def stand_up(self):
        if self.is_crouching:
            self.camera_pivot.y = self.stand_height
            self.collider.size = (1, 1.5, 1)  # 站立时调整碰撞体大小
            self.is_crouching = False

    def toggle_chat_box(self):
        if self.chat_box is None:
            self.chat_box = TextField(
                parent=camera.ui,
                position=(0.2, -0.2),
                scale=(0.6, 0.1),
                text='',
                color=color.white,
                background=color.black,
                text_color=color.white,
                text_field_color=color.black,
                selection_color=color.light_gray
            )
            self.chat_box.active = True
        else:
            self.process_chat_command()
            destroy(self.chat_box)
            self.chat_box = None

    def process_chat_command(self):
        command = self.chat_box.text.strip().lower()
        if command == 'green':
            self.player_place_color = color.green

# 设置玩家
player = CustomFirstPersonController()

# 生成一个简单的平面世界，地板为绿色
for x in range(20):
    for z in range(20):
        voxel = Voxel(position=(x, 0, z), color=color.green)

# 运行应用
app.run()