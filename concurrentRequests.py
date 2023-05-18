import base64
import concurrent.futures
import time

import requests

with open(f"test_data/mzx-1.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")


def make_request(url):
    response = requests.post(
        url,
        json={'image_base64_data': image_base64},
    )
    return response.status_code


def main():
    api_url = "http://127.0.0.1:8000/detectBase64"
    num_requests = 100  # Number of requests to send
    max_workers = 300  # Maximum number of concurrent workers
    print(f"Sending {num_requests} requests to {api_url}...")
    start_time = time.time()
    print(f"Using {max_workers} workers...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create a list of URLs to send requests to
        urls = [api_url] * num_requests

        # Submit tasks to the executor
        futures = [executor.submit(make_request, url) for url in urls]
        print(f"Submitted {len(futures)} requests...")

        # Wait for all futures to complete
        concurrent.futures.wait(futures)
    print("All requests complete!")
    end_time = time.time()
    elapsed_time = end_time - start_time

    total_requests = len(futures)
    successful_requests = sum(future.result() == 200 for future in futures)
    failed_requests = total_requests - successful_requests

    requests_per_second = total_requests / elapsed_time

    print(f"Elapsed Time: {elapsed_time} seconds")
    print(f"Total Requests: {total_requests}")
    print(f"Successful Requests: {successful_requests}")
    print(f"Failed Requests: {failed_requests}")
    print(f"Requests per Second: {requests_per_second}")


if __name__ == '__main__':
    main()
