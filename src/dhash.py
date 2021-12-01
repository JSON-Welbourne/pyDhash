from PIL import Image
import base64
import math

def decodeHash(hashString,parts = 4):
    return ''.join(["{:08b}".format(b) for i in range(parts) for b in base64.b64decode(
        hashString[i*int(len(hashString)/parts):(i+1)*int(len(hashString)/parts)])])

def hashToString(hash):
    return "".join([v for k,v in hash['output'].items()])

def hashImage(method,image,outputFormat="base64"):
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
                channels = [c for c in method[5:] if c in 'LRGBA']
                size = int(method[5+len(channels):])
                size = size if size >= 2 else 2
                width = size + 1
                height = size + 1
                for channel in channels:
                    try:
                        channel_data = list((
                                image.convert("L") 
                                if channel == 'L' 
                                else image.getchannel(channel))
                            .resize((width, height), Image.ANTIALIAS)
                            .getdata())
                        hash = {
                            'row': 0,
                            'col': 0, }
                        for y in range(size):
                            for x in range(size):
                                offset = y * width + x
                                hash['row'] = hash['row'] << 1 | (channel_data[offset] < channel_data[offset + 1])
                                hash['col'] = hash['col'] << 1 | (channel_data[offset] < channel_data[offset + width])
                        data = (hash['row'] << (size * size) | hash['col'])
                    except Exception as e:
                        data = 0
                        errors.append({
                            'location':'{}.{}'.format(method,channel),
                            'error':str(e),})                    
                    if outputFormat == 'base64':
                        bytesNeeded = math.ceil(((size)**2)/4)
                        output[channel] = base64.b64encode(data.to_bytes(bytesNeeded,'big')).decode("utf-8") # Base 64
                    elif outputFormat in ['base10','decimal','denary']:
                        bytesNeeded = len(str(data))
                        output[channel] = str(data)
                    elif outputFormat in ['base16','hex','hexadecimal']:
                        bytesNeeded = math.ceil(((size)**2)/4)
                        output[channel] = "%0{}X".format(int(bytesNeeded/2)) % (data) # Base 16 (Hex)
                    else:
                        errors.append({
                            'location': 'Convert Hash to String',
                            'error': 'Output Format Not Recognized', })
            else:
                errors.append({
                    'location':'Main',
                    'error':'Method NOT Recognized',})
        except Exception as e:
            errors.append({
                'location': 'Main',
                'error': str(e),})
    else:
        errors.append({
            'location': 'Main',
            'error': 'Invalid Image',})
    return {'output':output,'errors':errors}
