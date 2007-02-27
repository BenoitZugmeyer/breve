#!/usr/bin/python

try:
    from breve import Template
    from breve.tags import html
    from breve.util import Namespace
    from breve.flatten import register_flattener
    from breve.globals import register_global
except ImportError:
    print 'run "python setup.py install" from the parent directory first'
    raise SystemExit


Template.tidy = True

########## test basic functionality
from datetime import datetime

def flatten_datetime ( o ):
    return o.strftime ( '%Y/%m/%d' )
register_flattener ( datetime, flatten_datetime )
register_global ( 'today', datetime.today ( ) )

def example_renderer ( tag, data ):
    return tag ( class_ = 'custom-renderer' ) [
        'This was generated by a custom renderer.',
        'We also passed in this data: ', data
    ]


vars = dict ( 
    message = 'Hello, world!',
    example_renderer = example_renderer,
    username = 'admin',
    mytable = [ ( 'value', 'squared', 'cubed' ) ]
            + [ ( a, a**2, a**3 ) for a in range ( 10 ) ],
    person = { 'firstname': 'John', 'lastname': 'Doe' },
    userlist = [
        dict ( firstname = 'Ian', lastname = 'Bicking', projects = [ 'paste', 'sqlobject' ] ),
        dict ( firstname = 'Michael', lastname = 'Bayer', projects = [ 'sqlalchemy', 'mako', 'myghty' ] ),
        dict ( firstname = 'Kevin', lastname = 'Dangoor', projects = [ 'turbogears', 'zesty news' ] ),
        dict ( firstname = 'Ben', lastname = 'Bangert', projects = [ 'pylons' ] ),
        dict ( firstname = 'Bob', lastname = 'Ippolito', projects = [ 'mochikit', 'mochibot' ] )
    ]
)

for root, template in [ ( '1_basics', 'index' ),
                        ( '2_includes', 'index' ),
                        ( '3_inheritance', 'fragment' ),
                        ( '4_flatteners', 'index' ),
                        ( '5_conditionals', 'index' ),
                        ( '6_dynamic_inheritance', 'fragment' ),
                        ( '7_escape_artist', 'index' ),
                        ( '10_patterns', 'index' ) ]:
    print "RUNNING EXAMPLE", root, template
    print "=" * 40
    t = Template ( html.tags, root = root, doctype = html.doctype, xmlns = html.xmlns )
    print t.render ( template = template, vars = vars )
    print "\n\n\n"

####### test custom loaders
import os

class PathLoader ( object ):
    __slots__ = [ 'paths' ]

    def __init__ ( self, *paths ):
        self.paths = paths

    def stat ( self, template, root ):
        for p in self.paths:
            f = os.path.join ( root, p, template )
            if os.path.isfile ( f ):
                timestamp = long ( os.stat ( f ).st_mtime )
                uid = f
                return uid, timestamp
        raise OSError, 'No such file or directory %s' % template
    
    def load ( self, uid ):
        return file ( uid, 'U' ).read ( )

class StringLoader ( object ):
    __slots__ = [ ]
    
    def stat ( self, template, root ):
        return ( root, template ), 0

    def load ( self, uid ):
        return u'span [ "Hello, world" ]'
    
root, template = '9_custom_loaders', 'index'
pathloader = PathLoader ( 'inc1', 'inc2' )
stringloader = StringLoader ( )
vars = dict (
    loaders = Namespace ( {
        'pathloader': pathloader,
        'stringloader': stringloader
    } )
)

print "RUNNING EXAMPLE", root, template
print "=" * 40

t = Template ( tags = html.tags, root = root )
print t.render ( template = template, vars = vars )


    
raise SystemExit

####### test custom tags
import sys
sys.path.insert ( 0, '.' )
import sitemap # our custom tag definitions

vars = dict ( loc = 'http://www.example.com/',
              lastmod = '2007-01-01',
              changefreq = 'monthly',
              priority = 0.8 )
root, template = ( '8_custom_tags', 'index' )
print "RUNNING EXAMPLE", root, template
print "=" * 40

t = Template ( tags = sitemap.tags, xmlns = sitemap.xmlns, doctype = sitemap.doctype, root = root )
t.namespace = 'v'
print t.render ( template = template, vars = vars )
print "\n\n\n"


####### test it all!
root = 'A_all_features'

vars = dict (
    message = 'Hello, World.'
)

for template in [ 'include/index' ]:
    print "RUNNING EXAMPLE", root, template
    print "=" * 40

    t = Template ( tags = html.tags, xmlns = html.xmlns, doctype = html.doctype, root = root )
    t.namespace = 'v'
    print t.render ( template = template, vars = vars )
    print "\n\n\n"

