import instaloader
import os
import json
import argparse

class InstagramCrawler:
    def __init__(self, username, output_root="downloads"):
        self.username = username
        self.output_root = output_root

        # Configure Instaloader
        self.loader = instaloader.Instaloader(
            download_pictures=True,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=True,
            compress_json=False
        )

    def download_posts(self, count=None):
        print(f"Downloading posts for {self.username}...")

        # Define the target directory where files will be saved
        target_dir = os.path.join(self.output_root, self.username)

        try:
            profile = instaloader.Profile.from_username(self.loader.context, self.username)

            posts = profile.get_posts()

            downloaded_count = 0
            for post in posts:
                if count and downloaded_count >= count:
                    break

                print(f"Downloading post {post.shortcode}...")

                # download_post saves to the directory specified by 'target'
                # If target contains path separators, it is treated as a path.
                success = self.loader.download_post(post, target=target_dir)
                if success:
                    downloaded_count += 1

        except instaloader.ProfileNotExistsException:
            print(f"Profile {self.username} does not exist.")
        except instaloader.LoginRequiredException:
            print(f"Login required to access profile {self.username}.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def generate_index(self):
        """
        Scans the download directory and creates a consolidated index.json
        """
        target_dir = os.path.join(self.output_root, self.username)

        if not os.path.isdir(target_dir):
            print(f"Directory {target_dir} not found. Nothing to index.")
            return

        print(f"Generating index from {target_dir}...")

        structured_data = []
        files = sorted(os.listdir(target_dir))

        # Find JSON metadata files
        json_files = [f for f in files if f.endswith('.json')]

        for jf in json_files:
            file_path = os.path.join(target_dir, jf)

            # Skip if it's the index itself (if stored there) or invalid
            if jf == "index.json":
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Skipping broken json {jf}")
                    continue

                # Instaloader JSON structure usually has a 'node' key or is flat
                node = data.get('node', data)

                # Look for the image file corresponding to this JSON
                # Filename format: YYYY-MM-DD_HH-MM-SS_UTC.json
                base_name = os.path.splitext(jf)[0]

                image_path = None
                # Check for standard image extensions
                for ext in ['.jpg', '.png']:
                    img_name = base_name + ext
                    if img_name in files:
                        image_path = os.path.join(target_dir, img_name)
                        break

                # If not found, check for sidecar first image (_1.jpg)
                if not image_path:
                     img_name = base_name + "_1.jpg"
                     if img_name in files:
                         image_path = os.path.join(target_dir, img_name)

                if image_path:
                    # Extract caption
                    caption = ""
                    edge_media_to_caption = node.get("edge_media_to_caption", {})
                    edges = edge_media_to_caption.get("edges", [])
                    if edges:
                        caption = edges[0].get("node", {}).get("text", "")

                    post_data = {
                        "shortcode": node.get("shortcode"),
                        "timestamp": node.get("taken_at_timestamp"),
                        "date_str": base_name.split('_UTC')[0] if '_UTC' in base_name else "",
                        "caption": caption,
                        "image_path": image_path
                    }
                    structured_data.append(post_data)

        # Save index in the root or in the target dir?
        # User asked for pre-defined structure to reuse.
        # Let's save 'index.json' in the downloads directory for that user.
        index_path = os.path.join(target_dir, "index.json")
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(structured_data, f, indent=4, ensure_ascii=False)

        print(f"Created {index_path} with {len(structured_data)} posts.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instagram Crawler")
    parser.add_argument("username", help="Instagram username to crawl")
    parser.add_argument("--count", type=int, default=10, help="Max posts to download")
    parser.add_argument("--output", default="downloads", help="Output directory root")

    args = parser.parse_args()

    crawler = InstagramCrawler(args.username, output_root=args.output)
    crawler.download_posts(count=args.count)
    crawler.generate_index()
