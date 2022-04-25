from telethon.tl.functions.channels import ToggleSlowModeRequest
import schedule, time

@loader.tds
class SlowMod(loader.Module):
    """easy SlowMod."""
    strings={"name": "slowmod"}

async def slowmod(self, message):
    """turning on slowmod in chat.""" 
    args = utils.get_args_raw(message) 
    slow = client(functions.channels.ToggleSlowModeRequest(channel ='1530887128', seconds = args)) 
    
schedule.every().day.at("23:00").do(slow)
while True: 
    schedule.run_pending()
    time.sleep(1)