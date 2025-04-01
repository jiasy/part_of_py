from PIL import Image, ImageFilter

def smoothScalePic(imgPath_,targetImgPath_,scale_ = 2):
    #  打开图片
    _img = Image.open(imgPath_)
    _resizedImg = _img.resize((_img.width*scale_, _img.height*scale_), resample=Image.BICUBIC, box=None, reducing_gap=None)
    _resizedImg = _resizedImg.filter(ImageFilter.SMOOTH_MORE) # 平滑放大
    # _resizedImg.save(imgPath_.replace(".png","_1_reszied.png"))

    # 对图片进行处理并保存
    _sharpImg = _resizedImg.filter(ImageFilter.SHARPEN)# 生成锐化滤波器
    # _sharpImg.save(imgPath_.replace(".png","_2_sharp.png"))

    # 对图片进行处理并保存
    _edgeImg = _resizedImg.filter(ImageFilter.FIND_EDGES)# 生成锯齿化滤波器
    # _edgeImg.save(imgPath_.replace(".png","_3_edge.png"))

    # 将锯齿化图片覆盖到锐化图片上，使用正常叠加模式进行混合
    _resultImg = Image.alpha_composite(_sharpImg.convert('RGBA'), _edgeImg.convert('RGBA'))
    _resultImg.save(targetImgPath_)

if __name__ == "__main__":
    _imgPath = ""
    _targetImgPath = ""
    _scale = 4
    smoothScalePic(_imgPath,_targetImgPath,_scale)
