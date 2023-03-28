from os.path import isfile

from aiofiles import open as aopen

if not isfile("count"):
    with open("count", "w") as count_file:
        count_file.write("1")

async def get_count():
    async with aopen("count", "r+") as count_file:
        content = await count_file.read()
        result = int(content.strip())
        await count_file.seek(0)
        await count_file.write(str(result + 1))
    return result

def get_count_nowait():
    with open("count", "r+") as count_file:
        content = count_file.read()
        result = int(content.strip())
        count_file.seek(0)
        count_file.write(str(result + 1))
    return result
