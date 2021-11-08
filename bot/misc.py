import utils


# def validate_msg(msg: list[str]) -> bool:
#     if len(msg) == 9:
#
#     print('Не полные данные о пользователи')
#
#
def parse_player_from_message(msg: str) -> utils.Player:
    msg_player = msg.split()
    name_player = f"{msg_player[1]} {msg_player[2]}"
    player = utils.Player(name_player, *msg_player[3:])
    player.numbers = player.numbers.split("Numbers=")[-1]

    return player
