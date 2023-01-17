import discord
import asyncio
import datetime
import os
import re
from datetime import *


# intents = discord.Intents.default()
# intents.message_content = True
client = discord.Client(intents=discord.Intents.default())

TOKEN = os.environ['DISCORD_TOKEN']
# client = discord.Client()
alarms = {}

@client.event
async def on_ready():
    print("Bot is ready.")


@client.event
async def on_message(message):
    if message.content.startswith("!alarm"):
        
        user = message.author
        alarm_time = message.content[6:]
        # cmd, alarm_time = message.content.split(" ", 1)
        print(alarm_time)
        alarm_datetime = datetime.now()
        try:
          alarm_hour,alarm_minutes = map(int,alarm_time.split(".",1))
          alarm_datetime = alarm_datetime.replace(hour=alarm_hour,minute=alarm_minutes,second = 0)
        except ValueError:
          print("failed in 2nd try loop")
          await message.channel.send(f"Alarm time is written like this 15.55 or 1.0 for 01.00")
        
       # alarm_datetime = alarm_datetime.replace(
        #    year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        user = message.author
        # if the alarm time is in the past, add one day to the alarm time
        if alarm_datetime < datetime.now():
            alarm_datetime += datetime.timedelta(days=1)
        # Create a unique identifier for the alarm
        alarm_id = f"{user.id}-{alarm_time}"
        print(alarm_id)
        print(user.id)
        print(alarm_time)
        # If the alarm already exists, cancel it
        if alarm_id in alarms:
            alarms[alarm_id].cancel()
            del alarms[alarm_id]
            await message.channel.send(f"Alarm for {alarm_datetime.strftime('%H:%M')} has been cancelled.")
        else:
            # Schedule the alarm
           alarm = asyncio.ensure_future(
                remind_user(user, alarm_datetime, alarm_id))
           alarms[alarm_id] = alarm
           await message.channel.send(f"Alarm set for {alarm_datetime.strftime('%H:%M')}. Will be delayed if playing. - bound on activity.type")
        alarm = asyncio.ensure_future(
                remind_user(user, alarm_datetime, alarm_id))
        alarms[alarm_id] = alarm


@client.event
async def on_activity_update(before, after):
    if after and before.activity.type == discord.ActivityType.playing and after.activity.type != discord.ActivityType.playing:
        user = after.user
        time = client.alarm_time
        now = datetime.now()
        if now > time:
            time += datetime.timedelta(days=1)
        time_to_sleep = (time - now).total_seconds()
        await asyncio.sleep(time_to_sleep)
        await user.send(f"{user.mention}, it's {datetime.strftime('%H:%M')}!")


async def remind_user(user, alarm_datetime, alarm_id):
    print("remind_user runs")
    print(alarms)
    await asyncio.sleep((alarm_datetime - datetime.now()).seconds)
    print("asyncio sleep is over")
    if alarm_id in alarms:
        print("if statement entered")
        await user.send(f"{user.mention}, it's {alarm_datetime.strftime('%H:%M')}, go do what u set the alarm for!")
        print(alarms[alarm_id])
        alarms[alarm_id].cancel()
        del alarms[alarm_id]
        


client.run(TOKEN)
