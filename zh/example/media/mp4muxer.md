# venc - venc例程

本示例程序用于在 CanMV 开发板进行mp4 muxer的功能展示。  

```python
from media.mp4format import *

def canmv_mp4_muxer_test():
    width = 1280
    height = 720

    # 实例化mp4 container
    mp4_muxer = Mp4Container()

    mp4_cfg = Mp4CfgStr(mp4_muxer.MP4_CONFIG_TYPE_MUXER)
    if mp4_cfg.type == mp4_muxer.MP4_CONFIG_TYPE_MUXER:
        file_name = "/sdcard/app/tests/test.mp4"
        mp4_cfg.SetMuxerCfg(file_name, mp4_muxer.MP4_CODEC_ID_H265, width, height, mp4_muxer.MP4_CODEC_ID_G711U)

    # 创建mp4 muxer
    ret = mp4_muxer.Create(mp4_cfg)
    if ret:
        print("canmv_mp4_muxer_test, mp4 muxer Create failed.")
        return -1

    # 启动mp4 muxer
    ret = mp4_muxer.Start()
    if ret:
        print("canmv_mp4_muxer_test, mp4 muxer Start failed.")
        return -1

    frame_count = 0

    while True:
        # 处理音视频数据，按MP4格式写入文件
        ret = mp4_muxer.Process()
        if ret:
            print("canmv_mp4_muxer_test, mp4 muxer Process failed.")
            return -1

        frame_count += 1
        print("frame_coutn = ", frame_count)
        if frame_count >= 100:
            break

    # 停止mp4 muxer
    ret = mp4_muxer.Stop()
    if ret:
        print("canmv_mp4_muxer_test, mp4 muxer Stop failed.")
        return -1

    # 销毁mp4 muxer
    ret = mp4_muxer.Destroy()
    if ret:
        print("canmv_mp4_muxer_test, mp4 muxer Destroy failed.")
        return -1

    return 0

canmv_mp4_muxer_test()
```

具体接口定义请参考 [VENC](../../api/mpp/K230_CanMV_MP4模块API手册.md)
