#!/usr/bin/env python

import os
import re
import sys
import glob
import lxml.etree
import Bcfg2.Options
from Bcfg2.Server import XMLParser


SPECIFIC = re.compile(r'.*\/(white|black)list'
                      r'(\.(H_(?P<host>.*)|G\d+_(?P<group>.*)))?$')


def convert(files, xdata):
    hosts = []
    groups = []
    for oldfile in files:
        spec = SPECIFIC.match(oldfile)
        if spec and spec.group('host'):
            hosts.append(spec.group('host'))
        elif spec and spec.group('group'):
            groups.append(spec.group('group'))

    for oldfile in files:
        print("Converting %s" % oldfile)
        spec = SPECIFIC.match(oldfile)
        if not spec:
            print("Skipping unknown file %s" % oldfile)
            continue

        parent = xdata
        if spec.group('host'):
            for host in hosts:
                if host != spec.group('host'):
                    parent = lxml.etree.SubElement(parent, "Client",
                                                   name=host, negate="true")
            parent = lxml.etree.SubElement(parent, "Client",
                                           name=spec.group('host'))
        elif spec.group('group'):
            for host in hosts:
                parent = lxml.etree.SubElement(parent, "Client",
                                               name=host, negate="true")
            for group in groups:
                if group != spec.group('group'):
                    parent = lxml.etree.SubElement(parent, "Group",
                                                   name=group, negate="true")
            parent = lxml.etree.SubElement(parent, "Group",
                                           name=spec.group('group'))
        parent.append(lxml.etree.Comment("Converted from %s" % oldfile))
        olddata = lxml.etree.parse(oldfile, parser=Bcfg2.Server.XMLParser)
        for decision in olddata.xpath('//Decision'):
            parent.append(decision)
    return xdata


def main():
    opts = dict(repo=Bcfg2.Options.SERVER_REPOSITORY,
                configfile=Bcfg2.Options.CFILE)
    setup = Bcfg2.Options.load_option_parser(opts)
    setup.parse(sys.argv[1:])

    datadir = os.path.join(setup['repo'], 'Decisions')
    whitelist = lxml.etree.Element("Decisions")
    blacklist = lxml.etree.Element("Decisions")
    if os.path.exists(datadir):
        convert(glob.glob(os.path.join(datadir, 'whitelist*')),
                whitelist)
        convert(glob.glob(os.path.join(datadir, 'blacklist*')),
                blacklist)

    print("Writing %s" % os.path.join(datadir, "whitelist.xml"))
    open(os.path.join(datadir, "whitelist.xml"),
         'w').write(lxml.etree.tostring(whitelist, pretty_print=True))
    print("Writing %s" % os.path.join(datadir, "blacklist.xml"))
    open(os.path.join(datadir, "blacklist.xml"),
         'w').write(lxml.etree.tostring(blacklist, pretty_print=True))


if __name__ == '__main__':
    sys.exit(main())
