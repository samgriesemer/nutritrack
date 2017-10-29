import os

os.environ['GLOG_minloglevel'] = '2'

import cv2
import numpy as np
try:
    import caffe
except ImportError:
    caffe = None


class CaffePredict(object):
    def __init__(self, deploy_file='deploy.prototxt', caffe_model='snapshot_iter_35520.caffemodel',
                 mean_file='mean.binaryproto', labels_file='labels.txt'):
        if caffe is None:
            return

        # Read model architecture and trained model's weights
        self.net = caffe.Net(
            deploy_file,
            caffe.TEST,
            weights=caffe_model)

        # Load mean file and resize it
        mean_blob = caffe.proto.caffe_pb2.BlobProto()
        with open(mean_file, 'rb') as f:
            mean_blob.ParseFromString(f.read())
        mean_array = np.array(caffe.io.blobproto_to_array(mean_blob))
        mean_array = np.transpose(mean_array[0], (1, 2, 0))
        mean_array = cv2.resize(mean_array, self.net.blobs['data'].data[0][0].shape)
        self.mean_array = np.transpose(mean_array, (2, 0, 1))

        # Define image transformers
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.transformer.set_mean('data', self.mean_array)
        self.transformer.set_transpose('data', (2, 0, 1))

        self.labels = []
        with open(labels_file, 'r') as f:
            for line in f:
                self.labels.append(line.strip())

    def predict_image(self, image):
        im_shape = self.net.blobs['data'].data[0][0].shape
        image = cv2.resize(image, im_shape, interpolation=cv2.INTER_LINEAR)

        # Perform forward propagation for entire network
        self.net.blobs['data'].data[...] = self.transformer.preprocess('data', image)
        out = self.net.forward()
        pred_probas = out['softmax']
        prediction = int(pred_probas.argmax())

        output = {'prediction': {'label': self.labels[prediction], 'confidence': pred_probas[0][prediction]},
                  'top5': []}
        k = 0
        for i, val in sorted(enumerate(pred_probas[0]), key=lambda x: x[1]):
            # print(f'{val*100:2.2f}%\t\t{labels[i]}\t')
            output['top5'].append({'label': self.labels[i], 'confidence': val})
            k += 1
            if k > 5:
                break
        return output

client = CaffePredict()
