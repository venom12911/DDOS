import asyncio
import logging

async def run_attack(ip, port, duration):
    """ Executes the navin binary asynchronously with logging """
    try:
        logging.info(f"Starting attack on {ip}:{port} for {duration}s")
        process = await asyncio.create_subprocess_shell(
            f"./soul {ip} {port} {duration} 10",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"✅ *Output:*\n```\n{stdout.decode()}\n```")
        if stderr:
            print(chat_id=chat_id, text=f"⚠️ *Error:*\n```\n{stderr.decode()}\n```")

    except Exception as e:
        print(f"❌ *Error:* {str(e)}")

asyncio.run(run_attack(ip="1.1.1.1", port="1111", duration=10))
