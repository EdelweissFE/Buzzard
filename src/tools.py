
def getDictFromString( string, separator = "," ):

    d = {}

    split = string.split( separator )

    for s in split:
        if "=" in s:
            a = s.split("=")
            try:
                d[ a[0].lower() ] = float( a[1] )
            except:
                d[ a[0].lower() ] = a[1]


    return d 

