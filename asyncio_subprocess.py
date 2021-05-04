import asyncio
import pipes
import time


async def my_async_func(cmd:str, bytes_to_find:bytes, timeout:int):

    async def _subprocess_loop(cmd, bytes_to_find):
        print(f"Looking for {bytes_to_find} in subprocess '{cmd}'")

        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        while True:
            line = await proc.stdout.readline()
            print(line)
            if bytes_to_find in line:
                print(f"Found what we're looking for: {bytes_to_find}")
                break
        
        print("Waiting for subprocess to finish.")
        stdout, stderr = await proc.communicate()
        print("Printing the rest of the process output")
        print(stdout, stderr)

    try:
        await asyncio.wait_for(_subprocess_loop(cmd, bytes_to_find), timeout)
    except asyncio.TimeoutError:
        print("Timeout occurred. Process canceled.")


cmd = "ping -c 8 8.8.8.8"
substring = "icmp_seq=3"
timeout = 5

# Python 3.9 version
asyncio.run(my_async_func(cmd=cmd, bytes_to_find=substring.encode(), timeout=timeout))
# Python 3.6 version
# loop = asyncio.get_event_loop()
# loop.run_until_complete(my_async_func(cmd=cmd, bytes_to_find=substring.encode(), timeout=timeout))
# loop.close()