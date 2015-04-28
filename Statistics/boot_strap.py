import numpy as np
import random as rando


class BootStrap:

    def __init__(self, values_list, repetitions, target_percentile):
    
        self.values_list = values_list
        self.reps = repetitions
        self.percentile = target_percentile
    
    def run(self):

        n = len(self.values_list)
    
        if "No Data" in self.values_list:
            final = 'No Data', 'No Data', 'No Data', 'No Data', 'No Data'
            return final

        elif n < 5:
            overall_percentile = np.percentile(self.values_list, self.percentile)
            final = int(round(overall_percentile, -2)), 'Low Data', 'Low Data', 'Low Data', 'Low Data'
            return final

        elif n >= 5:

            overall_percentile = np.percentile(self.values_list, self.percentile)
            percent_list = self.boot_strap(n)
            tenth = np.percentile(percent_list, 10)
            ninetieth = np.percentile(percent_list, 90)

            distance_a = abs((overall_percentile-tenth)/tenth)
            distance_b = abs((overall_percentile-ninetieth)/ninetieth)
            possibles = [distance_a, distance_b]
            error = max(possibles)

            final = int(round(overall_percentile, -2)), error, int(round(tenth, -2)), int(round(ninetieth, -2))

            return final

    def boot_strap(self, n):

        percent_list = []

        result = [None] * n
        for x in xrange(self.reps):
            for i in xrange(n):
                j = int(rando.random() * n)
                result[i] = self.values_list[j]
            percent_list.append(np.percentile(result, self.percentile))

        return percent_list