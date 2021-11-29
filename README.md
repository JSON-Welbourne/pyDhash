# pyDhash

Multibase Perceptual Hash for Images

Written in Python

hashImage(<hashMethod><hashChannels><hashSize>,<image>)

hashMethods
  
  dhash
  
hashChannels
  
  A string consisting of any of the following letters in any order
  
  L - Luminance
  
  R - Red
  
  G - Green
  
  B - Blue
  
  A - Alpha
  
hashSize
  
  any integer greater than   
 
Examples:

import hash
image = '/path/to/image'
r = hash.hashImage("dhashLRGBA9",image)
print(r)
