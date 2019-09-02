import traceback

LINE_BETWEEN_D_AND_C = 317244.69772196264
LINE_BETWEEN_C_AND_B = 12332.777453270974
LINE_BETWEN_B_AND_A = -292341.8803543614
BETWEEN_4_3 = 317874.6814641745
BETWEEN_3_2 = 13261.28348909656
BETWEEN_2_1 = -291233.1713395638


def chat_message_parse(message):
    try:
        is_ok = True
        splited_message = message.split(":")
        if " Game version" in splited_message:
            is_ok = False
        if is_ok and not splited_message == ['']:
            message_author_and_chat_type = splited_message[2]

            message_author_raw = message_author_and_chat_type.split("'")[0]
            message_author_id_starts_from = message_author_and_chat_type.split("'")[0].rfind("(")
            message_author = message_author_raw[:message_author_id_starts_from]

            message_date = splited_message[0]

            message_chat_type = message_author_and_chat_type.split("'")[2]

            message_text = splited_message[3][:-1].strip("")

            return {
                "author": message_author,
                "date": message_date,
                "chat_type": message_chat_type,
                "text": message_text
            }
    except Exception:
        print(traceback.format_exc())
        return None


def strip_all(list_member):
    return list_member.strip()


def get_kill_sector(X, Y):
    if Y >= LINE_BETWEEN_D_AND_C:
        sector_letter = "D"
    elif Y >= LINE_BETWEEN_C_AND_B:
        sector_letter = "C"
    elif Y >= LINE_BETWEN_B_AND_A:
        sector_letter = "B"
    else:
        sector_letter = "A"

    if X >= BETWEEN_4_3:
        sector_number = "4"
    elif X >= BETWEEN_3_2:
        sector_number = "3"
    elif X >= BETWEEN_2_1:
        sector_number = "2"
    else:
        sector_number = "1"
    
    return {
        "sector_letter": sector_letter,
        "sector_number": sector_number 
    }


print(get_kill_sector(-85690.73, 497131.78))


def kill_message_parse(message):
    try:
        # is_ok == True if in message haveno line with "Game Version"
        if message:
            is_ok = True
            print(f"Default Message: {message}")
            splited_message = message.split(":")
            print(f"Splited Message: {splited_message}")
            if " Game version" in splited_message:
                is_ok = False
                return None
            if is_ok: 
                date = splited_message[0]
                killed_killer_loc = splited_message[2]

                killed_raw = killed_killer_loc.split(",")[0]
                killed_id_starts_from = killed_raw.rfind("(")
                killed = killed_raw[:killed_id_starts_from].strip()

                killer_raw = splited_message[3]
                if "Weapon" in killer_raw:
                    return None
                killer_id_starts_from = killer_raw.rfind("(")
                killer = killer_raw[:killer_id_starts_from].strip()

                killer_loc_raw = splited_message[4] 
                killer_loc = killer_loc_raw.split(',')[:3]
                killer_loc = list(map(strip_all, killer_loc))    
                killer_loc_result = {
                    "x": killer_loc[0],
                    "y": killer_loc[1],
                    "z": killer_loc[2]
                }

                killed_loc_raw = splited_message[5] 
                killed_loc = killed_loc_raw.split(']')
                killed_loc = killed_loc[0].split(",")   
                killed_loc = list(map(strip_all, killed_loc))   
                killed_loc_result = {
                    "x": killed_loc[0],
                    "y": killed_loc[1],
                    "z": killed_loc[2]
                }

                is_event_kill = "(victim participating in game event)" in message

                return {
                    "date": date,
                    "killed": killed,
                    "killed_loc": killed_loc_result,
                    "killer": killer,
                    "killer_loc": killer_loc_result,
                    "is_event_kill": is_event_kill
                }
    except Exception:
        print(traceback.format_exc())
        return None
