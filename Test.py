import torch
import torchvision
from torchvision import datasets,transforms
from torch.autograd import Variable
from torchvision import models
import os
import random
import cv2
from PIL import Image
import numpy as np

Image_dir = "D:/QiuChengTong/Dog&Cat/TortoiseVSDog/test"
for dirpath,dirnames,filenames in os.walk(Image_dir):
    if dirpath == Image_dir:
        image_files_list = filenames
total_images = len(image_files_list)

print('测试文件个数: {}'.format(total_images))

window_name = "Image Classification: Tortoise VS. Dog"
cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
W_bg = 800
H_bg = 600
cv2.resizeWindow(window_name,W_bg,H_bg)

index = 0

while True:
    img_bg = np.zeros((H_bg,W_bg,3), np.uint8)
    num = random.randint(0,total_images-1)
    img_file = image_files_list[num]
    file_path = os.path.join(Image_dir,img_file)
    img = cv2.imread(file_path)
    width = img.shape[1]
    height = img.shape[0]


    data_transform=transforms.Compose([transforms.Resize([224,224]),
                                     transforms.ToTensor(),
                                     transforms.Normalize(mean=[0.5,0.5,0.5],std=[0.5,0.5,0.5])])
    index_classes = {0:'Dog',1:'Tortoise'}

    model = torch.load('D:/QiuChengTong/Dog&Cat/ResNet50_.pth')    
    model.eval()

    Use_GPU=torch.cuda.is_available()
    if Use_GPU==True:
        model=model.cuda()
    

    image_PIL = Image.open(file_path)
    image_tensor = data_transform(image_PIL)
    image_tensor = torch.unsqueeze(image_tensor,0)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    image_tensor = image_tensor.to(device)
    #print(image_tensor.size())

    y_pred = model(image_tensor)
    print('-'*50)
    print(y_pred.data)
    val,pred = torch.max(y_pred.data,1)

    class_name = index_classes[pred.item()]
    print(class_name)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,class_name,(10,30), font, 1,(0, 255, 255), 2,cv2.LINE_AA)

    h_start = int((H_bg-height)/2)
    h_end = h_start+height
    w_start = int((W_bg-width)/2)
    w_end = w_start+width

    output = img_bg
    output[h_start:h_end, w_start:w_end] = img
    result_list = torch.squeeze(y_pred).data.cpu().numpy()

    cv2.putText(output,str(result_list[0]),(20,20), font,0.5,(0,0,255),1,cv2.LINE_AA)
    cv2.putText(output,str(result_list[1]),(20,40), font, 0.5,(0, 0, 255), 1,cv2.LINE_AA)
    
    file_info='{}/{}'.format(index,total_images)
    cv2.putText(output,file_info,(W_bg-100,20), font, 0.5,(0, 0, 255), 1,cv2.LINE_AA)
    cv2.putText(output,img_file,(W_bg-100,40), font, 0.5,(0, 0, 255), 1,cv2.LINE_AA)
    
    cv2.imshow(window_name, output)

    index += 1
    if cv2.waitKey(2000) == 27:
        break
print('已完成{}个图像的推理',format(index))
cv2.destroyAllWindows()

