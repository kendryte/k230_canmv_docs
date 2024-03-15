# Camera - 多摄像头预览及图像采集示例

```python
from media.camera import *  #导入camera模块，使用camera相关接口
from media.display import * #导入display模块，使用display相关接口
from media.media import *   #导入media模块，使用meida相关接口
import time, os             #导入time模块，使用time相关接口
import sys

def camera_test():
    print("camera_test")

    #初始化HDMI显示
    display.init(LT9611_1920X1080_30FPS)

    #下面配置3个sensor的属性

    #初始化默认sensor配置（CSI0 OV5647）
    camera.sensor_init(CAM_DEV_ID_0, CAM_DEFAULT_SENSOR)
    out_width = 640
    out_height = 480

    # 设置输出宽度16字节对齐
    out_width = ALIGN_UP(out_width, 16)

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
    display.set_plane(0, 0, out_width, out_height, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)

    #初始化默认sensor配置（CSI1 OV5647）
    camera.sensor_init(CAM_DEV_ID_1, CAM_OV5647_1920X1080_CSI1_30FPS_10BIT_USEMCLK_LINEAR)
    out_width = 640
    out_height = 480
    out_width = ALIGN_UP(out_width, 16)
    camera.set_outsize(CAM_DEV_ID_1, CAM_CHN_ID_0, out_width, out_height)
    camera.set_outfmt(CAM_DEV_ID_1, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)
    meida_source1 = media_device(CAMERA_MOD_ID, CAM_DEV_ID_1, CAM_CHN_ID_0)
    meida_sink1 = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO2)
    media.create_link(meida_source1, meida_sink1)
    display.set_plane(640, 320, out_width, out_height, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO2)

    #初始化默认sensor配置（CSI1 OV5647）
    camera.sensor_init(CAM_DEV_ID_2, CAM_OV5647_1920X1080_CSI2_30FPS_10BIT_USEMCLK_LINEAR)
    out_width = 640
    out_height = 480
    out_width = ALIGN_UP(out_width, 16)
    camera.set_outsize(CAM_DEV_ID_2, CAM_CHN_ID_0, out_width, out_height)
    camera.set_outfmt(CAM_DEV_ID_2, CAM_CHN_ID_0, PIXEL_FORMAT_RGB_888)
    meida_source2 = media_device(CAMERA_MOD_ID, CAM_DEV_ID_2, CAM_CHN_ID_0)
    meida_sink2 = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_OSD0)
    media.create_link(meida_source2, meida_sink2)
    display.set_plane(1280, 600, out_width, out_height, PIXEL_FORMAT_RGB_888, DISPLAY_MIRROR_NONE, DISPLAY_CHN_OSD0)

    #初始化媒体缓冲区
    media.buffer_init()

    #启动摄像头数据流（多sensor）
    camera.start_mcm_stream()

    try:
        while True:
            os.exitpoint()
            time.sleep(5)
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)
    #停止摄像头输出
    camera.stop_mcm_stream()

    #去初始化显示设备
    display.deinit()

    #去初始化媒体缓冲区资源
    media.destroy_link(meida_source, meida_sink)
    media.destroy_link(meida_source1, meida_sink1)
    media.destroy_link(meida_source2, meida_sink2)

    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # deinit media buffer
    media.buffer_deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    camera_test()
```

具体接口定义请参考 [camera](../../api/mpp/K230_CanMV_Camera模块API手册.md)
