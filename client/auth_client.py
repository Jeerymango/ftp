from client.socket_client import MySocketClient
import os,json,struct,hashlib
from client.progress_bar import progress_bar
class Auth:
    '''单例模式  防止重复登录注册时多次创建连接'''
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            obj = object.__new__(cls)
            cls.__instance = obj
        return cls.__instance

    def __init__(self):
        self.socket = MySocketClient()
        self.username = None

    # 登录
    def login(self):
        username = input('username :')
        password = input('password :')
        if username.strip() and password.strip():
            msg = {'username':username,'password':password,'operation':'login'}
            self.socket.mysend(msg=msg)
        else:
            msg = {'username':username,'password':password,'operation':'login'}
            self.socket.mysend(msg=msg)

        ret = self.socket.sk.recv(1024)
        return ret.decode('utf-8')

    # 注册
    def register(self):
        username = input('username :')
        password1 = input('password :')
        password2 = input('password_ensure :')
        if username.strip() and password1.strip() and password1 == password2:
            msg = {'username':username,'password':password1,'operation':'register'}
            self.socket.mysend(msg)
        ret = self.socket.sk.recv(1024)
        return ret.decode('utf-8')

    # 上传
    def put(self,send_dict):
        buffer = 1024
        # 自定义报头
        head = {'username':send_dict['username'],
                'filepath': send_dict['dir'],
                'operation':'put',
                'filesize': None}
        filesize = os.path.getsize(head['filepath'])
        head['filesize'] = filesize
        json_head = json.dumps(head)
        bytes_head = json_head.encode('utf-8')
        head_len = len(bytes_head)
        struct_len = struct.pack('i', head_len)
        self.socket.sk.send(struct_len)
        self.socket.sk.send(bytes_head)

        with open(head['filepath'], 'rb')as f:
            received_size = 0
            total = filesize
            progress = progress_bar(received_size,total)
            progress.__next__()
            while filesize:
                if filesize >= buffer:
                    content = f.read(buffer)
                    filesize -= buffer
                    received_size += buffer
                    self.socket.sk.send(content)
                    try:
                      progress.send(buffer)
                    except StopIteration as e:
                      print("100%")
                else:
                    content = f.read(filesize)
                    self.socket.sk.send(content)
                    filesize = 0
                    break

        ret = self.socket.sk.recv(1024)
        return ret.decode('utf-8')

    #下载
    def get(self,send_dict):
        buffer = 1024
        # 自定义报头
        head = {'username':send_dict['username'],
                'filename': send_dict['dir'],
                'operation':'get'}

        json_head = json.dumps(head)
        bytes_head = json_head.encode('utf-8')
        head_len = len(bytes_head)
        struct_len = struct.pack('i', head_len)
        self.socket.sk.send(struct_len)
        self.socket.sk.send(bytes_head)

        try:
            filesize_len = self.socket.sk.recv(4)
            filesize_len = struct.unpack('i', filesize_len)[0]
            json_filesize = self.socket.sk.recv(filesize_len)
            filesize = json.loads(json_filesize)
        except:
            return '下载失败,文件不存在'

        md5 =hashlib.md5()
        save_path = os.path.join(send_dict['get_to'],send_dict['dir'])
        with open(save_path, 'wb') as f:
            while filesize:
                if filesize >= buffer:
                    content = self.socket.sk.recv(buffer)
                    f.write(content)
                    filesize -= buffer
                    md5.update(content)
                else:
                    content = self.socket.sk.recv(filesize)
                    f.write(content)
                    md5.update(content)
                    break

        if self.socket.sk.recv(1024).decode('utf-8') == md5.hexdigest():
            return '下载成功'
        else:
            return'下载失败'

    def remove(self,send_dict):
        # 自定义报头
        head = {'username': send_dict['username'],
                'filepath': send_dict['dir'],
                'operation': 'remove'}

        json_head = json.dumps(head)
        bytes_head = json_head.encode('utf-8')
        head_len = len(bytes_head)
        struct_len = struct.pack('i', head_len)
        self.socket.sk.send(struct_len)
        self.socket.sk.send(bytes_head)

        ret = self.socket.sk.recv(1024)
        return ret.decode('utf-8')