import os
import hashlib
 
def filecount():
    filecount = int(os.popen('dir /B |find /V /C ""').read())
    return (filecount)
 
 
def md5sum(filename):
    f = open(filename, 'rb')
    md5 = hashlib.md5()
    while True:
        fb = f.read(8096)
        if not fb:
            break
        md5.update(fb)
    f.close()
    return (md5.hexdigest())
 
 
def delfile():
    all_md5 = {}
    filedir = os.walk(os.getcwd())
    for i in filedir:
        for tlie in i[2]:
            if md5sum(tlie) in all_md5.values():
                os.remove(tlie)
            else:
                all_md5[tlie] = md5sum(tlie)
 
 
if __name__ == '__main__':
    cnt = 0
    p = os.getcwd()
    files = os.listdir(p)
    for f in files:
        try:
            if open(p + '/' + f, 'rb').read(1) == b'{':
                os.remove(p + '/' + f)
                cnt += 1
        except:
            pass
    print('删除%d个返回失败的文件\n' % cnt)

    
    oldf = filecount()
    print('去重前有', oldf, '个文件\n\n\n请稍等正在删除重复文件...')
    delfile()
    print('\n\n去重后剩', filecount(), '个文件')
    print('\n\n一共删除了', oldf - filecount(), '个文件\n\n')
    os.system('pause')
