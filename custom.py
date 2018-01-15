import numpy as np
from argparse import ArgumentParser
from data_holder_custom import *
from mnist import MNIST
from model_custom import Model

mndata = MNIST('./mnist')

# label 0~9
# input data size of feature is 784
images, labels = mndata.load_training()
source_x, source_y = [], []
target_x, target_y = [], []
idx = 0
while idx < len(images):
    if labels[idx] == 0:
        source_x.append(images[idx])
        source_y.append([1, 0])
    elif labels[idx] == 1:
        source_x.append(images[idx])
        source_y.append([0, 1])
    elif labels[idx] == 2:
        target_x.append(images[idx])
        target_y.append([1, 0])
    elif labels[idx] == 3:
        target_x.append(images[idx])
        target_y.append([0, 1])
    idx = idx + 1


alpha = 1e-3
beta = 1e1
gamma = 1e-5
verbose = 50


Xs, ys = source_x, source_y
Xt, yt = target_x, target_y

src = data_holder(Xs, ys)
targ = data_holder(Xt, yt)
print 'alpha %.6f, beta %.6f, gamma %.6f'%(alpha, beta, gamma)
with Model() as model:
    model.build()
    model.inference(alpha, beta, gamma)
    model.train(src, targ, verbose=verbose)
    rr[i] = model.test(targ)
# print 'Test Accuracy is ', rr[i]
