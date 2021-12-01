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
    
    hash.hashImage("dhashLRGBA9",image)
    
    hash.hashImage("dhashL8",image)
    
    hash.hashImage("dhashHSV19",image)
    
    hash.hashImage("dhashRGB8",image)
    
    hash.hashImage("dhashLRGBAHSVCMYK9",image)
    
    hash.hashImage("dhashBAG9",image)
    
    hash.hashImage("dhashSLAKY13",image)
    
    
