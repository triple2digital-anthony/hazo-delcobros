import time

def measure_fps():
    start_time = time.time()
    frame_count = 0
    
    def update():
        nonlocal frame_count
        frame_count += 1
    
    def get_fps():
        nonlocal start_time, frame_count
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time
        start_time = time.time()
        frame_count = 0
        return fps
    
    return update, get_fps
