import threading
import time

x = 0
def loop_func():
    global x
    while True:
        x += 1 
        print("Variable x:", x)
        time.sleep(1)

def task_func(latest_x):
    print("Performing task with x =", latest_x)
    time.sleep(5) # simulate some heavy task
    print("Task finished!")

if __name__ == "__main__":
    # Start loop in background thread
    loop_thread = threading.Thread(target=loop_func) 
    loop_thread.daemon = True
    loop_thread.start()

    while True:
        # Perform task with latest state of x
        latest_x = x 
        task_thread = threading.Thread(target=task_func, args=(latest_x,))
        task_thread.start()  
        task_thread.join()