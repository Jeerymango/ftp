def progress_bar(received_size,total):
    current_percent = 0
    while received_size < total:
        if int((received_size / total) * 100) > current_percent :
            print("#",end="",flush=True)
            current_percent = (received_size / total) * 100
        new_size = yield
        received_size += new_size
