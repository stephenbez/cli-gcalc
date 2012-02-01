#!/usr/bin/python

import sys
import urllib
import urllib2
import demjson

# I use the demjson library because the google calculator returns non-standard
# json where the keys are not quoted

def do_calculation(query):
    url = "http://www.google.com/ig/calculator?hl=en&q="

    # Must quote to convert spaces to %20, etc.
    url += urllib.quote(query)

    #print url

    r = urllib2.urlopen(url).read()

    # The response uses a non-breaking space encoded as 0xa0 as the thousands separator.
    # From the chart here: http://en.wikipedia.org/wiki/Non-breaking_space
    # we know that the response is using latin-1 encoding
    r = r.decode('latin-1').encode('utf-8')

    # I prefer commas as my thousands separator
    r = r.replace("\xC2\xA0", ",")
    #print r

    result = demjson.decode(r)

    #print result

    if result["error"] != "":
        return "ERROR: " + result["error"]
    else:
        return result["rhs"]

if __name__ == '__main__':
    if (len(sys.argv) == 1):
        print "Usage: " + sys.argv[0] + ' "12+34"'
        sys.exit()

    print do_calculation(sys.argv[1])
