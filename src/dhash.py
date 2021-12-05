from PIL import Image
import base64
import math

config = {
    'defaultBase':  64,
    'resizeFlags':  Image.ANTIALIAS,
    'supportedChannels': [
        'L',
        'RGBA',
        'HSV',
        'CMYK', ], }

def decodeHash(hashString,parts = 4):
    return ''.join(["{:08b}".format(b) for i in range(parts) for b in base64.b64decode(
        hashString[i*int(len(hashString)/parts):(i+1)*int(len(hashString)/parts)])])

def hashToString(hash):
    return "".join([v for k,v in hash['output'].items()])

def hashImage(method,image,outputFormat=config['defaultBase'],resizeFlags=config['resizeFlags']):
    errors = []
    output = {}
    if type(image) == str:
        try:
            image = Image.open(image)
        except Exception as e:
            image = None
    if 'PIL.' in str(type(image)):        
        try:
            if method.startswith('dhash'):
                channels = [c for c in method[5:] if c in "".join(config['supportedChannels'])]
                size = int(method[5+len(channels):])
                size = size if size >= 2 else 2
                width = size + 1
                height = size + 1
                for channel in channels:
                    try:                        
                        for channelGroup in config['supportedChannels']:
                            if channel in channelGroup:
                                channelData = list(image
                                   .convert(channelGroup)
                                   .getchannel(channel)
                                   .resize((width,height), resizeFlags)
                                   .getdata())
                        hash = {
                            'row': 0,
                            'col': 0, }
                        for y in range(size):
                            for x in range(size):
                                offset = y * width + x
                                hash['row'] = hash['row'] << 1 | (channelData[offset] < channelData[offset + 1])
                                hash['col'] = hash['col'] << 1 | (channelData[offset] < channelData[offset + width])
                        data = (hash['row'] << (size * size) | hash['col'])
                    except Exception as e:
                        data = 0
                        errors.append({
                            'location':'{}.{}'.format(method,channel),
                            'error':str(e),})                    
                    if outputFormat in [10,'10','base10','decimal','denary']:
                        bytesNeeded = len(str(data))
                        output[channel] = str(data)
                    elif outputFormat in [16,'16','base16','hex','hexadecimal']:
                        bytesNeeded = math.ceil(((size)**2)/4)
                        output[channel] = "%0{}X".format(int(bytesNeeded/2)) % (data) # Base 16 (Hex)
                    elif outputFormat in [64,'64','base64']:
                        bytesNeeded = math.ceil(((size)**2)/4)
                        output[channel] = base64.b64encode(data.to_bytes(bytesNeeded,'big')).decode("utf-8") # Base 64
                    else:
                        errors.append({
                            'location': 'Convert Hash to String',
                            'error': 'Output Format Not Recognized', })
                output['string'] = "".join([output[c] for c in channels])
                if outputFormat in [64,'64','base64']:                
                    output['decoded'] = ''.join([
                        "{:08b}".format(b) 
                        for i in range(len(channels)) 
                        for b in base64.b64decode(
                            output['string'][
                                i * int( len(output['string']) / len(channels) ) : 
                                (i + 1) * int( len(output['string']) / len(channels) ) ] ) ] )
            else:
                errors.append({
                    'location':'Main',
                    'error':'Hash Method NOT Recognized',})
        except Exception as e:
            errors.append({
                'location': 'Main',
                'error': str(e),})
    else:
        errors.append({
            'location': 'Main',
            'error': 'Invalid Image',})
    return {'output':output,'errors':errors}
