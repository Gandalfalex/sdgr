import numpy as np
from scipy.spatial.distance import euclidean
import scipy

from fastdtw import fastdtw

x = [0.6724833437377331, -3.5875499788467007, 0.02954858845646413, -0.020555625571507363, 5.433840145031848,
     6.811562455795647, 20.04693036310733, 17.434640816875426, 18.19638666443939, 13.791866162694207,
     5.2249641196330225, -1.122531761222234, -7.189290321536299, -4.182749587882924, 1.9634806229720283,
     6.5594577726064385, 5.133601694463303, 19.577231568473245, 20.189678960916467, 20.01530840513949,
     18.987642982331813, 13.471715062559833, 3.616452345484344, -3.5160570062477996, -5.576226887632446,
     0.9048742454342484, 5.318970821548172, 7.483445569971478, 18.252919048032545, 21.187982676552757, -100.0,
     16.555348615008125, 13.77384701988668, 6.421232158234851, 2.1073962440976715, -0.7661301130638556,
     -7.445993125209359, 1.0571181370117122, 12.297451039581059, 11.346264319054587, 22.344752078640788,
     17.463509624792145, 20.715474939170996, 7.829400283898222, 5.781031535797444, -1.785685114667003,
     -2.474300241016362, -0.11757673955679415, -0.7672709040052013, 11.662933138767514, 11.153879509338136,
     18.393456599799208, 22.81379140638228, 16.558321598133425, 8.322465402747069, 7.074796256811425,
     1.8412101904931557, -5.546603451263953, -4.060454682159424, 0.8056483269085915, 100.0, 12.672130004895891,
     19.396864385833354, 19.37681410523084, 20.236632031240227, 12.154172466968548, 5.833154523566268,
     0.3187982003577883, -4.699102910963049, -7.994933713632084, -3.06268241962168, 4.13717545297462,
     11.968807938089785, 19.95784224385404, 16.678394602724715, 17.878061866902296, 15.542726116390881,
     10.080456636044593, 2.2149659574166556, -0.648727536229762, -8.157762326052131, 2.101867071257427,
     5.424110893944468, 8.267475463684606, 18.44702500252731, 21.334167343262138, 20.478197211464998, 12.210240810235,
     5.0356851211314915, -4.135355201540797, -3.1654173584931637, -7.309394995397927, 3.377511286624287,
     1.2399571096575817, 8.276616451580702, 15.97319787511188, 17.91713830068199, 20.70352841789982, 15.593900821519227,
     11.390149501773477]

y = [0 for i in x]



distance, path = fastdtw(np.array([x]), np.array([y]), dist=euclidean)
print(distance)




correlate_result = np.correlate(np.array(x), np.array(y), 'full')
print(sum(correlate_result))


temp = scipy.stats.kstest(np.array(x), np.array(y), args=(), N=20, alternative='two-sided', method='auto')
print(temp)