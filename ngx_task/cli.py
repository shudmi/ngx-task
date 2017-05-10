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
