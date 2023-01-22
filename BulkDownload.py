#!/usr/bin/env python
# Script to download all .nc files from a THREDDS catalog directory
# Written by Sage 4/5/2016, revised 5/31/2018

from xml.dom import minidom
from urllib.request import urlopen
from urllib.request import urlretrieve

# Divide the url you get from the data portal into two parts
# Everything before "catalog/"
server_url = 'https://dapds00.nci.org.au/thredds/'
# Everything after "catalog/"
request_url = 'cj37/BARRA/BARRA_AD/v1/forecast/prs/air_temp/1990/01/'


def get_elements(url, tag_name, attribute_name):
    """Get elements from an XML file"""
    # usock = urllib2.urlopen(url)
    usock = urlopen(url)
    xmldoc = minidom.parse(usock)
    usock.close()
    tags = xmldoc.getElementsByTagName(tag_name)
    attributes = []
    for tag in tags:
        attribute = tag.getAttribute(attribute_name)
        attributes.append(attribute)
    return attributes


def main():
    url = server_url + request_url + 'catalog.xml'
    print(url)
    catalog = get_elements(url, 'dataset', 'urlPath')
    files = []
    for citem in catalog:
        if (citem[-3:] == '.nc'):
            files.append(citem)
    count = 0
    for f in files:
        count += 1
        file_url = server_url + 'fileServer/' + f
        file_prefix = file_url.split('/')[-1][:-3]
        file_name = file_prefix + '.nc'
        print('Downloaing file %d of %d' % (count, len(files)))
        print(file_name)
        a = urlretrieve(file_url, file_name)
        print(a)


# Run main function when in comand line mode
if __name__ == '__main__':
    main()
