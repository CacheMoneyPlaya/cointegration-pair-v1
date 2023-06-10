from discord_webhook import DiscordWebhook, DiscordEmbed
import json
import time
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".config.env")
webhook_domain = config['WEBHOOK_DOMAIN']


def update_discord_channel(signals) -> None:
    for signal in signals:
        if signal['z_score_n'] > 0:
            execute_signal(signal, 'ff0000')
        else:
            execute_signal(signal, '00ff00')


def execute_signal(data, colour_scheme):
    try:
        webhook = DiscordWebhook(
            url=webhook_domain
        )

        file_name = data['a_ticker'] + '_' + data['b_ticker'] + '.png'
        file_loc = './ZScoreEvaluation/Charts/' + file_name

        with open(file_loc, "rb") as f:
            webhook.add_file(file=f.read(), filename=file_name)

        embed = build_embedded_content(data, colour_scheme, file_name)
        webhook.add_embed(embed)

        response = webhook.execute()

    except Exception as e:
        print(e)
        pass


def build_embedded_content(data, colour_scheme, file_name):
    z_score = str(data['z_score_n'])
    half_life = str(data['half_life'])
    z_zero = str(data['z_zero'])
    pair = data['a_ticker'] + 'USDT-' + data['b_ticker'] + 'USDT'
    p_value = str(data['p_value'])

    # create embed object for webhook
    embed = DiscordEmbed(title='🚨 Deviated Z-Score Alert 🚨', color=colour_scheme)
    embed.set_author(name='ZS BOT')
    embed.set_timestamp()
    embed.add_embed_field(name='PAIR', value=pair, inline=False)
    embed.add_embed_field(name='P-VALUE COEF', value=p_value + ' :white_check_mark:', inline=False)
    embed.add_embed_field(name='LATEST Z-SCORE', value=z_score, inline=False)
    embed.add_embed_field(name='HALF-LIFE (Hours)', value=half_life, inline=False)
    embed.add_embed_field(name='Pair price at mean (Z=0)', value=z_zero, inline=False)
    embed.add_embed_field(name='Time UTC', value=time.strftime("%d-%m-%Y %H:%M:%S", time.localtime()), inline=False)
    embed.set_thumbnail(url='attachment://' + file_name)

    return embed
