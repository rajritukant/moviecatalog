from threading import Lock, Thread
request_counter = 0
lock = Lock()


class CounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        # set the counter to zero when the server starts
        global request_counter
        request_counter = 0
        # lock = Lock()

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print('in middleware')
        global request_counter
        # synchronizing updates to the counter by locking it
        global lock
        lock.acquire()
        request_counter += 1
        lock.release()
        print('request_counter')
        print(request_counter)
        self.process_request(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def get_counter(self):
        global request_counter
        return request_counter

    def reset_counter(self):
        global lock
        global request_counter
        lock.acquire()
        request_counter = 0
        lock.release()

    def process_request(self, request):
        print('in process request middleware')
        return None


# def counter_middleware(get_response):
#     # One-time configuration and initialization.

#     def middleware(request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.

#         response = get_response(request)

#         # Code to be executed for each request/response after
#         # the view is called.

#         return response

#     return middleware


# code for older versions of django
# class CounterMiddleware(object):
#     # def process_exception(self, request, exception):
#     #     return None

#     def process_request(self, request):
#         print('in middleware')
#         return None
