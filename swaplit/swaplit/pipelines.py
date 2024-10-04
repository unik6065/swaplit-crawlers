# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter  # This import is not used and can be removed
import swiftclient
import os
from scrapy.pipelines.images import ImagesPipeline


class SwaplitPipeline:
    def process_item(self, item, spider):
        return item

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
