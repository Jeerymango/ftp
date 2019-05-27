from server.socket_server import MyFtpServer
import socketserver

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1',8081),MyFtpServer)
    server.serve_forever()