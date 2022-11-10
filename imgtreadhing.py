import threading
import time
import requests

img_urls = ['https://cdn.pixabay.com/photo/2022/10/31/18/44/spider-web-7560535_960_720.jpg']

def download_image(img_url):
    img_bytes = requests.get(img_url).content
    img_name = img_url.split('/')[9]
    with open(img_name, 'wb') as img_file:
        img_file.write(img_bytes)
        print(f"{img_name} was downloaded")

if __name__ == '__main__':
    start = time.perf_counter()

    t1 = threading.Thread(target=download_image, args=[img_urls[0]])
    t1.start()
    t1.join()

    end = time.perf_counter()
    print(f"Tasks ended in {round(end - start, 2)} second(s)")