import unittest
import os
import json
import shutil
from src.crawler import InstagramCrawler

class TestInstagramCrawler(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_downloads"
        self.username = "test_user"
        self.crawler = InstagramCrawler(self.username, output_root=self.test_dir)

        # Create dummy data
        target_dir = os.path.join(self.test_dir, self.username)
        os.makedirs(target_dir, exist_ok=True)

        self.dummy_shortcode = "TEST12345"
        self.dummy_timestamp = 1600000000
        self.dummy_caption = "This is a test caption"

        self.base_name = "2020-09-13_12-26-40_UTC"

        # Create JSON metadata
        with open(os.path.join(target_dir, self.base_name + ".json"), "w") as f:
            json.dump({
                "node": {
                    "shortcode": self.dummy_shortcode,
                    "taken_at_timestamp": self.dummy_timestamp,
                    "edge_media_to_caption": {
                        "edges": [{"node": {"text": self.dummy_caption}}]
                    }
                }
            }, f)

        # Create Dummy Image
        with open(os.path.join(target_dir, self.base_name + ".jpg"), "w") as f:
            f.write("image data")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_generate_index(self):
        self.crawler.generate_index()

        index_path = os.path.join(self.test_dir, self.username, "index.json")
        self.assertTrue(os.path.exists(index_path))

        with open(index_path, "r") as f:
            data = json.load(f)

        self.assertEqual(len(data), 1)
        item = data[0]
        self.assertEqual(item["shortcode"], self.dummy_shortcode)
        self.assertEqual(item["caption"], self.dummy_caption)
        self.assertTrue(item["image_path"].endswith(".jpg"))

if __name__ == "__main__":
    unittest.main()
