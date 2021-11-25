import asyncio #Module that imitates sync working

from pywebio import start_server #Function from pywebio library
from pywebio.input import input_group, input, actions
from pywebio.output import output, put_markdown, put_scrollable, put_buttons
from pywebio.session import run_async, run_js


messages = []
users = set()

max_messages = 150


async def main():

    global messages, users
    put_markdown("Welcome to THE CHAT!") #Function from pywebio library

    msg_box = output() #"output" is a placeholder from this library
    put_scrollable(msg_box, height=250, keep_bottom=True)

    nickname = await input(
        "Enter THE CHAT",
        required=True,
        placeholder="Your nickname",
        validate=lambda n: "Fuck off! Your are not the first to use this nickname!"
        if n in users else None)
    users.add(nickname)

    messages.append((f'`{nickname}`', f': joined THE CHAT!!'))
    msg_box.append(put_markdown(f'`{nickname}` joined THE CHAT!'))

    refresh_task = run_async(refresh_msg(nickname, msg_box))

    while True:
        data = await input_group("💭 Type your message!", [
            input(placeholder="Filthy message text ...", name="msg"),
            actions(name="cmd", buttons=["Post it!", {'label': "Escape from here!", 'type': 'cancel'}])
        ], validate=lambda m: ('msg', "Filthy message text must be here...") if m["cmd"] == "Post it!" and not m['msg'] else None)

        if data is None:
            break

        msg_box.append(put_markdown(f"`{nickname}`: {data['msg']}"))
        messages.append((nickname, data['msg']))

    refresh_task.close()

    users.remove(nickname)
    msg_box.append(put_markdown(f' User `{nickname}` has left THE CHAT!'))
    messages.append((f'User {nickname}', f' has left THE CHAT!'))

    put_buttons(['Relogin'], onclick=lambda btn: run_js('window.location.reload()'))


async def refresh_msg(nickname, msg_box):

    global messages

    last_idx = len(messages)

    while True:
        await asyncio.sleep(1)

        for m in messages[last_idx:]:
            if m[0] != nickname:  # if not a message from current user
                msg_box.append(put_markdown(f'`{m[0]}`: {m[1]}'))

        # remove expired
        if len(messages) > max_messages:
            messages = messages[len(messages) // 2:]

        last_idx = len(messages)


if __name__ == "__main__":
    start_server(main, debug=True, port=8080, cdn=False) #Starts "main" on port 8080

