from django import template
from django.template.defaultfilters import stringfilter
from os.path import splitext, basename
from xml.dom import minidom
from urlparse import urlparse
import urllib2, json, re, os

register = template.Library()

@register.filter
@stringfilter
def oembed(oembed_url):
    width = 400
    height = 300
    services = {
        'youtube.com': 'youtube',
        'youtu.be': 'yoube',
        'vimeo.com': 'vimeo',
        'vine.co': 'vine',
        'facebook.com': 'facebook',
        #'imgur.com': 'imgur'
    }

    parsedUrl = urlparse(oembed_url)

    url = parsedUrl.netloc
    url = url.replace("www.", "", 1)

    if url not in services:
        # Check if url is image
        images = ['.jpg', '.jpeg', '.gif', '.png']
        disassembled = urlparse(oembed_url)
        filename, file_ext = splitext(basename(disassembled.path))

        print file_ext
        if file_ext in images:
            embedHtml = "<a href='{image}' ><img src='{image}' height=300 alt='{name}' /></a>".format(image=oembed_url, name=filename)
            return embedHtml
        else:
            return ""
    else:
        provider = services[url]
        try:
            # Youtube
            if provider is 'youtube':
                videoCode = parsedUrl.query[-11:]
                embedHtml = "<iframe width=\"{width}\" height=\"{height}\" src=\"//www.youtube.com/embed/{video}\" frameborder=\"0\" allowfullscreen></iframe>".format(width=width, height=height, video=videoCode)
                embedHtml = re.sub('http', 'https', embedHtml)
                return embedHtml

            # Vimeo
            elif provider is 'vimeo':
                videoCode = parsedUrl.path[-8:]
                embedHtml = "<iframe src=\"//player.vimeo.com/video/{video}\" width=\"{width}\" height=\"{height}\" frameborder=\"0\" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>".format(width=width, height=height, video=videoCode)
                embedHtml = re.sub('http', 'https', embedHtml)
                return embedHtml

            # Youtu.be
            elif provider is 'yoube':
                videoCode = parsedUrl.path[-11:]
                embedHtml = "<iframe width=\"{width}\" height=\"{height}\" src=\"//www.youtube.com/embed/{video}\" frameborder=\"0\" allowfullscreen></iframe>".format(width=width, height=height, video=videoCode)
                embedHtml = re.sub('http', 'https', embedHtml)
                return embedHtml

            # Vine
            elif provider is 'vine':
                videoCode = parsedUrl.path[-11:]
                embedHtml = "<iframe class=\"vine-embed\" src=\"https://vine.co/v/{video}/embed/simple\" width=\"{width}\" height=\"{height}\" frameborder=\"0\"></iframe>".format(width=width, height=height, video=videoCode)
                if parsedUrl.scheme is "http":
                    embedHtml = re.sub('http', 'https', embedHtml)
                return embedHtml

            # Facebook
            elif provider is 'facebook':
                par = urlparse.parse_qs(urlparse.urlparse(url).query)
                videoCode = par['v']
                print videoCode
                embedHtml = "<object width=\"{width}\" height=\"{height}\" ><param name=\"allowfullscreen\" value=\"true\" /><param name=\"allowscriptaccess\" value=\"always\" /><param name=\"movie\" value=\"http://www.facebook.com/v/{video}\" /><embed src=\"http://www.facebook.com/v/{video}\" type=\"application/x-shockwave-flash\" allowscriptaccess=\"always\" allowfullscreen=\"true\" width=\"{width}\" height=\"{height}\"></embed></object>".format(width=width, height=height, video=videoCode)
                if parsedUrl.scheme is "http":
                    embedHtml = re.sub('http', 'https', embedHtml)
                return embedHtml

            # Imgur TODO
            '''
            elif provider is 'imgur':
                # Check if url is image
                images = ['.jpg', '.jpeg', '.gif', '.png']
                disassembled = urlparse(oembed_url)
                filename, file_ext = splitext(basename(disassembled.path))

                print file_ext
                if file_ext in images:
                    embedHtml = "<a href='{image}' ><img src='{image}' height=300 alt='{name}' /></a>".format(image=oembed_url, name=filename)
                    return embedHtml
                else:
                    # Try to show picture anyway

             '''
        except Exception:
            return ""
