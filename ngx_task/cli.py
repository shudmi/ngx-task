import multiprocessing as mp
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from ngx_task import settings, utils


def generate_data():
    if not os.path.exists(settings.DATA_DIR):
        os.mkdir(settings.DATA_DIR, 0o755)

    files_to_submit = ['arc-{}.zip'.format(arc_num) for arc_num in range(1, 51)]

    with ThreadPoolExecutor() as pool:
        futures_to_process = {pool.submit(utils.archive_documents, filename): filename
                              for filename in files_to_submit}
        for fut in as_completed(futures_to_process):
            print('Complete {}'.format(futures_to_process[fut]))

        print('All data has been generated')


def process_data():
    file_queue = mp.JoinableQueue()
    object_queue = mp.JoinableQueue()

    file_worker = mp.Process(target=utils.worker, args=('files.csv', file_queue,))
    file_worker.start()
    object_worker = mp.Process(target=utils.worker, args=('objects.csv', object_queue,))
    object_worker.start()

    for arc in os.listdir(settings.DATA_DIR):
        path = os.path.join(settings.DATA_DIR, arc)
        utils.process_archive(path, file_queue, object_queue)

    file_queue.put(None)
    object_queue.put(None)

    file_queue.join()
    object_queue.join()
