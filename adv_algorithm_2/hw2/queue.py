#!/usr/bin python3.6


class Queue():
    def __init__(self, queue_list=[]):
        self.queue = queue_list

    def enqueue(self, item):
        # Adding elements to the queue
        self.queue.append(item)

    def show_queue(self):
        print(self.queue)

    def dequeue(self):
        # Removing elements from the queue
        if len(self.queue) <= 0:
            print('queue is empty')
            return None
        else:
            # print("Elements dequeued from queue")
            item = self.queue.pop(0)
            return item

    def notEmpty(self):
        if len(self.queue) == 0:
            return False
        else:
            return True


if __name__ == "__main__":
    test_queue = Queue([1, 2, 3])
    test_queue.show_queue()

    test_queue.enqueue(4)
    item = test_queue.dequeue()
    test_queue.show_queue()

    print(test_queue.notEmpty())

    test_queue.dequeue()
    test_queue.dequeue()
    test_queue.dequeue()
    test_queue.show_queue()
    print(test_queue.notEmpty())

    test_queue.enqueue(5)
    test_queue.show_queue()
    print(test_queue.notEmpty())
