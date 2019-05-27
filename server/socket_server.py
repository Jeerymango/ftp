import socketserver,json,os,struct
from server import views

class MyFtpServer(socketserver.BaseRequestHandler):
    def put(self, msg):
        put_return = views.put(self, msg)
        return put_return


    def get(self, msg):
        get_return = views.get(self, msg)
        return get_return

    def remove(self, msg):
        remove_return = views.remove(self, msg)
        return remove_return

    def handle(self):
        msg = self.my_recv()
        operation_str = msg['operation']
        if hasattr(views,operation_str):
            func = getattr(views,operation_str)
            ret = func(msg)
            self.my_send(ret)

        # 处理上传 下载 删除
        while True:
            head_len = self.request.recv(4)
            head_len = struct.unpack('i',head_len)[0]
            dict_msg = self.my_recv(head_len)
            if hasattr(self,dict_msg['operation']):
                func1 = getattr(self,dict_msg['operation'])
                put_return = func1(dict_msg)
                self.my_send(put_return)


    def my_recv(self,len=1024):
        msg = self.request.recv(len)
        msg = msg.decode('utf-8')
        msg = json.loads(msg)
        return msg

    def my_send(self,msg):
        msg = str(msg)
        msg = msg.encode('utf-8')
        self.request.send(msg)

