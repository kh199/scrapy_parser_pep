import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
FILE_NAME = 'status_summary_%Y-%m-%d_%H-%M-%S.csv'


class PepParsePipeline:

    def open_spider(self, spider):
        self.status_dict = defaultdict(int)

    def process_item(self, item, spider):
        self.status_dict[item['status']] += 1
        return item

    def close_spider(self, spider):
        filename = datetime.now().strftime(FILE_NAME)
        total = sum(self.status_dict.values())
        file_path = BASE_DIR / 'results' / f'{filename}'
        with open(file_path, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус, Количество'])
            writer.writerows(self.status_dict.items())
            writer.writerow(['Total', total])
