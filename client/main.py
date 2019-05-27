from client.auth_client import Auth
import re
def main():
    auth_obj = None
    get_to = None
    file_path = None
    operation_l = [("登陆",'login'),("注册",'register'),("退出",'exit')]

    menu = '''\033[32;1m
                    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
                             帮    助                   输入的文件名或路径
                            【1】上   传      put         需要上传的文件路径
                            【2】下   载      get         已上传过的文件名
                            【3】删   除      remove      已上传过的文件名
                            【4】退   出      exit
                    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
                    \033[0m '''
    list_menu =[('1','put'),('2','get'),('3','remove'),('4','exit')]
    login_count = 0
    while login_count < 3:
        for index, item in enumerate(operation_l, 1):
            print(index, item[0])
        try:
            num = int(input('>>>'))
            func_str = operation_l[num-1][1]
        except:
            print('请输入1-3!')

        if hasattr(Auth,func_str):  #登录 注册
            auth_obj = Auth()
            func = getattr(auth_obj,func_str)
            ret = func()
            print(ret)
            s = re.findall('登陆成功', ret)
            if s and func_str == 'login':
                name =ret.replace('登陆成功','')
                while True:
                    print(menu)
                    while True:
                        try:
                            num = int(input('(输入需要执行的操作的序号(1-4)>>>'))
                            func_str1 = list_menu[num - 1][1]
                            if num == 4:
                                break
                            file_path = input('请输入文件名或目录名：')
                            if func_str1 == 'get':
                                get_to = input('下载到哪里:(输入完整路径)')
                            break
                        except:
                            print('输入有误,请重新输入正确数字')
                    send_dict = {'username': name, 'operation': None, 'dir': file_path,'get_to':get_to}
                    if hasattr(Auth, func_str1):
                        func = getattr(auth_obj, func_str1)
                        put_return = func(send_dict)
                        print(put_return)
                    else:
                        exit()

            elif ret and func_str == 'register': print('注册成功')

        elif auth_obj:      #之前选择登录注册过想退出
            auth_obj.socket.sk.close()
            exit()

        else:
            exit()

        login_count += 1


if __name__ == '__main__':
    main()