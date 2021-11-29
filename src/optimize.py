from PIL import Image
import dhash
import time
import jellyfish

paths = [
    '/home/flask/images/cache/ABPDP/crqqqyprfikvstylhlhp.jpg',
    '/home/flask/images/cache/ABPWM/24142.jpg', ]
images = {p:Image.open(p) for p in paths}
minI = 1
maxI = 100
tabString = "    "
hashes = {}
deviations = {}
for i in range(minI,maxI):
    for path in paths:
        key = "{}:{}".format(i,path)
        hashes[key] = dhash.hashImage('dhashLRGBA{}'.format(i),images[path])
        hashString = dhash.hashToString(hashes[key])
        print("[{}.{}]".format(
            i, path))
        if len(hashString) < (76*20):
            lines = int((len(hashString)/5) ** (1/2))
            [print("    {}".format(
                " ".join([
                    hashString[(hashPart * int(len(hashString)/5)) + (hashLine * int(len(hashString)/(5*lines))) :
                               (hashPart * int(len(hashString)/5)) + ((hashLine + 1) * int(len(hashString)/(5*lines)))]
                    for hashPart in range(5)])))
                for hashLine in range(lines)]
        else:
            pass
            # [print("    {}".format(
            #     hashString[i2 * int(len(hashString)/5): (i2 + 1) * int(len(hashString)/5)])) for i2 in range(5)]
        if 'errors' in hashes[key] and len(hashes[key]['errors']) > 0:
            [print("{}{}".format(tabString * 1, e)) for e in hashes[key]['errors'] if e['location'][-1] != 'A']
    if dhash.hashToString(hashes["{}:{}".format(i,paths[0])]) != dhash.hashToString(hashes["{}:{}".format(i,paths[1])]):
        deviations[i] = jellyfish.hamming_distance(
            dhash.decodeHash(hashImage.hashToString(hashes["{}:{}".format(i,paths[0])]), parts=5),
            dhash.decodeHash(hashImage.hashToString(hashes["{}:{}".format(i,paths[1])]), parts=5) )
    print("{}Deviation: {} / {} = {}".format(
        tabString * 1,
        deviations[i],
        5 * 2 * i ** 2,
        int(10000 * deviations[i] / (5 * 2 * i ** 2))/100))
# deviations = {
#     k:v for k,v in deviations.items() 
#     if ((k == minI
#         or (int(10000 * (v / (5 * 2 * k ** 2))) >= int(10000 * (deviations[max([k2 for k2 in deviations.keys() if k2 < k])] / (5 * 2 * (max([k2 for k2 in deviations.keys() if k2 < k])) ** 2))))
#     and (k >= maxI 
#         or int(10000 * (v / (5 * 2 * k ** 2))) >= int(10000 * (deviations[min([k2 for k2 in deviations.keys() if k2 > k])] / (5 * 2 * (min([k2 for k2 in deviations.keys() if k2 > k])) ** 2))))))}
deviations = {
    k:v for k,v in deviations.items() 
    if ((k == minI or k > maxI)
        or all([
            int(10000 * (v / (5 * 2 * k ** 2))) >= 
            int(10000 * (deviations[k2] / (5 * 2 * k2 ** 2)))
            for k2 in deviations.keys() if k2 < k]))}
for k,v in deviations.items():
    print("{}{}: {}{} / {}{} = {}".format(
        tabString * 1,
        k,
        " " * (max([len(str(k1)) + len(str(v1)) for k1,v1 in deviations.items()]) - len(str(k)) - len(str(v))),
        v, 5 * 2 * k ** 2,
        " " * (max([len(str(5*2*k1**2)) for k1 in deviations.keys() ]) - len(str(5*2*k**2))),
        int(10000 * (v / (5 * 2 * k ** 2)))/100 ))
