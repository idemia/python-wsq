
import unittest
import io
import os
import tempfile

import PIL.Image
import wsq

#_______________________________________________________________________________
class WSQTestCase(unittest.TestCase):
    
    def test_wsq(self):
        # check we can read a WSQ compressed image
        i = PIL.Image.open(os.path.join(os.path.dirname(__file__),'test.wsq'))
        
        # rotate the image 45 degrees
        i = i.rotate(45)        
        # check we can save an image in wsq format
        buf = io.BytesIO()
        i.save(buf,'WSQ')
        self.assertGreater( len(buf.getvalue()) , 1000 )
        self.assertLess( len(buf.getvalue()) , i.size[0]*i.size[1]/10 )

        # Save in a file
        with tempfile.TemporaryFile() as tf:
            i.save(tf,'WSQ')
        
    def test_bad_mode(self):
        # Create a color image and try to save it as a WSQ
        i = PIL.Image.new("RGB",(100,100))
        buf = io.BytesIO()
        with self.assertRaises(IOError):
            i.save(buf,'WSQ')

    def test_bad_image(self):
        with open(os.path.join(os.path.dirname(__file__),'test.wsq'),'rb') as f:
            buf = f.read()
        buf = buf.replace(b'\xFF\xA2',b'\xFF\xFF')
        with self.assertRaises(IOError):
            i = PIL.Image.open(io.BytesIO(buf))

# ______________________________________________________________________________
if __name__=='__main__':
    unittest.main(argv=['-v'])
    
