# TLDA
TensorFlow implementation of the paper [Supervised Representation Learning: Transfer Learning with Deep Autoencoders][TLDA].

---
## Dependency

* [Numpy][np]
* [Tensorflow][tf] >= 1.0
* [CIFAR-100 Dataset][cifar]

---
## Setup
Run `bash setup.sh` in terminal to automatically download the CIFAR-100 dataset.

---

## Usage
Enter `python TLDA.py` in bash for fast with default setting.

Use `--cifar_path` to specify the path of pretrained VGG Net. By default, the model is located under `datasets/cifar-100-python` directory

Use `--outfile` to specify file to save the result. By default, the file is "result.csv".

Use `--help` to acquire more information.

---

[TLDA]:http://www.intsci.ac.cn/users/zhuangfuzhen/paper/IJCAI15-578.pdf
[np]:https://github.com/numpy/numpy/blob/master/INSTALL.rst.txt
[tf]:http://tensorflow.org
[cifar]:https://www.cs.toronto.edu/~kriz/cifar.html


## custom
1. https://tensorflowkorea.gitbooks.io/tensorflow-kr/content/g3doc/tutorials/mnist/download/
2. 링크를 따라가서 train-images-idx3-ubyte.gz, train-labels-idx1-ubyte.gz 다운 받기
3. root 폴더에 mnist 폴더를 만들고 그 안에 위 압축파일을 푼다.
4. python custom.py
5. (0, 1 구별 VS 2, 3 구별)

