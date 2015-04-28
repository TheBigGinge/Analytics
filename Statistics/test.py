import entropy
import time
import numpy as np


method_1 = []
stat = entropy.EntropyStringMatching()
for i in xrange(0, 10000):
    start = time.time()
    #stat = entropy.EntropyStringMatching()
    stat.run("Data Analyst", 'Fancy Data Analyst')
    end = time.time()

    diff = (end - start) * 1000
    method_1.append(diff)

print "Method 1 returns an average of %s " % np.average(method_1)

method_2 = []

for i in xrange(0, 10000):
    start = time.time()
    calc = entropy.joint_entropy("Data Analyst", 'fancy data analyst') / entropy.entropy("Data Analyst")
    end = time.time()

    diff = (end - start) * 1000
    method_2.append(diff)

print "Method 2 returns an average of %s " % np.average(method_2)
