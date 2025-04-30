#!/usr/bin/env python3

import json
import os
import sys
import argparse
import asyncio
import aiohttp
import aiofiles
from pathlib import Path
from tqdm import tqdm

async def download_image(session, url, output_path):
    """
    Asynchronously download an image from the given URL and save it.
    
    Args:
        session (aiohttp.ClientSession): The aiohttp session to use for requests.
        url (str): The URL of the image to download.
        output_path (Path): The path where the image should be saved.
    
    Returns:
        bool: True if download was successful, False otherwise.
    """
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return False
            
            # Make sure the directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the image content to file
            async with aiofiles.open(output_path, 'wb') as f:
                while True:
                    chunk = await response.content.read(8192)
                    if not chunk:
                        break
                    await f.write(chunk)
            
            return True
    except Exception:
        return False

def extract_file_id_from_drive_link(link):
    """
    Extract the file ID from a Google Drive link.
    
    Args:
        link (str): The Google Drive link.
    
    Returns:
        str: The file ID.
    """
    parts = link.split('/')
    for i, part in enumerate(parts):
        if part == 'd':
            return parts[i+1]
    return None

def get_direct_download_link(file_id):
    """
    Get the direct download link for a Google Drive file.
    
    Args:
        file_id (str): The Google Drive file ID.
    
    Returns:
        str: The direct download link.
    """
    return f"https://drive.google.com/uc?export=download&id={file_id}"

async def download_all_images(data, output_folder, max_images, max_concurrent=20):
    """
    Download all images concurrently with a limit on simultaneous downloads.
    
    Args:
        data (list): The JSON data with image information.
        output_folder (Path): The folder where images will be saved.
        max_images (int): Maximum number of images to download.
        max_concurrent (int): Maximum number of concurrent downloads.
    
    Returns:
        tuple: (successful_count, failed_count, updated_data)
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    connector = aiohttp.TCPConnector(limit=max_concurrent)
    
    updated_data = []
    async with aiohttp.ClientSession(connector=connector) as session:
        images_to_process = []
        
        # Prepare the download tasks
        for idx, item in enumerate(data):
            if idx >= max_images:
                break
                
            image_filename = item.get('link')
            if not image_filename:
                continue
            
            drive_link = item.get('online_link')
            if not drive_link:
                continue
            
            file_id = extract_file_id_from_drive_link(drive_link)
            if not file_id:
                continue
            
            download_url = get_direct_download_link(file_id)
            output_path = (output_folder / image_filename).resolve()  # Changed to use resolve()
            
            # Create a copy of the item to modify
            new_item = item.copy()
            new_item['local_path'] = str(output_path)  # Now contains absolute path
            updated_data.append(new_item)
            
            images_to_process.append((download_url, output_path))
        
        total_downloads = len(images_to_process)
        if total_downloads == 0:
            return 0, 0, updated_data
        
        # Download with progress bar
        with tqdm(total=total_downloads, desc="Downloading images") as pbar:
            async def download_with_semaphore(url, path):
                async with semaphore:
                    success = await download_image(session, url, path)
                    pbar.update(1)
                    return success
            
            tasks = [
                asyncio.create_task(download_with_semaphore(url, path)) 
                for url, path in images_to_process
            ]
            
            results = await asyncio.gather(*tasks)
            
            successful = sum(1 for r in results if r)
            failed = sum(1 for r in results if not r)
            
        return successful, failed, updated_data

async def main_async():
    parser = argparse.ArgumentParser(description='Download images from a JSON file asynchronously.')
    parser.add_argument('--json_file', required=True, default='./questions.json', help='Path to the JSON file containing image information.')
    parser.add_argument('--output_folder', required=True, default='./images', help='Path to the folder where images will be saved.')
    parser.add_argument('--max-images', type=int, default=500, help='Maximum number of images to download (optional)')
    parser.add_argument('--max-concurrent', type=int, default=20, 
                       help='Maximum number of concurrent downloads (default: 20)')
    
    args = parser.parse_args()
    
    output_folder = Path(args.output_folder).resolve()  # Ensure output folder is absolute
    output_folder.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(args.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)
    
    print(f"Found {len(data)} items in the JSON file.")
    max_images = len(data) if args.max_images is None else min(args.max_images, len(data))
    print(f"Preparing to download up to {max_images} images...")
    
    successful, failed, updated_data = await download_all_images(
        data, 
        output_folder, 
        max_images, 
        max_concurrent=args.max_concurrent
    )
    
    # Save the updated JSON with local_path information
    json_path = Path(args.json_file)
    new_json_path = json_path.parent / f"{json_path.stem}_processed{json_path.suffix}"
    
    try:
        with open(new_json_path, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, indent=2, ensure_ascii=False)
        print(f"\nSaved updated JSON with local paths to: {new_json_path}")
    except Exception as e:
        print(f"\nError saving updated JSON: {e}")
    
    print("\nDownload summary:")
    print(f"Successfully downloaded: {successful} images")
    print(f"Failed to download: {failed} images")

def main():
    if sys.platform.startswith('win') and hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main_async())

if __name__ == "__main__":
    main()