import asyncio
import discord
from discord.ext import commands

# Configure intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

# Set up the bot with the defined intents
bot = commands.Bot(command_prefix=",", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync commands with Discord
    print(f'Logged in as {bot.user}')

@bot.tree.command(name="mass_kick", description="Kick a specified number of members")
async def mass_kick(interaction: discord.Interaction, number: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need to be an administrator to use this command.")
        return

    # Send the initial confirmation message
    await interaction.response.send_message(
        f"Do you really want to kick {number} members? React with 👍 to confirm or 👎 to cancel."
    )
    message = await interaction.original_response()
    await message.add_reaction("👍")
    await message.add_reaction("👎")

    def check(reaction, user):
        return user == interaction.user and reaction.message.id == message.id and reaction.emoji in ["👍", "👎"]

    try:
        reaction, _ = await bot.wait_for("reaction_add", check=check, timeout=60.0)

        if reaction.emoji == "👍":
            # Start the mass kick process
            await interaction.followup.send("Starting the mass kick...")

            members = interaction.guild.members
            kicked = 0

            for member in members:
                if not member.bot and kicked < number:
                    try:
                        await member.kick(reason="Mass kick")
                        kicked += 1
                    except discord.Forbidden:
                        print(f"Cannot kick {member.name}, missing permissions.")
                        continue
                    except discord.HTTPException as e:
                        print(f"HTTP Exception occurred: {e}")
                        break

                if kicked >= number:
                    break

            await interaction.followup.send(f"Finished kicking. Total members kicked: {kicked}")
        else:
            await interaction.followup.send("Mass kick canceled.")
    except asyncio.TimeoutError:
        await interaction.followup.send("No response received. Mass kick canceled.")

bot.run('MTI3ODUwMDg3NjMzNTcxMDI3MQ.G1yjLE.89_09B1Quc3yEGCsBvpJFpDCiAWh7jmKsmwAbQ')  # Replace 'YOUR_BOT_TOKEN' with your actual bot token
