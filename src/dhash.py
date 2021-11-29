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
    try:
        if method.startswith('dhash'):
            channels = [c for c in method[5:] if c in 'LRGBA']
            size = int(method[5+len(channels):])
            size = size if size >= 2 else 2
            width = size + 1
            height = size + 1
            s = {}
            for channel in channels:
                try:
                    channel_image = image.convert("L") if channel == 'L' else image.getchannel(channel)
                    small_image = channel_image.resize((width, height), Image.ANTIALIAS)
                    channel_data = list(small_image.getdata())
                    row_hash = 0
                    col_hash = 0
                    for y in range(size):
                        for x in range(size):
                            offset = y * width + x
                            row_bit = channel_data[offset] < channel_data[offset + 1]
                            row_hash = row_hash << 1 | row_bit
                            col_bit = channel_data[offset] < channel_data[offset + width]
                            col_hash = col_hash << 1 | col_bit
                    data = (row_hash << (size * size) | col_hash)
                except Exception as e:
                    data = 0
                    errors.append({
                        'location':'{}.{}'.format(method,channel),
                        'error':str(e),})
                if outputFormat == 'base64':
                    bytesNeeded = math.ceil(((size)**2)/4)
                    s[channel] = base64.b64encode(data.to_bytes(bytesNeeded,'big')).decode("utf-8") # Base 64
                elif outputFormat in ['hex','base16']:
                    bytesNeeded = math.ceil(((size)**2)/4)
                    s[channel] = "%0{}X".format(int(bytesNeeded/2)) % (data) # Base 16 (Hex)
            return {'output':s,'errors':errors}
        else:
            errors.append({
                'location':'Main',
                'error':'Method NOT Recognized',})
    except Exception as e:
        errors.append({
            'location': 'Main',
            'error': str(e),})
    return {'output':{},'errors':errors}
