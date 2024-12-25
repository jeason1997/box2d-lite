import build.box2d as box2d  # 确保SWIG绑定生成的Python模块
from build.box2d import Vec2  # 确保Vec2有正确的Python绑定
import pygame, sys

def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Box2D")
    # 颜色定义
    blue = (0, 0, 255)
    white = (255, 255, 255)

    # 创建一个重力向下的世界
    gravity = Vec2(0.0, 1.0)  # Y轴向下的重力
    iterations = 10  # 模拟的迭代次数
    world = box2d.World(gravity, iterations)

    # 创建一个地面 Body
    ground_body = box2d.Body()
    ground_body.Set(Vec2(50.0, 1.0), 999999)  # 设定地面的大小
    ground_body.position.Set(0.0, -0.5)  # 设置地面的位置
    world.Add(ground_body)  # 将地面添加到世界中

    # 创建一个动态的方块
    dynamic_body = box2d.Body()
    dynamic_body.Set(Vec2(1.0, 1.0), 2.0)  # 设定方块的大小和密度
    dynamic_body.position.Set(0.0, 2.0)  # 设置方块的位置
    world.Add(dynamic_body)  # 添加方块到世界

    dynamic_body.AddForce(Vec2(1, 0))
    # 运行模拟
    time_step = 1.0 / 60.0  # 每帧的时间步长
    while True:  # 运行60帧
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 填充背景
        screen.fill(white)
        # 绘制方块
        pygame.draw.circle(screen, blue, (dynamic_body.position.x * 10, dynamic_body.position.y * 10), 10)
        # 更新屏幕
        pygame.display.flip()
        # 限制帧率
        pygame.time.Clock().tick(60)

        world.Step(time_step)  # 运行一步模拟
        print(f"Body Position: {dynamic_body.position.x, dynamic_body.position.y}")  # 打印方块的位置

if __name__ == "__main__":
    main()