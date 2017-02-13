import sys, math
from PIL import Image

def Distance(p1,p2):
  dx = p2[0] - p1[0]
  dy = p2[1] - p1[1]
  return math.sqrt(dx*dx+dy*dy)

def ScaleRotateTranslate(image, angle, center = None, new_center = None, scale = None, resample=Image.BICUBIC):
  if (scale is None) and (center is None):
    return image.rotate(angle=angle, resample=resample)
  nx,ny = x,y = center
  sx=sy=1.0
  if new_center:
    (nx,ny) = new_center
  if scale:
    (sx,sy) = (scale, scale)
  cosine = math.cos(angle)
  sine = math.sin(angle)
  a = cosine/sx
  b = sine/sx
  c = x-nx*a-ny*b
  d = -sine/sy
  e = cosine/sy
  f = y-nx*d-ny*e
  return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=resample)

def CropFace(image, eye_left=(0,0), eye_right=(0,0), offset_pct=(0.2,0.2), dest_sz = (70,70)):
  # calculate offsets in original image
  offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
  offset_v = math.floor(float(offset_pct[1])*dest_sz[1])
  # get the direction
  eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
  # calc rotation angle in radians
  rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
  # distance between them
  dist = Distance(eye_left, eye_right)
  # calculate the reference eye-width
  reference = dest_sz[0] - 2.0*offset_h
  # scale factor
  scale = float(dist)/float(reference)
  # rotate original around the left eye
  image = ScaleRotateTranslate(image, center=eye_left, angle=rotation)
  # crop the rotated image
  crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
  crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
  image = image.crop((int(crop_xy[0]), int(crop_xy[1]), int(crop_xy[0]+crop_size[0]), int(crop_xy[1]+crop_size[1])))
  # resize it
  image = image.resize(dest_sz, Image.ANTIALIAS)
  return image

if __name__ == "__main__":
    offsetPercentage= (0.3,0.3)
    imgSize = (200,200)

    image1 = Image.open(r"D:\arbetsprov\learn\male\ArnSwa1.jpg")
    image2 = Image.open(r"D:\arbetsprov\learn\male\ArnSwa2.jpg")
    image3 = Image.open(r"D:\arbetsprov\learn\male\ArnSwa3.jpg")
    CropFace(image1, eye_left=(650, 488), eye_right=(936, 474), offset_pct=offsetPercentage, dest_sz=imgSize).save("maleCrop1.jpg")
    CropFace(image2, eye_left=(286, 447), eye_right=(516, 422), offset_pct=offsetPercentage, dest_sz=imgSize).save("maleCrop2.jpg")
    CropFace(image3, eye_left=(1039, 555), eye_right=(1322, 591), offset_pct=offsetPercentage, dest_sz=imgSize).save("maleCrop3.jpg")

    image1 = Image.open(r"D:\arbetsprov\learn\male\BraPit1.jpg")
    image2 = Image.open(r"D:\arbetsprov\learn\male\BraPit2.jpg")
    image3 = Image.open(r"D:\arbetsprov\learn\male\BraPit3.jpg")
    CropFace(image1, eye_left=(129, 167), eye_right=(196, 175), offset_pct=offsetPercentage, dest_sz=imgSize).save("maleCrop4.jpg")
    CropFace(image2, eye_left=(168, 243), eye_right=(272, 243), offset_pct=offsetPercentage, dest_sz=imgSize).save("maleCrop5.jpg")
    CropFace(image3, eye_left=(90, 156), eye_right=(166, 154), offset_pct=offsetPercentage, dest_sz=imgSize).save("maleCrop6.jpg")

    image1 = Image.open(r"D:\arbetsprov\learn\male\GeoClo1.jpg")
    image2 = Image.open(r"D:\arbetsprov\learn\male\GeoClo2.jpg")
    image3 = Image.open(r"D:\arbetsprov\learn\male\GeoClo3.jpg")
    CropFace(image1, eye_left=(123, 144), eye_right=(194, 140), offset_pct=offsetPercentage, dest_sz=imgSize).save("maleCrop7.jpg")
    CropFace(image2, eye_left=(801, 999), eye_right=(1220, 1008), offset_pct=offsetPercentage, dest_sz=imgSize).save("maleCrop8.jpg")
    CropFace(image3, eye_left=(292, 423), eye_right=(482, 401), offset_pct=offsetPercentage, dest_sz=imgSize).save("maleCrop9.jpg")

    image1 = Image.open(r"D:\arbetsprov\learn\male\JohDep1.jpg")
    image2 = Image.open(r"D:\arbetsprov\learn\male\JohDep2.jpg")
    image3 = Image.open(r"D:\arbetsprov\learn\male\JohDep3.jpg")
    CropFace(image1, eye_left=(490, 710), eye_right=(796, 739), offset_pct=offsetPercentage, dest_sz=imgSize).save("maleCrop10.jpg")
    CropFace(image2, eye_left=(335, 183), eye_right=(514, 188), offset_pct=offsetPercentage, dest_sz=imgSize).save("maleCrop11.jpg")
    CropFace(image3, eye_left=(111, 78), eye_right=(159, 81), offset_pct=offsetPercentage, dest_sz=imgSize).save("maleCrop12.jpg")

    image1 = Image.open(r"D:\arbetsprov\learn\female\AngJol1.jpg")
    image2 = Image.open(r"D:\arbetsprov\learn\female\AngJol2.jpg")
    image3 = Image.open(r"D:\arbetsprov\learn\female\AngJol3.jpg")
    CropFace(image1, eye_left=(276, 276), eye_right=(416, 276), offset_pct=offsetPercentage, dest_sz=imgSize).save("femaleCrop1.jpg")
    CropFace(image2, eye_left=(573, 312), eye_right=(1005, 310), offset_pct=offsetPercentage, dest_sz=imgSize).save("femaleCrop2.jpg")
    CropFace(image3, eye_left=(487, 445), eye_right=(784, 452), offset_pct=offsetPercentage, dest_sz=imgSize).save("femaleCrop3.jpg")

    image1 = Image.open(r"D:\arbetsprov\learn\female\EmmWat1.jpg")
    image2 = Image.open(r"D:\arbetsprov\learn\female\EmmWat2.jpg")
    image3 = Image.open(r"D:\arbetsprov\learn\female\EmmWat3.jpg")
    CropFace(image1, eye_left=(1016, 1124), eye_right=(1470, 1081), offset_pct=offsetPercentage, dest_sz=imgSize).save("femaleCrop4.jpg")
    CropFace(image2, eye_left=(689, 663), eye_right=(929, 651), offset_pct=offsetPercentage, dest_sz=imgSize).save("femaleCrop5.jpg")
    CropFace(image3, eye_left=(118, 193), eye_right=(186, 181), offset_pct=offsetPercentage, dest_sz=imgSize).save("femaleCrop6.jpg")

    image1 = Image.open(r"D:\arbetsprov\learn\female\JenLop1.jpg")
    image2 = Image.open(r"D:\arbetsprov\learn\female\JenLop2.jpg")
    image3 = Image.open(r"D:\arbetsprov\learn\female\JenLop3.jpg")
    CropFace(image1, eye_left=(116, 147), eye_right=(182, 145), offset_pct=offsetPercentage, dest_sz=imgSize).save("femaleCrop7.jpg")
    CropFace(image2, eye_left=(321, 431), eye_right=(507, 431), offset_pct=offsetPercentage, dest_sz=imgSize).save("femaleCrop8.jpg")
    CropFace(image3, eye_left=(265, 265), eye_right=(410, 268), offset_pct=offsetPercentage, dest_sz=imgSize).save("femaleCrop9.jpg")

    image1 = Image.open(r"D:\arbetsprov\learn\female\KatPer1.jpg")
    image2 = Image.open(r"D:\arbetsprov\learn\female\KatPer2.jpg")
    image3 = Image.open(r"D:\arbetsprov\learn\female\KatPer3.jpg")
    CropFace(image1, eye_left=(87, 104), eye_right=(136, 103), offset_pct=offsetPercentage, dest_sz=imgSize).save("femaleCrop10.jpg")
    CropFace(image2, eye_left=(327, 310), eye_right=(457, 306), offset_pct=offsetPercentage, dest_sz=imgSize).save("femaleCrop11.jpg")
    CropFace(image3, eye_left=(114, 76), eye_right=(147, 76), offset_pct=offsetPercentage, dest_sz=imgSize).save("femaleCrop12.jpg")