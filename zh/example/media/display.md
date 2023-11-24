# Display - 图像采集显示实例

```python
from media.camera import * #导入camera模块，使用camera相关接口
from media.display import * #导入display模块，使用display相关接口
from media.media import * #导入media模块，使用meida相关接口
from time import * #导入time模块，使用time相关接口
import time #导入time模块，使用time相关接口


def camera_display_test():
    CAM_OUTPUT_BUF_NUM = 6
    CAM_INPUT_BUF_NUM = 4

    #定义输出窗口的宽度和高度，并进行对齐
    out_width = 1080
    out_height = 720
    out_width = ALIGN_UP(out_width, 16)

    #初始化HDMI显示
    display.init(LT9611_1920X1080_30FPS)
    #初始化默认sensor配置（OV5647）
    camera.sensor_init(CAM_DEV_ID_0, CAM_DEFAULT_SENSOR)

    #设置通道buffer数量
    camera.set_outbufs(CAM_DEV_ID_0, CAM_CHN_ID_0, CAM_OUTPUT_BUF_NUM)
    #设置通道0输出尺寸
    camera.set_outsize(CAM_DEV_ID_0, CAM_CHN_ID_0, out_width, out_height)
    #设置通道0输出格式
    camera.set_outfmt(CAM_DEV_ID_0, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)

     #创建媒体数据源设备
    meida_source = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    #创建媒体数据接收设备
    meida_sink = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    #创建媒体链路，数据从源设备流到接收设备
    media.create_link(meida_source, meida_sink)
    #设置显示输出平面的属性
    display.set_plane(400, 200, out_width, out_height, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

    #初始化媒体缓冲区
    ret = media.buffer_init()
    if ret:
        print("camera_display_test, buffer init failed")
        return ret

    #启动摄像头数据流
    camera.start_stream(CAM_DEV_ID_0)

    #采集显示600s后，停止采集输出
    count = 0
    while count < 600:
        time.sleep(1)
        count += 1

    #停止摄像头输出
    camera.stop_stream(CAM_DEV_ID_0)
    #销毁媒体链路
    media.destroy_link(meida_source, meida_sink)
    time.sleep(1)
    #去初始化显示设备
    display.deinit()
    #去初始化媒体缓冲区资源
    ret = media.buffer_deinit()
    if ret:
        print("camera_display_test, media_buffer_deinit failed")
    return ret

    print("camera_display_test exit")
    return 0

camera_display_test()

```

具体接口定义请参考 [display](../../api/mpp/K230_CanMV_Display模块API手册.md)
