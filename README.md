# pyDhash

Multibase Perceptual Hash for Images

Written in Python

Inspired by http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html

hashImage({hashMethod}{hashChannels}{hashSize},{image})

hashMethods
    
    dhash
  
hashChannels - A string consisting of any of the following letters in any order
    
    L - Luminance
    
    R - Red
    
    G - Green
    
    B - Blue
    
    A - Alpha
    
    H - Hue
    
    S - Saturation
    
    V
    
    C
    
    M
    
    Y
    
    K
  
hashSize
    
    any integer greater than 1
 
Usage:

    import hash
    
    image = '/path/to/image'
    
    r = hash.hashImage("dhashLRGBA9",image)
    
    print(r)
