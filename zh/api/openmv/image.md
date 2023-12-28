# image 图像处理 API手册

移植于`openmv`，与`openmv`功能相同，详细请参考[官方文档](https://docs.openmv.io/library/omv.image.html)，以下仅列出与官方API的差异部分及新增API。

## 类 `Image`

图像对象是机器视觉操作的基本对象。
image支持从micropython gc，mmz，heap，vb区域创建，REF为在参考对象内存上直接生成image。
未使用的image对象会在执行gc回收时自动释放，用户也可手动执行释放，此时申请的图像内存会立即归还到系统。

image支持的格式：

- BINARY
- GRAYSCALE
- RGB565
- BAYER
- YUV422
- JPEG
- PNG
- ARGB8888 (新增格式)
- RGB888 (新增格式)
- RGBP888 (新增格式)
- YUV420 (新增格式)

image支持的分配区域：

- ALLOC_MPGC：micropython管理的内存
- ALLOC_HEAP：系统堆内存
- ALLOC_MMZ：多媒体内存
- ALLOC_VB：视频缓冲区
- ALLOC_REF：不分配内存，使用参考对象内存

### 构造函数

```python
class image.Image(path, alloc=ALLOC_MMZ, cache=True, phyaddr=0, virtaddr=0, poolid=0, data=None)
```

从path中的文件创建一个图像对象，支持bmp/pgm/ppm/jpg/jpeg格式的图像文件。

```python
class image.Image(w, h, format, alloc=ALLOC_MMZ, cache=True, phyaddr=0, virtaddr=0, poolid=0, data=None)
```

创建一个指定大小格式的图像对象。

- w: 图像宽度
- h: 图像高度
- format: 图像格式
- alloc: 图像创建内存位置，可选参数，默认ALLOC_MMZ
- cache: 使能内存cache，可选参数，默认True
- phyaddr: 图像数据的物理内存地址，仅在VB区域中创建有效
- virtaddr: 图像数据的虚拟内存地址，仅在VB区域中创建有效
- poolid: VB poolid，仅在VB区域中创建有效，可选参数
- data: 参考对象，可用于初始化image数据，可选参数

示例：

```python
# 在MMZ区域创建一个ARGB8888 640*480的图像：
img = image.Image(640,480,image.ARGB8888)
# 在VB区域创建一个YUV420 640*480的图像：
img = image.Image(640,480,image.YUV420,alloc=image.ALLOC_VB,phyaddr=xxx,virtaddr=xxx,poolid=xxx)
# 使用REF创建一个RGB888 640*480的图像：
img = image.Image(640,480,image.RGB888,alloc=image.ALLOC_REF,data=buffer_obj)
img = image.Image(640,480,image.RGB888,alloc=image.ALLOC_REF,data=ulab_obj)
# 立即释放图像内存
del img
gc.collect()
```

### 函数

#### 新增函数

##### `phyaddr`

```python
image.phyaddr()
```

获取image数据的物理内存地址。

##### `virtaddr`

```python
image.virtaddr()
```

获取image数据的虚拟内存地址。

##### `poolid`

```python
image.poolid()
```

获取image数据的VB poolid。

##### `to_rgb888`

```python
image.to_rgb888(x_scale=1.0[, y_scale=1.0[, roi=None[, rgb_channel=-1[, alpha=256[, color_palette=None[, alpha_palette=None[, hint=0[, alloc=ALLOC_MMZ, cache=True, phyaddr=0, virtaddr=0, poolid=0]]]]]]]])
```

转换图像格式为RGB888，返回一个新图像对象。
除原生支持格式外，额外添加`RGB888`格式支持，其它格式不支持。

##### `copy_to`

```python
image.copy_to(dst_img)
```

拷贝img到dst_img。

##### `to_numpy_ref`

```python
image.to_numpy_ref()
```

将image类转换成numpy类，转换完成后numpy与image指向的是同一块数据，在numpy使用完成之前不能删除image，支持格式`GRAYSCALE`、`RGB565`、`ARGB8888`、`RGB888`、`RGBP888`。

#### 差异函数

##### 图像变换API

- `to_bitmap`
- `to_grayscale`
- `to_rgb565`
- `to_rainbow`
- `to_ironbow`
- `to_jpeg`
- `to_png`
- `copy`
- `crop`
- `scale`

以上API的`crop`参数失效，新增分配方式参数，总是返回一个新图像对象，图像对象的分配参数参考构造函数。

`compress`与`compressed`新增分配方式参数，总是返回一个新图像对象。
`compress_for_ide`与`compressed_for_ide`新增分配方式参数，总是返回一个新图像对象。

除原生支持格式外，额外添加`RGB888`格式支持，其它格式不支持。

##### 画图API

除原生支持格式外，额外添加`ARGB8888`、`RGB888`格式支持，其它格式不支持。

##### BINARY API

`binary`新增分配方式参数，仅在copy=True时有效。

##### POOL API

`mean_pooled`和`midpoint_pooled`新增分配方式参数。

#### 其它图像算法API

只支持原生格式，`RGB888`格式需要经过转换后才能使用。
