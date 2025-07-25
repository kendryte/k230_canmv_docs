# Lvgl 例程讲解

## 概述

CanMV K230 集成了[lv_binding_micropython](https://github.com/lvgl/lv_binding_micropython)项目，用户可以利用lvgl进行图形用户界面（GUI）开发。本示例展示了在 CanMV 开发板上实现 lvgl 动图显示的功能。

## 示例

下面的示例程序演示了如何在CanMV开发板上使用lvgl库显示动态图像。该示例依赖于一些资源文件，建议使用固件内自带的lvgl例程。

```python
from media.display import *
from media.media import *
import time, os, sys, gc
import lvgl as lv

DISPLAY_WIDTH = ALIGN_UP(1920, 16)
DISPLAY_HEIGHT = 1080

def display_init():
    # 使用hdmi作为显示输出，如果您选择的屏幕无法点亮，请参考API文档中的K230_CanMV_Display模块API手册自行配置
    Display.init(Display.LT9611, to_ide = True)
    # 初始化media管理器
    MediaManager.init()

def display_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(50)
    # 销毁 display
    Display.deinit()
    # 释放media缓冲区
    MediaManager.deinit()

def disp_drv_flush_cb(disp_drv, area, color):
    global disp_img1, disp_img2

    if disp_drv.flush_is_last() == True:
        if disp_img1.virtaddr() == uctypes.addressof(color.__dereference__()):
            Display.show_image(disp_img1)
        else:
            Display.show_image(disp_img2)
    disp_drv.flush_ready()

def lvgl_init():
    global disp_img1, disp_img2

    lv.init()
    disp_drv = lv.disp_create(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    disp_drv.set_flush_cb(disp_drv_flush_cb)
    disp_img1 = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    disp_img2 = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    disp_drv.set_draw_buffers(disp_img1.bytearray(), disp_img2.bytearray(), disp_img1.size(), lv.DISP_RENDER_MODE.DIRECT)

def lvgl_deinit():
    global disp_img1, disp_img2

    lv.deinit()
    del disp_img1
    del disp_img2

def user_gui_init():
    res_path = "/sdcard/examples/15-LVGL/data/"

    font_montserrat_16 = lv.font_load("A:" + res_path + "font/montserrat-16.fnt")
    ltr_label = lv.label(lv.scr_act())
    ltr_label.set_text("In modern terminology, a microcontroller is similar to a system on a chip (SoC).")
    ltr_label.set_style_text_font(font_montserrat_16,0)
    ltr_label.set_width(310)
    ltr_label.align(lv.ALIGN.TOP_MID, 0, 0)

    font_simsun_16_cjk = lv.font_load("A:" + res_path + "font/lv_font_simsun_16_cjk.fnt")
    cz_label = lv.label(lv.scr_act())
    cz_label.set_style_text_font(font_simsun_16_cjk, 0)
    cz_label.set_text("嵌入式系统（Embedded System），\n是一种嵌入机械或电气系统内部、具有专一功能和实时计算性能的计算机系统。")
    cz_label.set_width(310)
    cz_label.align(lv.ALIGN.BOTTOM_MID, 0, 0)

    anim_imgs = [None]*4
    with open(res_path + 'img/animimg001.png','rb') as f:
        anim001_data = f.read()

    anim_imgs[0] = lv.img_dsc_t({
    'data_size': len(anim001_data),
    'data': anim001_data
    })
    anim_imgs[-1] = anim_imgs[0]

    with open(res_path + 'img/animimg002.png','rb') as f:
        anim002_data = f.read()

    anim_imgs[1] = lv.img_dsc_t({
    'data_size': len(anim002_data),
    'data': anim002_data
    })

    with open(res_path + 'img/animimg003.png','rb') as f:
        anim003_data = f.read()

    anim_imgs[2] = lv.img_dsc_t({
    'data_size': len(anim003_data),
    'data': anim003_data
    })

    animimg0 = lv.animimg(lv.scr_act())
    animimg0.center()
    animimg0.set_src(anim_imgs, 4)
    animimg0.set_duration(2000)
    animimg0.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    animimg0.start()

def main():
    os.exitpoint(os.EXITPOINT_ENABLE)
    try:
        display_init()
        lvgl_init()
        user_gui_init()
        while True:
            time.sleep_ms(lv.task_handler())
    except BaseException as e:
        print(f"Exception {e}")
    lvgl_deinit()
    display_deinit()
    gc.collect()

if __name__ == "__main__":
    main()
```

```{admonition} 提示
具体接口定义请参考 [lvgl](../../api/lvgl/lvgl.md)
```
