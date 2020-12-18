def discord_post(discord_connector, message):
    if isinstance(message, str):
        discord_connector.post(content=message)
    elif isinstance(message, dict):
        discord_connector.post(**message)
