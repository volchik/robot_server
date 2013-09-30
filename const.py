#content type
ext2conttype = {"jpg"  : "image/jpg",
                "jpeg" : "image/jpeg",
                "png"  : "image/png",
                "gif"  : "image/gif",
		"ico"  : "image/ico",
		"txt"  : "text/text",
		"html" : "text/html",
		"htm"  : "text/html",
                "js"   : "text/javascript"}

#allow file ext
d_allowtype =  {"jpg"  : "",
		"jpeg" : "",
		"png"  : "",
		"gif"  : "",
		"ico"  : "",
		"js"   : ""}


def file_ext(filename):
	if filename.rfind(".") != 0:
		return filename[filename.rfind(".")+1:].lower()
	else:
		return ""


def file_type(filename):
	try:
		ext = file_ext(filename)
		if ext2conttype.get(ext) != None:
			return ext2conttype.get(ext)
	except:
		return ""


def file_allow(filename):
	if d_allowtype.get(file_ext(filename)) != None:
		return True
	else: return False
