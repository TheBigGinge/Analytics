import numpy
import scipy

class Thompson:

    def __init__(self, data_list, value_to_check):
        self.data_list = data_list
        self.value_to_check = value_to_check

    def run(self):
        mean = numpy.mean(self.data_list)
        sample_dev = numpy.var(self.data_list)
        abs_mean_dev = numpy.abs(self.value_to_check - mean)

        print mean
        print sample_dev
        print abs_mean_dev

sample = [1, 2, 3, 4, 5, 6, 7]
Thompson(sample, 7).run()

