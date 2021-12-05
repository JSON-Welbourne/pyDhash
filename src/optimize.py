from PIL import Image
import os
import dhash
import time
import jellyfish

defaultConfig = {
    'min':          2,
    'max':          100,
    'hashType':     "dhashL",
    'tabString':    "    ",
    'images':       [   '/home/flask/images/cache/ABPDP/crqqqyprfikvstylhlhp.jpg',
                        '/home/flask/images/cache/ABPWM/24142.jpg', ], }

def main(**kwargs):
    hashType = kwargs.get('hashType')
    hashChannels = len(hashType)-5
    paths = kwargs.get('images')    
    minI = kwargs.get('min')
    maxI = kwargs.get('max')
    tabString = kwargs.get('tabString')
    images = {}
    print("hashChannels:    {}".format(hashChannels))
    for p in paths:
        try:
            if os.path.isfile(p):
                print("Found `{}`".format(p))
                images[p] = Image.open(p)
            else:
                print("Unable to find `{}`".format(p))
        except Exception as e:
            print("ERROR Initializing Paths, path = {}: {}".format(p,e))
    hashes = {}
    deviations = {}
    for i in range(minI,maxI):
        try:            
            for path in paths:
                try:
                    key = "{}:{}".format(i,path)
                    hashes[key] = dhash.hashImage('{}{}'.format(hashType,i),images[path])
                    hashString = hashes[key]['string']
                    print("[{}.{}]".format(
                        i, path))
                    if len(hashString) < (76*20):
                        lines = int((len(hashString)/hashChannels) ** (1/2))
                        [print("    {}".format(
                            " ".join([
                                hashString[(hashPart * int(len(hashString)/hashChannels)) + (hashLine * int(len(hashString)/(hashChannels*lines))) :
                                           (hashPart * int(len(hashString)/hashChannels)) + ((hashLine + 1) * int(len(hashString)/(hashChannels*lines)))]
                                for hashPart in range(5)])))
                            for hashLine in range(lines)]
                    else:
                        pass
                        # [print("    {}".format(
                        #     hashString[i2 * int(len(hashString)/5): (i2 + 1) * int(len(hashString)/5)])) for i2 in range(5)]
                    if 'errors' in hashes[key] and len(hashes[key]['errors']) > 0:
                        [print("{}{}".format(tabString * 1, e)) for e in hashes[key]['errors'] if e['location'][-1] != 'A']
                except Exception as e:
                    print("ERROR, path = {}: {}".format(path,e))
            if dhash.hashToString(hashes["{}:{}".format(i,paths[0])]) != dhash.hashToString(hashes["{}:{}".format(i,paths[1])]):
                deviations[i] = jellyfish.hamming_distance(
                    hashes["{}:{}".format(i,paths[0])]['decoded'],
                    hashes["{}:{}".format(i,paths[1])]['decoded'] )
            print("{}Deviation: {} / {} = {}".format(
                tabString * 1,
                deviations[i],
                hashChannels * 2 * i ** 2,
                int(10000 * deviations[i] / (hashChannels * 2 * i ** 2))/100))
        except Exception as e:
            print("ERROR, i = {}: {}".format(i,e))

            # deviations = {
    #     k:v for k,v in deviations.items() 
    #     if ((k == minI
    #         or (int(10000 * (v / (5 * 2 * k ** 2))) >= int(10000 * (deviations[max([k2 for k2 in deviations.keys() if k2 < k])] / (5 * 2 * (max([k2 for k2 in deviations.keys() if k2 < k])) ** 2))))
    #     and (k >= maxI 
    #         or int(10000 * (v / (5 * 2 * k ** 2))) >= int(10000 * (deviations[min([k2 for k2 in deviations.keys() if k2 > k])] / (5 * 2 * (min([k2 for k2 in deviations.keys() if k2 > k])) ** 2))))))}

    for k,v in deviations.items():
        try:
            print("{}{}: {}{} / {}{} = {}".format(
                tabString * 1,
                k,
                " " * (max([len(str(k1)) + len(str(v1)) for k1,v1 in deviations.items()]) - len(str(k)) - len(str(v))),
                v, hashChannels * 2 * k ** 2,
                " " * (max([len(str(hashChannels*2*k1**2)) for k1 in deviations.keys() ]) - len(str(hashChannels*2*k**2))),
                int(10000 * (v / (hashChannels * 2 * k ** 2)))/100 ))
        except Exception as e:
            print("ERROR, (k,v) = {},{}: {}".format(k,v,e))

    print("Summary of Hash `{}`".format(hashType))
    deviations = {
        k:v for k,v in deviations.items() 
        if ((k == minI or k > maxI)
            or all([
                int(10000 * (v / (hashChannels * 2 * k ** 2))) >= 
                int(10000 * (deviations[k2] / (hashChannels * 2 * k2 ** 2)))
                for k2 in deviations.keys() if k2 < k]))}
    for k,v in deviations.items():
        print("{}{}: {}{} / {}{} = {}".format(
            tabString * 1,
            k,
            " " * (max([len(str(k1)) + len(str(v1)) for k1,v1 in deviations.items()]) - len(str(k)) - len(str(v))),
            v, hashChannels * 2 * k ** 2,
            " " * (max([len(str(hashChannels*2*k1**2)) for k1 in deviations.keys() ]) - len(str(hashChannels*2*k**2))),
            int(10000 * (v / (hashChannels * 2 * k ** 2)))/100 ))

if __name__ == "__main__":
    import sys
    config = defaultConfig
    for i,a in enumerate(sys.argv):
        if i == 0 or i == 1:
            pass
        elif a.startswith('dhash'):
            config['hashType'] = a
        elif a == 'min':
            config['minArg'] = i
        elif i == config.get('minArg',-1):
            config['min'] = a
        elif a == 'max':
            config['maxArg'] = i
        elif i == config.get('maxArg',-1):
            config['max'] = a
        else:
            if config['images'] == defaultConfig['images']:
                config['images'] = []
            config['images'].append(a)
    try:                
        main(**config)
    except Exception as e:
        print("ERROR: {}".format(e))
