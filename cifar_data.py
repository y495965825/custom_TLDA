import numpy as np
import os
import cPickle


def get_XY(pos, neg):
    X = np.concatenate((pos, neg), axis=0)
    y = np.zeros((pos.shape[0]+neg.shape[0], 2), dtype=np.float32)
    y[:pos.shape[0], 0] = 1
    y[pos.shape[0]:, 1] = 1
    return X, y

def load_CIFAR_batch(filename):
    """ load single batch of cifar """
    with open(filename, 'rb') as f:
        data_dict = cPickle.load(f)
        ims = data_dict['data']
        coarse_labels = np.array(data_dict['coarse_labels'])
        fine_labels = np.array(data_dict['fine_labels'])
        return ims, coarse_labels, fine_labels

def load_CIFAR100(batch_dir):
    """ load all of cifar """
    ims, coarse_labels, fine_labels = load_CIFAR_batch(batch_dir + '/train')
    ims_t, c_labels, f_labels = load_CIFAR_batch(batch_dir + '/test')
    ims = np.concatenate((ims, ims_t))
    coarse_labels = np.concatenate((coarse_labels, c_labels))
    fine_labels = np.concatenate((fine_labels, f_labels))
    return ims, coarse_labels, fine_labels

def load_data(types, cifar_dir = 'datasets'):
    # reorder the cifar-100 dataset by its superclass
    # see https://www.cs.toronto.edu/~kriz/cifar.html for details of classes
    fname = cifar_dir.split('/')[0] + '/cifar100-reordered.npy'
    if os.path.isfile(fname) == False:
        ims, coarse_labels, fine_labels = load_CIFAR100(cifar_dir)
        data = org_by_super_class(ims, coarse_labels, fine_labels, cifar_dir + '/meta')
        with open(fname, 'wb') as fo:
            np.save(fo, data)

    data = {}
    with open(fname, 'rb') as infile:
        d_temp = np.load(infile).item()
    for name in types:
        data[name] = d_temp[name]
    for k in data:
        for kk in data[k]:
            # no reshape
            # data[k][kk] = np.transpose(data[k][kk].reshape((-1, 3, 32, 32)), (0, 2, 3, 1))
            data[k][kk] = data[k][kk].astype(np.float32) / 255.
    return data

def org_by_super_class(ims, coarse_labels, fine_labels, meta_dir):
    print ims.shape, coarse_labels.shape, fine_labels.shape
    with open(meta_dir) as fo:
        name_dict = cPickle.load(fo)
    coarse_names = name_dict['coarse_label_names']
    fine_names = name_dict['fine_label_names']

    data_dict = {}

    for i, name in enumerate(coarse_names):
        data_dict[name] = {}
        temp_labels = fine_labels[coarse_labels == i]
        f_lbs = []
        print temp_labels.shape
        for f_lb in temp_labels:
            if f_lb not in f_lbs:
                f_lbs.append(f_lb)
            if len(f_lbs) == 5:
                break

        for f_lb in f_lbs:
            data_dict[name][fine_names[f_lb]] = ims[fine_labels == f_lb]

    return data_dict

class data_holder(object):
    def __init__(self, images, labels):
        self._num_examples = images.shape[0]
        self._epochs_completed = 0
        self._index_in_epoch = 0
        self._images = images
        self._labels = labels

    def next_batch(self, batch_size=100):
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._images.shape[0]:
            self._epochs_completed += 1
            perm = np.random.permutation(self._images.shape[0])
            self._images = self._images[perm]
            self._labels = self._labels[perm]
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._images.shape[0], "Batch size must less equal to number of examples."
        end = self._index_in_epoch
        return self._images[start:end], self._labels[start:end]


    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels

    @property
    def size(self):
        return self._num_examples
