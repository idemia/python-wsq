
import os,array
from PIL import Image, ImageFile

# _wsq is a C extension declaring: decompress, compress
import _wsq

#______________________________________________________________________________
class WSQEncoder:
    def __init__(self,args):
        self._args = args
        self.pushes_fd = False
    def setimage(self,im,*lost):
        self._im = im
    def encode(self,bufsize):
        c,r = self._im.size[0],self._im.size[1]
        # this is not efficient but PIL does not provide a getdata symetric to putdata
        a = array.array('B')
        a.fromlist(list(self._im))
        data = a.tobytes()
        buf = _wsq.compress(data,r,c,self._args)
        # status, errcode, buf
        # 1 = done, <0=error
        return 0,1,buf
    def encode_to_file(self,fh,bufsize):
        c,r = self._im.size[0],self._im.size[1]
        # this is not efficient but PIL does not provide a getdata symetric to putdata
        a = array.array('B')
        a.fromlist(list(self._im))
        data = a.tobytes()
        buf = _wsq.compress(data,r,c,self._args)
        os.write(fh,buf)
        # errcode
        return 1
    def cleanup(self):
        pass

def wsq_encoder(mode,args,*a,**kw):
    return WSQEncoder(args)

class WSQDecoder:
    def __init__(self,args):
        self._args = args
        self.pulls_fd = False
    def setimage(self,im,*lost):
        self._im = im
    def decode(self,data):
        buf,w,h,ppi = _wsq.decompress(data)
        self._im.putdata( buf )
        return -1,0
    def cleanup(self):
        pass
    
    
def wsq_decoder(mode,args=None):
    return WSQDecoder(args)
    
from PIL import _imaging
_imaging.wsq_encoder = wsq_encoder
_imaging.wsq_decoder = wsq_decoder

#______________________________________________________________________________
# Read WSQ image
def _accept(prefix):
    # detect FFA0 = marker for "start of image"
    return prefix[:2] == b'\xFF\xA0'

class WsqImageFile(ImageFile.ImageFile):

    format = "WSQ"
    format_description = "WSQ Bitmap"

    def _open(self):
        # XXX: maybe reading the whole buffer is not necessary
        buf = self.fp.read()
        # detect FFA2 (start of frame)
        pos = buf.find(b'\xFF\xA2')
        if pos<2:
            raise IOError("cannot decode WSQ image, missing SOF marker (FFA2)")
        # skip marker (2 bytes) + Frame length (2 bytes), A, B (1 byte each) = 6 bytes
        y = buf[pos+6]*256 + buf[pos+7]
        x = buf[pos+8]*256 + buf[pos+9]
        # we now have Y & X
        self.fp.seek(0)
        self.mode = "L"
        try:
            self.size = x,y
        except AttributeError:
            # Support Pillow >= 5.3.0
            self._size = x,y
        self.palette = None

        # arg = ratio
        self.tile = [("wsq",(0, 0)+self.size,0,(12,))]
        
    def load_read(self, bytes):
        # may be overridden for blocked formats (e.g. PNG)
        # for WSQ, one block only. We can safely close the stream
        ret = self.fp.read()
        self.fp.close()
        return ret
    
#______________________________________________________________________________
# Write WSQ image
def _save(im, fp, filename, check=0,*args,**kw):

    if im.mode!='L':
        raise IOError("cannot write mode %s as WSQ" % im.mode)

    if check:
        return check
    # 12 is the ratio we want
    ImageFile._save(im, fp, [("wsq", (0,0)+im.size, 0, (12,))])

#______________________________________________________________________________
# Registry

Image.register_open(WsqImageFile.format, WsqImageFile, _accept)
Image.register_save(WsqImageFile.format, _save)

Image.register_extension(WsqImageFile.format, ".wsq")
