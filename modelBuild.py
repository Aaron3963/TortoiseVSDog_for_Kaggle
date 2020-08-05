# -*- coding: utf-8 -*-
import torch
import torchvision
from torchvision import datasets, transforms
from torch.autograd import Variable
from torchvision import models
import os
import time
import matplotlib.pyplot as plt

print(torch.__version__)
data_dir = "TortoiseVSDog"
batch_n = 32
data_transform = {x : transforms.Compose([transforms.Scale([224,224]),
                                        transforms.ToTensor(),
                                        transforms.Normalize(mean = [0.5,0.5,0.5], std = [0.5,0.5,0.5])]) for x in ["train","valid"]}

image_datasets = {x :datasets.ImageFolder(root = os.path.join(data_dir, x),
                                        transform = data_transform[x]) for x in ["train","valid"]}
dataloader = {x : torch.utils.data.DataLoader(dataset = image_datasets[x],
                                            batch_size = batch_n,
                                            shuffle = True) for x in ["train","valid"]}

example_x,example_y = next(iter(dataloader["train"]))  
print("-"*60)
print('x的个数:{}'.format(len(example_x)))
print('y的个数:{}'.format(len(example_y)))  

index_classes = image_datasets["train"].class_to_idx
print(index_classes)

example_classes = image_datasets["train"].classes
print(example_classes)

img = torchvision.utils.make_grid(example_x)
img = img.numpy().transpose([1,2,0])
print(example_y)
print([example_classes[i] for i in example_y])
plt.imshow(img)
plt.show()

model = models.resnet50(pretrained = True)
for parma in model.parameters():
    parma.requires_grad = False

model.fc = torch.nn.Linear(2048,2)
#print(model)

Use_GPU = torch.cuda.is_available()
if Use_GPU == True:
    model = model.cuda()

loss_f = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.fc.parameters(), lr = 1e-3)

epoch_n = 3
time_start = time.time()

for epoch in range(epoch_n):
    print("Epoch {}/{}".format(epoch,epoch_n))
    print("*"*40)
    localTime = time.asctime(time.localtime(time.time()))
    print("Local Time: ", localTime)

    for phase in ["train","valid"]:
        if phase == "train":
            print("Training......")
            model.train(True)
        else:
            print("Validing......")
            model.train(False)

        running_loss = 0.0
        running_corrects = 0

        for batch,data in enumerate(dataloader[phase],1):
            x,y = data
            if Use_GPU == True:
                x,y = Variable(x.cuda()),Variable(y.cuda())
            else:
                x,y = Variable(x),Variable(y)
            
            y_pred = model(x)
            _,pred = torch.max(y_pred.data,1)

            optimizer.zero_grad()
            loss = loss_f(y_pred,y)

            if phase == "train":
                loss.backward()
                optimizer.step()

            running_loss += loss.item()
            running_corrects += torch.sum(pred == y.data)

            if batch%100 == 0 and phase == "train":
                print("Batch {}, Train Loss:{:.4f}, Train Accuracy:{:.2f}%".format(batch,running_loss/batch,100*running_corrects/(batch_n*batch)))

        epoch_loss = running_loss/(len(image_datasets[phase])/batch_n)
        epoch_acc = 100 * running_corrects/len(image_datasets[phase])
        print("{} Loss:{:.4f}, Accuracy:{:.2f}%".format(phase,epoch_loss,epoch_acc))

    time_spend = time.time() - time_start
    print("Total Time Spend: {:.1f} minutes!".format(time_spend/60))
    print("\n")
torch.save(model,"ResNet50_.pth")

        




