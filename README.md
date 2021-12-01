# pyDhash

Multibase Perceptual Hash for Images

Written in Python

Inspired by http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html

hashImage({hashMethod}{hashChannels}{hashSize},{image})

hashMethods
    
    dhash
  
hashChannels - A string consisting of any of the following letters in any order
    
    L   R G B A   H S V   C M Y K

hashSize
    
    any integer greater than 1
 
Usage:

    import hash
    
    image = '/path/to/image'
    
    r = hash.hashImage("dhashLRGBA9",image)
    
    print(r)
