import argparse
import asyncio
import hashlib
import os
from uuid import uuid4
import aiohttp


def get_extension(content_type: str) -> str:
    """Определяет расширение файла по заголовку Content-Type."""
    if 'image/jpeg' in content_type:
        return '.jpg'
    elif 'image/png' in content_type:
        return '.png'
    elif 'image/gif' in content_type:
        return '.gif'
    else:
        return '.bin'


def save_file(filepath: str, data: bytes) -> None:
    """Синхронно сохраняет данные в файл."""
    with open(filepath, 'wb') as f:
        f.write(data)


async def download_file(
        session: aiohttp.ClientSession,
        url: str,
        folder_path: str,
        hashes: set,
        lock: asyncio.Lock,
        max_attempts: int = 10
) -> bool:
    """Загружает и сохраняет уникальный файл."""
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    file_hash = hashlib.sha256(data).hexdigest()

                    async with lock:
                        if file_hash in hashes:
                            print(f"Дубликат обнаружен, повторная попытка... (попытка {attempts})")
                            continue
                        hashes.add(file_hash)

                    content_type = response.headers.get('Content-Type', '')
                    extension = get_extension(content_type)
                    filename = f"{uuid4()}{extension}"
                    filepath = os.path.join(folder_path, filename)

                    await asyncio.to_thread(save_file, filepath, data)
                    print(f"Загружено: {filename}")
                    return True
                else:
                    print(f"Ошибка загрузки: статус {response.status} (попытка {attempts})")
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e} (попытка {attempts})")

    print(f"Не удалось загрузить уникальный файл после {max_attempts} попыток")
    return False


async def main():
    parser = argparse.ArgumentParser(description='Асинхронная загрузка файлов')
    parser.add_argument('-n', '--num-files', type=int, required=True, help='Количество файлов')
    parser.add_argument('-d', '--directory', type=str, required=True, help='Папка для сохранения')
    parser.add_argument('--url', type=str, default='https://thispersondoesnotexist.com/', help='URL источника')
    args = parser.parse_args()

    os.makedirs(args.directory, exist_ok=True)
    hashes = set()
    lock = asyncio.Lock()

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(
                download_file(session, args.url, args.directory, hashes, lock)
            ) for _ in range(args.num_files)
        ]
        results = await asyncio.gather(*tasks)
        successful = sum(results)

        if successful < args.num_files:
            print(f"Предупреждение: загружено только {successful} из {args.num_files} файлов")


if __name__ == '__main__':
    asyncio.run(main())