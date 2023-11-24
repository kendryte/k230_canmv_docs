# Camera - 摄像头预览及图像采集示例

```python
from media.camera import * #导入camera模块，使用camera相关接口
from media.display import * #导入display模块，使用display相关接口
from media.media import * #导入media模块，使用meida相关接口
from time import * #导入time模块，使用time相关接口
import time
import image #导入image模块，使用image相关接口


def canmv_camera_test():
    print("canmv_camera_test")

    #初始化HDMI显示
    display.init(LT9611_1920X1080_30FPS)

    #初始化默认sensor配置（OV5647）
    camera.sensor_init(CAM_DEV_ID_0, CAM_DEFAULT_SENSOR)
    #camera.sensor_init(CAM_DEV_ID_0, CAM_IMX335_2LANE_1920X1080_30FPS_12BIT_LINEAR)

    out_width = 1920
    out_height = 1080
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

    out_width = 640
    out_height = 480
    out_width = ALIGN_UP(out_width, 16)

    #设置通道1输出尺寸
    camera.set_outsize(CAM_DEV_ID_0, CAM_CHN_ID_1, out_width, out_height)
    #设置通道1输出格式
    camera.set_outfmt(CAM_DEV_ID_0, CAM_CHN_ID_1, PIXEL_FORMAT_RGB_888)

    #设置通道2输出尺寸
    camera.set_outsize(CAM_DEV_ID_0, CAM_CHN_ID_2, out_width, out_height)
    #设置通道2输出格式
    camera.set_outfmt(CAM_DEV_ID_0, CAM_CHN_ID_2, PIXEL_FORMAT_RGB_888_PLANAR)

    #初始化媒体缓冲区
    ret = media.buffer_init()
    if ret:
        print("canmv_camera_test, buffer init failed")
        return ret

    #启动摄像头数据流
    camera.start_stream(CAM_DEV_ID_0)
    time.sleep(15)

    capture_count = 0
    while capture_count < 100:
        time.sleep(1)
        for dev_num in range(CAM_DEV_ID_MAX):
            if not camera.cam_dev[dev_num].dev_attr.dev_enable:
                continue

            for chn_num in range(CAM_CHN_ID_MAX):
                if not camera.cam_dev[dev_num].chn_attr[chn_num].chn_enable:
                    continue

                print(f"canmv_camera_test, dev({dev_num}) chn({chn_num}) capture frame.")
                #从指定设备和通道捕获图像
                img = camera.capture_image(dev_num, chn_num)
                if img == -1:
                    print("camera.capture_image failed")
                    continue

                if img.format() == image.YUV420:
                    suffix = "yuv420sp"
                elif img.format() == image.RGB888:
                    suffix = "rgb888"
                elif img.format() == image.RGBP888:
                    suffix = "rgb888p"
                else:
                    suffix = "unkown"

                filename = f"/sdcard/dev_{dev_num:02d}_chn_{chn_num:02d}_{img.width()}x{img.height()}_{capture_count:04d}.{suffix}"
                print("save capture image to file:", filename)

                with open(filename, "wb") as f:
                    if f:
                        img_data = uctypes.bytearray_at(img.virtaddr(), img.size())
                        # save yuv data to sdcard.
                        #f.write(img_data)
                    else:
                        print(f"capture_image, open dump file failed({filename})")

                time.sleep(1)
                #释放捕获的图像数据
                camera.release_image(dev_num, chn_num, img)

                capture_count += 1

    #停止摄像头输出
    camera.stop_stream(CAM_DEV_ID_0)

    #去初始化显示设备
    display.deinit()

    #销毁媒体链路
    media.destroy_link(meida_source, meida_sink)

    time.sleep(1)
    #去初始化媒体缓冲区资源
    ret = media.buffer_deinit()
    if ret:
        print("camera test, media_buffer_deinit failed")
        return ret

    print("camera test exit")
    return 0


canmv_camera_test()
```

具体接口定义请参考 [camera](../../api/mpp/K230_CanMV_Camera模块API手册.md)
