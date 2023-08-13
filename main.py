from config import *
import discord
from discord import app_commands
from request import api

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="count", description=f"Count of Players on {DOMAIN}", guild=discord.Object(id=SERVERID))
async def count(interaction: discord.Interaction):
    total = api.count()
    embed = discord.Embed(
        title=f'<:pass:1082231929107128320>︙General information of {DOMAIN}! Server',
        description=f'- **Total players:** {total.total}\n- **Online players:** {total.online}',
        color=int(COLOR, 0)
    )

    await interaction.response.send_message(embed=embed)

@tree.command(name="pinfo", description=f"Player Info", guild=discord.Object(id=SERVERID))
async def player_info(interaction: discord.Interaction, who: str):
    try:
        pinfo = api.pinfo(who)
    except KeyError:
        await interaction.response.send_message('> ## - Player Not Found')
    embed = discord.Embed(
        title=f'Player Info',
        description=f'({pinfo.id}) {pinfo.tag} {pinfo.name} ',
        color=int(COLOR, 0)
    )
    country = str(pinfo.country).upper()
    embed.set_thumbnail(url=f'https://osu.{DOMAIN}/static/images/flags/{country}.png')
    embed.set_image(url=f'https://a.{DOMAIN}/{pinfo.id}')

    await interaction.response.send_message(embed=embed)

@tree.command(name="pstats", description=f"Player Stats", guild=discord.Object(id=SERVERID))
async def player_stats(interaction: discord.Interaction, who: str):
    try:
        pstats = api.pstats(who)
    except KeyError:
        await interaction.response.send_message('> ## - Player Not Found')
    vnstd = pstats.vn_std_json['pp']
    vntaiko = pstats.vn_taiko_json['pp']
    vncatch = pstats.vn_catch_json['pp']
    vnmania = pstats.vn_mania_json['pp']
    rxstd = pstats.rx_std_json['pp']
    rxtaiko = pstats.rx_taiko_json['pp']
    rxcatch = pstats.rx_catch_json['pp']
    apstd = pstats.ap_std_json['pp']
    embed = discord.Embed(
        title=f'Player Stats',
        description=f'- vn!std: {vnstd}pp\n- vn!taiko: {vntaiko}pp\n- vn!catch: {vncatch}pp\n- vn!mania: {vnmania}pp\n- rx!std: {rxstd}pp\n- rx!taiko: {rxtaiko}pp\n- rx!catch: {rxcatch}pp\n- ap!std: {apstd}pp',
        color=int(COLOR, 0)
    )

    await interaction.response.send_message(embed=embed)

@tree.command(name="pscores", description=f"Player Scores", guild=discord.Object(id=SERVERID))
async def player_scores(interaction: discord.Interaction, who: str, mode: int, scope: str):
    try:
        apiscores = api.pscores(who, mode, 5, scope)

        lim = 0
        scores = ''
        while lim <= 4:
            bid = apiscores.scores_list[lim]['bid']
            grade = apiscores.scores_list[lim]['grade']

            if grade == 'SSH':
                grade = RANK_SSH
            elif grade == 'SS':
                grade = RANK_SS
            elif grade == 'SH':
                grade = RANK_SH
            elif grade == 'S':
                grade = RANK_S
            elif grade == 'A':
                grade = RANK_A
            elif grade == 'B':
                grade = RANK_B
            elif grade == 'C':
                grade = RANK_C
            elif grade == 'D':
                grade = RANK_D
            elif grade == 'F':
                grade = RANK_F

            title = apiscores.scores_list[lim]['title']
            artist = apiscores.scores_list[lim]['artist']
            version = apiscores.scores_list[lim]['diff']
            stars = apiscores.scores_list[lim]['stars']
            pp = apiscores.scores_list[lim]['pp']
            mods = apiscores.scores_list[lim]['mods']
            acc = apiscores.scores_list[lim]['acc']
            combo = apiscores.scores_list[lim]['combo']
            playtime = apiscores.scores_list[lim]['playtime']
            scores += f"- **#{lim + 1}** [{artist} - {title} [{version}]](https://osu.ppy.sh/b/{bid}) [{stars}★]\n- - {grade} **{pp}pp** • {acc}% [**{combo}x**] **+{mods}** *`{playtime}`*\n"
            lim += 1
        
        embed = discord.Embed(
            title=f'{apiscores.player_name} {scope} Scores in {apiscores.gamemode}',
            description=f'{scores}',
            color=int(COLOR, 0)
        )
        embed.set_thumbnail(url=f'https://a.{DOMAIN}/{apiscores.player_id}')
        await interaction.response.send_message(embed=embed)
    except KeyError:
        await interaction.response.send_message('> ## - Player Not Found')

@tree.command(name="mostplayed", description=f"Player Scores", guild=discord.Object(id=SERVERID))
async def player_most_played(interaction: discord.Interaction, who: str, mode: int):
    try:
        mostplayed = api.pmostplayed(who, mode, 5)
        
        lim = 0
        maps = ''
        while lim <= 4:
            bid = mostplayed.map_list[lim]['bid']
            status = mostplayed.map_list[lim]['status']
            if status == '-1':
                status = 'NotSubmitted'
            elif status == '0' or status == 0:
                status = 'Pending'
            elif status == '1' or status == 1:
                status = 'UpdateAvailable'
            elif status == '2' or status == 2:
                status = 'Ranked'
            elif status == '3' or status == 3:
                status = 'Approved'
            elif status == '4' or status == 4:
                status = 'Qualified'
            elif status == '5' or status == 5:
                status = 'Loved'
            title = mostplayed.map_list[lim]['title']
            artist = mostplayed.map_list[lim]['artist']
            creator = mostplayed.map_list[lim]['creator']
            diff = mostplayed.map_list[lim]['diff']
            plays = mostplayed.map_list[lim]['plays']
            maps += f"- ({status}) (by {creator})\n- - [{title} - {artist} [{diff}]](https://osu.ppy.sh/b/{bid}) - {plays} plays\n"
            lim += 1

        embed = discord.Embed(
            title=f'Player {who} Most Played in {mostplayed.gamemode}',
            description=f'{maps}',
            color=int(COLOR, 0)
        )
        await interaction.response.send_message(embed=embed)
    except KeyError:
        await interaction.response.send_message('> ## - Player Not Found')
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=SERVERID))
    print("Ready!")

client.run(TOKEN)
