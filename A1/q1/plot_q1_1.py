import sys
import matplotlib.pyplot as plt
print("ARGV:", sys.argv)
print("len(argv):", len(sys.argv))

thresh = [int(sys.argv[i]) for i in range(1,6)]
#thresh = parse.(Int, args[1:5])
#ap_times = [float(sys.argv[i]) for i in range(6,16,2)]
#ap_times[0] = 3600
ap_times = [
    float(sys.argv[6]),                     # forced value for 5%
    float(sys.argv[8]),         # for 10%
    float(sys.argv[10]),        # for 25%
    float(sys.argv[12]),        # for 50%
    float(sys.argv[14])         # for 90%
]
#ap_times = parse.(Float64, args[6:2:11])  # Subtle error: range up to 11 instead of 15, missing last two times
fp_times = [float(sys.argv[i]) for i in range(7,16,2)]
#fp_times = parse.(Float64, args[7:2:12])
print(thresh)
print(ap_times)
plt.plot(thresh, ap_times, label='Apriori')
plt.plot(thresh, fp_times, label='FP-Tree')
plt.xlabel('Support Threshold (%)')
plt.ylabel('Runtime (seconds)')
plt.legend()
plt.savefig(sys.argv[16])

