# coding=utf-8
# Date: 15/1/30'
# Email: wangjian2254@icloud.com
__author__ = u'王健'
import sys,os

extens = [".js"]
linesCount = 0
filesCount = 0

def funCount(dirName):
    global extens,linesCount,filesCount
    for root,dirs,fileNames in os.walk(dirName):
        for f in fileNames:
            fname = os.path.join(root,f)
            try :
                ext = f[f.rindex('.'):]
                if(extens.count(ext) > 0):
                    print 'support'
                    filesCount += 1
                    print fname
                    # l_count = len(open(fname).readlines())
                    l_count = 0
                    for l in open(fname).readlines():
                        if len(l.strip()) > 0:
                            l_count += 1
                    print fname," : ",l_count
                    linesCount += l_count
                else:
                    print ext," : not support"
            except:
                print "Error occur!"
                pass


if len(sys.argv) > 1 :
    for m_dir in sys.argv[1:]:
        print m_dir
        funCount(m_dir)
else :
    funCount("../webhtml")

print "files count : ",filesCount
print "lines count : ",linesCount