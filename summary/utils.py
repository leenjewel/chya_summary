import md5

def md5_encode(txt) :
    md5_obj = md5.new()
    md5_obj.update(txt)
    return md5_obj.hexdigest()

