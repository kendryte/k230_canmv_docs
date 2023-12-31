# image_drawing_alpha_blending_test

```python
# Image Drawing Alpha Blending Test
#
# This script tests the performance and quality of the draw_image()
# method which can perform nearest neighbor, bilinear, bicubic, and
# area scaling along with color channel extraction, alpha blending,
# color palette application, and alpha palette application.

from media.camera import *
from media.display import *
from media.media import *
import time, os, gc, sys

DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

small_img = image.Image(4,4,image.RGB565)
small_img.set_pixel(0, 0, (0,   0,   127))
small_img.set_pixel(1, 0, (47,  255, 199))
small_img.set_pixel(2, 0, (0,   188, 255))
small_img.set_pixel(3, 0, (0,   0,   127))
small_img.set_pixel(0, 1, (0,   176, 255))
small_img.set_pixel(1, 1, (222, 0,   0  ))
small_img.set_pixel(2, 1, (50,  255, 195))
small_img.set_pixel(3, 1, (86,  255, 160))
small_img.set_pixel(0, 2, (255, 211, 0  ))
small_img.set_pixel(1, 2, (83,  255, 163))
small_img.set_pixel(2, 2, (255, 211, 0))
small_img.set_pixel(3, 2, (0,   80,  255))
small_img.set_pixel(0, 3, (255, 118, 0  ))
small_img.set_pixel(1, 3, (127, 0,   0  ))
small_img.set_pixel(2, 3, (0,   144, 255))
small_img.set_pixel(3, 3, (50,  255, 195))

big_img = image.Image(128,128,image.RGB565)
big_img.draw_image(small_img, 0, 0, x_scale=32, y_scale=32)

alpha_div = 1
alpha_value_init = 0
alpha_step_init = 2

x_bounce_init = DISPLAY_WIDTH//2
x_bounce_toggle_init = 1

y_bounce_init = DISPLAY_HEIGHT//2
y_bounce_toggle_init = 1

def camera_init():
    # use hdmi for display
    display.init(LT9611_1920X1080_30FPS)
    # config vb for osd layer
    config = k_vb_config()
    config.max_pool_cnt = 1
    config.comm_pool[0].blk_size = 4*DISPLAY_WIDTH*DISPLAY_HEIGHT
    config.comm_pool[0].blk_cnt = 1
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE
    # meida buffer config
    media.buffer_config(config)
    # init default sensor
    camera.sensor_init(CAM_DEV_ID_0, CAM_DEFAULT_SENSOR)
    # # set chn0 output size
    # camera.set_outsize(CAM_DEV_ID_0, CAM_CHN_ID_0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    # # set chn0 output format
    # camera.set_outfmt(CAM_DEV_ID_0, CAM_CHN_ID_0, PIXEL_FORMAT_YUV_SEMIPLANAR_420)
    # # create meida source device
    # globals()["meida_source"] = media_device(CAMERA_MOD_ID, CAM_DEV_ID_0, CAM_CHN_ID_0)
    # # create meida sink device
    # globals()["meida_sink"] = media_device(DISPLAY_MOD_ID, DISPLAY_DEV_ID, DISPLAY_CHN_VIDEO1)
    # # create meida link
    # media.create_link(meida_source, meida_sink)
    # # set display plane with video channel
    # display.set_plane(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, PIXEL_FORMAT_YVU_PLANAR_420, DISPLAY_MIRROR_NONE, DISPLAY_CHN_VIDEO1)
    # set chn1 output nv12
    camera.set_outsize(CAM_DEV_ID_0, CAM_CHN_ID_1, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    camera.set_outfmt(CAM_DEV_ID_0, CAM_CHN_ID_1, PIXEL_FORMAT_RGB_888)
    # media buffer init
    media.buffer_init()
    # request media buffer for osd image
    globals()["buffer"] = media.request_buffer(4 * DISPLAY_WIDTH * DISPLAY_HEIGHT)
    # start stream for camera device0
    camera.start_stream(CAM_DEV_ID_0)

def camera_deinit():
    # stop stream for camera device0
    camera.stop_stream(CAM_DEV_ID_0)
    # deinit display
    display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # release media buffer
    media.release_buffer(globals()["buffer"])
    # destroy media link
    # media.destroy_link(globals()["meida_source"], globals()["meida_sink"])
    # deinit media buffer
    media.buffer_deinit()

def draw():
    # create image for osd
    buffer = globals()["buffer"]
    osd_img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.RGB565, alloc=image.ALLOC_VB, phyaddr=buffer.phys_addr, virtaddr=buffer.virt_addr, poolid=buffer.pool_id)
    osd_img.clear()
    display.show_image(osd_img, 0, 0, DISPLAY_CHN_OSD0)
    alpha_value = alpha_value_init
    alpha_step = alpha_step_init
    x_bounce = x_bounce_init
    x_bounce_toggle = x_bounce_toggle_init
    y_bounce = y_bounce_init
    y_bounce_toggle = y_bounce_toggle_init
    fps = time.clock()
    while True:
        fps.tick()
        try:
            os.exitpoint()
            rgb888_img = camera.capture_image(CAM_DEV_ID_0, CAM_CHN_ID_1)
            img = rgb888_img.to_rgb565()
            camera.release_image(CAM_DEV_ID_0, CAM_CHN_ID_1, rgb888_img)
            img.draw_image(big_img, x_bounce, y_bounce, rgb_channel=-1, alpha=alpha_value//alpha_div)

            x_bounce += x_bounce_toggle
            if abs(x_bounce-(img.width()//2)) >= (img.width()//2): x_bounce_toggle = -x_bounce_toggle

            y_bounce += y_bounce_toggle
            if abs(y_bounce-(img.height()//2)) >= (img.height()//2): y_bounce_toggle = -y_bounce_toggle

            alpha_value += alpha_step
            if not alpha_value or alpha_value//alpha_div == 256: alpha_step = -alpha_step

            img.copy_to(osd_img)
            del img
            gc.collect()
            print(fps.fps())
        except KeyboardInterrupt as e:
            print("user stop: ", e)
            break
        except BaseException as e:
            sys.print_exception(e)
            break

def main():
    os.exitpoint(os.EXITPOINT_ENABLE)
    camera_is_init = False
    try:
        print("camera init")
        camera_init()
        camera_is_init = True
        print("draw")
        draw()
    except Exception as e:
        sys.print_exception(e)
    finally:
        if camera_is_init:
            print("camera deinit")
            camera_deinit()

if __name__ == "__main__":
    main()

```

具体接口使用请参考相关文档说明：

- [camere](../../../api/mpp/K230_CanMV_Camera模块API手册.md)
- [display](../../../api/mpp/K230_CanMV_Display模块API手册.md)
- [media](../../../api/mpp/K230_CanMV_Media模块API手册.md)
- [image](../../../api/openmv/image.md)
