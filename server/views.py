import re,os,json,struct,hashlib
from server.pwd_md5 import my_md5
from server.user import User
from . import settings
# 登录
def login(msg):
    if msg['username'] =='' or msg['password'] == '':
        return '账号或密码不能为空'
    with open(settings.userinfo_path,'r')as f:
        for i in f:
            uname = msg['username'] +'|'
            if msg['username']==re.search(uname,i).group():
                file_pwd = re.search('\|.+\|',i).group().replace('|','')
                if my_md5(msg['password']) == file_pwd:
                    return  ('%s登陆成功'%msg['username'])
                else:
                    return '密码错误'
        else:
            return '没有该账户'

# 注册
def register(msg):
    user_obj = User(msg['username'])
    os.mkdir(user_obj.home)
    with open(settings.userinfo_path,'a')as f:
        pwd = my_md5(msg['password'])
        f.writelines('%s|%s|%s\n'%(msg['username'],pwd,user_obj.home))
    return '注册成功'

# 上传
def put(self,msg):
    filesize = msg['filesize']
    filename = os.path.split(msg['filepath'])
    user_obj = User(msg['username'])
    save_path = os.path.join(user_obj.home, filename[-1])

    with open(save_path, 'wb') as f:
        while filesize:
            if filesize >= settings.buffer:
                content = self.request.recv(settings.buffer)
                f.write(content)
                filesize -= settings.buffer
            else:
                content = self.request.recv(filesize)
                f.write(content)
                break
    return '上传成功'

# 下载
def get(self,msg):
    filename = msg['filename']
    user_obj = User(msg['username'])
    get_path = os.path.join(user_obj.home, filename)


    try:
        filesize = os.path.getsize(get_path)
        size_len = len(str(filesize))
        struct_len = struct.pack('i', size_len)
        self.request.send(struct_len)
        self.request.send(str(filesize).encode('utf-8'))
    except :
        return '文件不存在'

    md5 = hashlib.md5()
    with open(get_path, 'rb')as f:
        while filesize:
            if filesize >= settings.buffer:
                content = f.read(settings.buffer)
                filesize -= settings.buffer
                self.request.send(content)
                md5.update(content)
            else:
                content = f.read(filesize)
                self.request.send(content)
                filesize = 0
                md5.update(content)
                break

    return md5.hexdigest()

# 删除
def remove(self,msg):
    filename = msg['filepath']
    user_obj = User(msg['username'])
    get_path = os.path.join(user_obj.home, filename)

    try:
        os.remove(get_path)
        return ('%s删除成功'%msg['filepath'])
    except:
        return '要删除的文件不存在'

