# player - mp4文件播放器例程

本示例程序用于对 CanMV 开发板进行一个mp4文件播放器的功能展示。

```python
from media.player import * #导入播放器模块，用于播放mp4文件

start_play = False #播放结束flag
def player_event(event,data):
    global start_play
    if(event == K_PLAYER_EVENT_EOF): #播放结束标识
        start_play = False #设置播放结束标识

def play_mp4_test(filename):
    global start_play
    player=Player() #创建播放器对象
    player.load(filename) #加载mp4文件
    player.set_event_callback(player_event) #设置播放器事件回调
    player.start() #开始播放
    start_play = True

    #等待播放结束
    while(start_play):
        time.sleep(0.1)

    player.stop() #停止播放
    print("play over")

play_mp4_test("/sdcard/app/tests/test.mp4")#播放mp4文件
```

具体接口定义请参考 [player](../../api/mpp/K230_CanMV_播放器模块API手册.md)
