import discord
import asyncio
import datetime
import os
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
        # time = message.content[6:] # get the time specified in the command
        # time = datetime.strptime(time, "%H:%M") # convert the time string to a datetime object
        user = message.author
        alarm_time = message.content[6:]
        # cmd, alarm_time = message.content.split(" ", 1)
        alarm_time = datetime.strptime(alarm_time, "%H:%M")
        alarm_time = alarm_time.replace(
            year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        user = message.author
        # if the alarm time is in the past, add one day to the alarm time
        if alarm_time < datetime.now():
            alarm_time += datetime.timedelta(days=1)
        # Create a unique identifier for the alarm
        alarm_id = f"{user.id}-{alarm_time}"
        # If the alarm already exists, cancel it
        if alarm_id in alarms:
            alarms[alarm_id].cancel()
            del alarms[alarm_id]
            await message.channel.send(f"Alarm for {alarm_time.strftime('%H:%M')} has been cancelled.")
        else:
            # Schedule the alarm
            alarm = asyncio.ensure_future(
                remind_user(user, alarm_time, alarm_id))
            alarms[alarm_id] = alarm
            await message.channel.send
#
        await message.channel.send(f"Alarm set for {alarm_time.strftime('%H:%M')}. Will be delayed if playing. - bound on activity.type")
        # client.alarm_time = time
        ''' check if the user is in a game 
        if user.activity and user.activity.type == discord.ActivityType.playing:
            await message.channel.send("I'll remind you when you're done playing.")
            # set the alarm_time so that the on_activity_update event can use it.
            client.alarm_time = time
        else:
            await message.channel.send("I'll remind you at the specified time.")
            await asyncio.sleep((time - datetime.now()).seconds)
            await message.channel.send(f"{user.mention}, it's {time.strftime('%H:%M')}!")
'''


@client.event
async def on_activity_update(before, after):
    if after and before.type == discord.ActivityType.playing and after.type != discord.ActivityType.playing:
        user = after.user
        time = client.alarm_time
        now = datetime.datetime.now()
        if now > time:
            time += datetime.timedelta(days=1)
        time_to_sleep = (time - now).total_seconds()
        await asyncio.sleep(time_to_sleep)
        await user.send(f"{user.mention}, it's {time.strftime('%H:%M')}!")


async def remind_user(user, time, alarm_id):
    await asyncio.sleep((time - datetime.now()).seconds)
    if alarm_id in alarms:
        await user.send(f"{user.mention}, it's {time.strftime('%H:%M')}!")
        del alarms[alarm_id]


client.run(TOKEN)
