import asyncio
import pipes
import time


async def my_async_func(cmd, bytes_to_find):

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





cmd = "ping -c 8 8.8.8.8"
substring = "icmp_seq=3"
timeout = 5


# Python 3.7+
try:
    asyncio.run(asyncio.wait_for(my_async_func(cmd=cmd, bytes_to_find=substring.encode()), timeout))
except asyncio.TimeoutError:
    print("Timeout occured. Process already canceled.")
    # raise


# # Python 3.6+
# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(asyncio.wait_for(my_async_func(cmd=cmd, bytes_to_find=substring.encode()), timeout))
# except asyncio.TimeoutError:
#     print("Timeout occured. Process already canceled.")
#     # raise
