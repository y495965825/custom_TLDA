class data_holder(object):
    def __init__(self, images, labels):
        self._epochs_completed = 0
        self._index_in_epoch = 0
        self._images = images
        self._labels = labels

    def next_batch(self, batch_size=100):
        if self._index_in_epoch + batch_size >= len(self._images):
            self._index_in_epoch = 0
        start = self._index_in_epoch
        end = start + batch_size
        return self._images[start:end], self._labels[start:end]


    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels
