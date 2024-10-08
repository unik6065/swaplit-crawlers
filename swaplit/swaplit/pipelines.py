# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter  # This import is not used and can be removed
import swiftclient
import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import CsvItemExporter
import swaplit.items as items


class CSVExportItemPipeline:
    def open_spider(self, spider):
        self.exporters = {}
        self.csv_file_path = spider.name.split('_')[0]

    def close_spider(self, spider):
        for exporter, csv_file in self.exporters.values():
            exporter.finish_exporting()
            csv_file.close()

    def _exporter_for_item(self, item):
        if isinstance(item, items.SwaplitItem):
            self.csv_file_path += '_books.csv'
        elif isinstance(item, items.AuthorItem):
            self.csv_file_path += '_authors.csv'
        else:
            self.csv_file_path += '_editors.csv'

        csv_file = open(self.csv_file_path, "wb")
        exporter = CsvItemExporter(csv_file)
        exporter.start_exporting()
        self.exporters[csv_file] = (exporter, csv_file)
        return self.exporters[csv_file][0]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item

class SwaplitPipeline:
    def open_spider(self, spider):
        # Se connecter à OpenStack Swift
        self.container = spider.settings.get('DATA_CONTAINER')
        self.conn = swiftclient.Connection(
            auth_version='3',  # OpenStack Identity API v3
            user=os.getenv('OS_USERNAME'),
            key=os.getenv('OS_PASSWORD'),
            authurl=os.getenv('OS_AUTH_URL'),
            os_options={
                'project_id': os.getenv('OS_PROJECT_ID'),
                'user_domain_name': os.getenv('OS_USER_DOMAIN_NAME'),
                'region_name': os.getenv('OS_REGION_NAME')
            }
        )
        self.file_name = spider.name.split('_')[0]
        files_extended = ['_books.csv', '_authors.csv', '_editors.csv']
        self.file_names = []
        for extension in files_extended:
            self.file_names.append(f"{self.file_name}{extension}")

    def process_item(self, item, spider):
        return item
    def close_spider(self, spider):
        for file in self.file_names:
            try:
                with open(file, 'rb') as csv_file:
                    self.conn.put_object(
                        self.container,
                        file,
                        contents=csv_file,
                        content_type='text/csv'
                    )
                os.remove(file)
            except:
                print('Not file called', file)
        # Retrieve the URL of the uploaded image
        self.conn.close()


class SwiftImagesPipeline(ImagesPipeline):

    def open_spider(self, spider):
        # Se connecter à OpenStack Swift
        self.spiderinfo = self.SpiderInfo(spider)
        self.conn = swiftclient.Connection(
            auth_version='3',  # OpenStack Identity API v3
            user=os.getenv('OS_USERNAME'),
            key=os.getenv('OS_PASSWORD'),
            authurl=os.getenv('OS_AUTH_URL'),
            os_options={
                'project_id': os.getenv('OS_PROJECT_ID'),
                'user_domain_name': os.getenv('OS_USER_DOMAIN_NAME'),
                'region_name': os.getenv('OS_REGION_NAME')
            }
        )
        if spider.name == 'book':
            self.container = spider.settings.get('SWIFT_CONTAINER')
        elif spider.name == 'hachette_editors':
            self.container = spider.settings.get('SWIFT_EDITOR_CONTAINER')

    def store_image(self, image_path):
        # Uploader une image dans le conteneur Swift
        with open(image_path, 'rb') as img_file:
            self.conn.put_object(
                self.container,
                os.path.basename(image_path),  # Use only the base name of the image path
                contents=img_file,
                content_type='image/jpeg'  # or another MIME type depending on the format
            )
            os.remove(image_path)
            # Retrieve the URL of the uploaded image
            image_url = self.conn.url + '/' + self.container + '/' + os.path.basename(image_path)
            return image_url


    def item_completed(self, results, item, info):
        # Appelé après que les images soient téléchargées localement
        for ok, x in results:
            if ok:
                # Une fois que l'image est téléchargée localement, on l'upload vers Swift
                image_path = "images/"+x['path']
                image_url = self.store_image(image_path)
                item['image_urls'] = [image_url]

        return item

    def close_spider(self, spider):
        # Fermer la connexion à Swift après la fin du travail
        self.conn.close()
