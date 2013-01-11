#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from xml.etree import ElementTree
import os
import conf4BlogListInGithub

mmdir = "D:\WorkSpace\FreeMindTools\MM"
mddir = "D:\WorkSpace\syman\_posts"
class MMTransform():
    """freemind's file(.mm) transform tools"""

    def mm2md(self, mmFileContent):
        md = []
        mmtree = ElementTree.XML(mmFileContent)
        for node in mmtree.find('node').findall('node'):
            self._mm2SimpleMd(node, md)
        return os.linesep.join(md)

    def mm2notes(self, mmFileContent):
        pass

    def mm2s5(self, mmFileContent):
        pass

    def _mm2SimpleMd(self, node, md, num=0):
        if node.get('TEXT'):
            branchcontent = []
            '''when find html tag,not transform'''
            if node.attrib['TEXT'].find('<'):
                if num == 1:
                    branchcontent = ['- ']
                elif num == 0:
                    branchcontent = ['# ']
                else:
                    branchcontent = ['        ']
            branchcontent.append(node.attrib['TEXT'])
            md.append(''.join(branchcontent))

            for childbranch in node.getchildren():
                self._mm2SimpleMd(childbranch, md, num + 1)


class MakeBlogInGithub():
    """make blog by markdown file in github.com"""
    def _getconf(self,mdFilename):
        return conf4BlogListInGithub.bloglist[mdFilename]

    def md2blog(self, md, mdFilename):
        config = self._getconf(mdFilename)
        
        prefix = []
        prefix.append('---')
        prefix.append('layout : '+config['layout'])
        prefix.append('category : ' + config['category'])
        prefix.append('tags : ' + '[' + ', '.join(config['tags'].split(',')) + ']')
        prefix.append('title : ' + config['title'])
        prefix.append('---')
        prefix.append('[思维导图文件下载]('+config['mmLink']+')')
        prefix.append(md)
        return  os.linesep.join(prefix)
		

def main():
	mblog = MakeBlogInGithub()
	file_list = [f_name for f_name in os.listdir(mmdir) if f_name.endswith('mm')]
	print file_list
	for filename in file_list:
		print filename
		mmFilename = filename
		mdFilename = mblog._getconf(mmFilename)['mdfname'].encode('utf8')
		mm = file(os.path.join(mmdir,mmFilename),'rb')
		md = file(os.path.join(mddir,mdFilename),'wb')
		transform = MMTransform()
		md.write(mblog.md2blog(transform.mm2md(mm.read()).encode('utf8'), mmFilename))
		# md.write(transform.mm2md(mm.read()).encode('utf8'))
		mm.close()
		md.close()


def gitpull():
	os.chdir(mddir)
	os.system('git pull')




def gitpush():
	os.chdir(mddir)
	os.system('git add .')
	os.system('git commit -m "post blogs"')
	os.system('git push')

if __name__ == "__main__":
	gitpull()
	main()
	gitpush()
