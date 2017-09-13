type('',(__import__('discord').Client,),{'handle_message':lambda s,m:s.loop.create_task([...,m.channel.send('Pong!')]['!ping'in m.content])})().run(__import__('os').environ["TOKEN"])
