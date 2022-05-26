import time, re

from telegram.ext import CommandHandler

from bot import LOGGER, dispatcher, telegraph
from telegraph.exceptions import RetryAfterError, TelegraphException
from bot.helper.drive_utils.gdriveTools import GoogleDriveHelper
from bot.helper.ext_utils.bot_utils import new_thread, is_gdrive_link, is_appdrive_link, is_gdtot_link, is_gplink_link, is_bitly_link, is_linkvertise_link, is_hubdrive_link
from bot.helper.ext_utils.clone_status import CloneStatus
from bot.helper.ext_utils.exceptions import DDLException
from bot.helper.ext_utils.parser import appdrive, gdtot, gplinks, linkvertise, hubdrive
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage, deleteMessage, sendMessageWithPreview
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters

@new_thread
def byPass(update, context):
    LOGGER.info('User: {} [{}]'.format(update.message.from_user.first_name, update.message.from_user.id))
    args = update.message.text.split(" ", maxsplit=1)
    reply_to = update.message.reply_to_message
    txt = ''
    if len(args) > 1:
        txt = args[1]
        links = re.findall(r'\bhttps?://.\S+', txt)

        '''if len(links) == 1:
            #if reply_to is not None:
                #if len(link) == 0:
                    #link = reply_to.text
            link = links[0]
            is_appdrive = is_appdrive_link(link)
            is_gdtot = is_gdtot_link(link)
            is_bitly = is_bitly_link(link)
            is_linkvertise = is_linkvertise_link(link)
            is_hubdrive = is_hubdrive_link(link)

            if (is_appdrive or is_gdtot or is_hubdrive):
                try:
                    msg = sendMessage(f"⫸ <b>Processing:</b> <code>{link}</code>", context.bot, update)
                    LOGGER.info(f"Processing: {link}")
                    if is_appdrive:
                        link = appdrive(link)
                    if is_gdtot:
                        link = gdtot(link)
                    if is_hubdrive:
                        link = hubdrive(link)
                    deleteMessage(context.bot, msg)
                except DDLException as e:
                    deleteMessage(context.bot, msg)
                    LOGGER.error(e)
                    e = f"⫸ <b>{str(e)}</b>"
                    return sendMessage(e, context.bot, update)

            if is_gdrive_link(link):
                msg = sendMessage(f"⫸ <b>Cloning:</b> <code>{link}</code>", context.bot, update)
                LOGGER.info(f"Cloning: {link}")
                status_class = CloneStatus()
                gd = GoogleDriveHelper()
                sendCloneStatus(link, msg, status_class, update, context)
                result = gd.clone(link, status_class)
                deleteMessage(context.bot, msg)
                status_class.set_status(True)

                if update.message.from_user.username:
                    uname = f'@{update.message.from_user.username}'
                else:
                    uname = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
                if uname is not None:
                    cc = f'\n\n<b>cc: </b>{uname}'

                sendMessage(result + cc, context.bot, update)
                if is_gdtot:
                    LOGGER.info(f"Deleting: {link}")
                    gd.deleteFile(link)
                if is_appdrive:
                    LOGGER.info(f"Deleting: {link}")
                    gd.deleteFile(link)
                if is_hubdrive:
                    LOGGER.info(f"Deleting: {link}")
                    gd.deleteFile(link)

            elif is_gplink_link(link):
                try:
                    reply = sendMessage(f"<b>⫸ Bypassing:</b> <code>{link}</code>", context.bot, update)
                    LOGGER.info(f"Bypassing: {link}")
                    parsed_link = gplinks(link)
                    if update.message.from_user.username:
                        uname = f'@{update.message.from_user.username}'
                    else:
                        uname = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
                    if uname is not None:
                        cc = f'\n\n<b>cc: </b>{uname}'
                    time.sleep(2)
                    deleteMessage(context.bot, reply)
                    res = f"<b>⫸ Source URL</b> : {link}\n\n<b>⫸ Bypassed URL</b> : {parsed_link}{cc}"
                    sendMessage(res, context.bot, update)

                except DDLException as e:
                    deleteMessage(context.bot, reply)
                    LOGGER.error(e)
                    e = f"⫸ <b>{str(e)}</b>"
                    return sendMessage(e, context.bot, update)

            elif (is_linkvertise or is_bitly):
                try:
                    reply = sendMessage(f"<b>⫸ Bypassing:</b> <code>{link}</code>", context.bot, update)
                    LOGGER.info(f"Bypassing: {link}")
                    parsed_link = linkvertise(link)

                    if update.message.from_user.username:
                        uname = f'@{update.message.from_user.username}'
                    else:
                        uname = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
                    if uname is not None:
                        cc = f'\n\n<b>cc: </b>{uname}'
                    time.sleep(2)
                    deleteMessage(context.bot, reply)
                    res = f"<b>⫸ Source URL</b> : {link}\n\n<b>⫸ Bypassed URL</b> : {parsed_link}{cc}"
                    sendMessage(res, context.bot, update)
                    
                except DDLException as e:
                    deleteMessage(context.bot, reply)
                    LOGGER.error(e)
                    e = f"⫸ <b>{str(e)}</b>"
                    return sendMessage(e, context.bot, update)

            else:
                sendMessage("⫸ <b>Unsupported link!!!</b>\n\n<i>Supported Link:</i>\nAppDrive, DriveApp, GDTOT, GPLinks, BitLy, Linkvertise (Unstable)", context.bot, update)
                LOGGER.info("Bypassing: None [Cause Nothing Found (Single Link)]")'''

        if len(links) <= 5:
            parsed_count = 0
            error_count = 0
            errors = ""
            output = ""
            total = len(links)
            if len(links) == 1:
                reply = sendMessage('⫸ <b>Bypassing Link...Please Wait!</b>', context.bot, update)
            else:
                reply = sendMessage('⫸ <b>Bypassing Multiple Links...Please Wait!</b>', context.bot, update)
            for link in links:
                is_appdrive = is_appdrive_link(link)
                is_gdtot = is_gdtot_link(link)
                is_bitly = is_bitly_link(link)
                is_linkvertise = is_linkvertise_link(link)
                is_hubdrive = is_hubdrive_link(link)
                is_gplink = is_gplink_link(link)
                is_gdrive = is_gdrive_link(link)

                if (is_appdrive or is_gdtot or is_hubdrive):
                    try:
                        if is_appdrive:
                            link = appdrive(link)
                        if is_gdtot:
                            link = gdtot(link)
                        if is_hubdrive:
                            link = hubdrive(link)
                    except DDLException as e:
                        errors += link + "\n" + str(e) + "\n\n"
                        error_count += 1

                if is_gdrive_link(link):
                    gd = GoogleDriveHelper()
                    result, drive_link, index_link = gd.cloneForMultiple(link)
                    output += result + f'\n<a href="{drive_link}">Drive URL</a>' +  f'  |  <a href="{index_link}">Index URL</a>\n\n'
                    parsed_count += 1
                    if is_gdtot:
                        LOGGER.info(f"Deleting: {link}")
                        gd.deleteFile(link)
                    if is_appdrive:        
                        LOGGER.info(f"Deleting: {link}")
                        gd.deleteFile(link)
                    if is_hubdrive:
                        LOGGER.info(f"Deleting: {link}")
                        gd.deleteFile(link)
                        
                if is_gplink:
                    try:
                        parsed_link = gplinks(link)
                        title = f"➤ <code>GPLink Bypass</code>"
                        output += title + f'\n<a href="{link}">Source URL</a>' +  f'  |  <a href="{parsed_link}">Bypassed URL</a>\n\n'
                        parsed_count += 1

                    except DDLException as e:
                        errors += link + "\n" + str(e) + "\n\n"
                        error_count += 1

                if (is_linkvertise or is_bitly):
                    try:
                        parsed_link = linkvertise(link)
                        if 'bit.ly' in link:
                            title = f"➤ <code>Bitly Bypass</code>"
                        else:
                            title = f"➤ <code>Linkvertise Bypass</code>"
                        output += title + f'\n<a href="{link}">Source URL</a>' +  f'  |  <a href="{parsed_link}">Bypassed URL</a>\n\n'
                        parsed_count += 1

                    except DDLException as e:
                        errors += link + "\n" + str(e) + "\n\n"
                        error_count += 1

                if len(links) > 1 and (is_gdtot or is_appdrive or is_hubdrive or is_gdrive or is_gplink or is_linkvertise or is_bitly):
                    editMessage(f'⫸ <b>Bypassing Multiple Links...Please Wait!\n\nTotal Links Parsed : {parsed_count}/{total}\nErrors Found : {error_count}</b>', reply)

            if (is_gdtot or is_appdrive or is_hubdrive or is_gdrive or is_gplink or is_linkvertise or is_bitly):
                try:
                    msg = f"{output}"
                    if errors != "":
                        msg += f"\n\n<b>{error_count} Error(s) Occured While Bypassing</b>\n{errors}"
                    if update.message.from_user.username:
                      uname = f'@{update.message.from_user.username}'
                    else:
                      uname = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
                    if uname is not None:
                        cc = f'<b>cc: </b>{uname}'
                    deleteMessage(context.bot, reply)
                    sendMessage(msg + cc, context.bot, update)
                except Exception as e:
                    deleteMessage(context.bot, reply)
                    sendMessage(f"⫸ <b>Error Occured!!!</b>\n{e}", context.bot, update)
                    LOGGER.info(f"Error Occured: {e}")
            else:
                deleteMessage(context.bot, reply)
                sendMessage("⫸ <b>Unsupported link(s)!!!</b>\n\n<i>Supported Link:</i>\nAppDrive, DriveApp, GDTOT, GPLinks, BitLy, Linkvertise (Unstable)", context.bot, update)
                LOGGER.info("Bypassing: None [Cause Nothing Found] (Multiple Links)")

        elif len(links) > 5:
            parsed_count = 0
            error_count = 0
            errors = ""
            output = ""
            total = len(links)
            reply = sendMessage('⫸ <b>Bypassing Multiple Links...Please Wait!</b>', context.bot, update)
            for link in links:
                is_appdrive = is_appdrive_link(link)
                is_gdtot = is_gdtot_link(link)
                is_bitly = is_bitly_link(link)
                is_linkvertise = is_linkvertise_link(link)
                is_hubdrive = is_hubdrive_link(link)
                is_gplink = is_gplink_link(link)
                is_gdrive = is_gdrive_link(link)

                if (is_appdrive or is_gdtot or is_hubdrive):
                    try:
                        if is_appdrive:
                            link = appdrive(link)
                        if is_gdtot:
                            link = gdtot(link)
                        if is_hubdrive:
                            link = hubdrive(link)
                    except DDLException as e:
                        errors += link + "\n" + str(e) + "\n\n"
                        error_count += 1

                if is_gdrive_link(link):
                    gd = GoogleDriveHelper()
                    result, drive_link, index_link = gd.cloneForMultiple(link)
                    output += result + f'<br><a href="{drive_link}">Drive URL</a>' +  f'  |  <a href="{index_link}">Index URL</a><br><br>'
                    parsed_count += 1
                    if is_gdtot:
                        LOGGER.info(f"Deleting: {link}")
                        gd.deleteFile(link)
                    if is_appdrive:        
                        LOGGER.info(f"Deleting: {link}")
                        gd.deleteFile(link)
                    if is_hubdrive:
                        LOGGER.info(f"Deleting: {link}")
                        gd.deleteFile(link)
                        
                if is_gplink:
                    try:
                        parsed_link = gplinks(link)
                        title = f"➤ <code>GPLink Bypass</code>"
                        output += title + f'<br><a href="{link}">Source URL</a>' +  f'  |  <a href="{parsed_link}">Bypassed URL</a><br><br>'
                        parsed_count += 1

                    except DDLException as e:
                        errors += link + "\n" + str(e) + "\n\n"
                        error_count += 1

                if (is_linkvertise or is_bitly):
                    try:
                        parsed_link = linkvertise(link)
                        if 'bit.ly' in link:
                            title = f"➤ <code>Bitly Bypass</code>"
                        else:
                            title = f"➤ <code>Linkvertise Bypass</code>"
                        output += title + f'<br><a href="{link}">Source URL</a>' +  f'  |  <a href="{parsed_link}">Bypassed URL</a><br><br>'
                        parsed_count += 1

                    except DDLException as e:
                        errors += link + "\n" + str(e) + "\n\n"
                        error_count += 1
                        
                editMessage(f'⫸ <b>Bypassing Multiple Links...Please Wait!\n\nTotal Links Parsed : {parsed_count}/{total}\nErrors Found : {error_count}</b>', reply)
            if (is_gdtot or is_appdrive or is_hubdrive or is_gdrive or is_gplink or is_linkvertise or is_bitly):
                try:
                    if error_count > 3 and error_count <= 10:
                        errors = errors.replace("\n", "<br>")
                        error_outputs = telegraph[0].create_page(
                            title='Errors While Parsing',
                            author_name='Max Parker',
                            author_url='https://t.me/max_parker',
                            html_content=errors,
                        )["path"]
                        errors = f'https://telegra.ph/{error_outputs}'
                    
                    try:
                        links_outputs = telegraph[1].create_page(
                            title='Bypassed Links',
                            author_name='Max Parker',
                            author_url='https://t.me/max_parker',
                            html_content=output,
                        )["path"]
                        links_outputs = f'https://telegra.ph/{links_outputs}'

                    except TelegraphException:
                        links_outputs = ''

                    msg = f"⫸ <b>{parsed_count} Links Bypassed</b>\n{links_outputs}"
                    if errors != "":
                        msg += f"\n\n<b>{error_count} Errors Occured While Bypassing</b>\n\n" + errors
                    if error_count == total:
                        msg = f"⫸ <b>Error Occured in All of the Links!</b>"
                        if error_count > 10:
                            LOGGER.info(f"Errors: {errors}")
                            msg += f"\nCan't show the errors in telegraph due to flood limit. Check logs!"
                        else:
                            msg += f"\n\n{errors}"
                    if update.message.from_user.username:
                      uname = f'@{update.message.from_user.username}'
                    else:
                      uname = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
                    if uname is not None:
                        if error_count > 1 and error_count < 3:
                            cc = f'<b>cc: </b>{uname}'
                        else:
                            cc = f'\n\n<b>cc: </b>{uname}'
                    deleteMessage(context.bot, reply)
                    sendMessageWithPreview(msg + cc, context.bot, update)
                except Exception as e:
                    deleteMessage(context.bot, reply)
                    sendMessage(f"⫸ <b>Error Occured!!!</b>\n{e}", context.bot, update)
                    LOGGER.info(f"Error Occured: {e}")
            else:
                deleteMessage(context.bot, reply)
                sendMessage("⫸ <b>Unsupported link(s)!!!</b>\n\n<i>Supported Link:</i>\nAppDrive, DriveApp, GDTOT, GPLinks, BitLy, Linkvertise (Unstable)", context.bot, update)
                LOGGER.info("Bypassing: None [Cause Nothing Found] (Multiple Links)")

    else:
        sendMessage("⫸ <b>Send AppDrive / DriveApp / GDTOT / GPlinks / BitLy link along with command</b>", context.bot, update)
        LOGGER.info("Bypassing: None")


@new_thread
def sendCloneStatus(link, msg, status, update, context):
    old_statmsg = ''
    while not status.done():
        time.sleep(3)
        try:
            statmsg = f"⫸ <b>Cloning:</b> <a href='{status.source_folder_link}'>{status.source_folder_name}</a>\n━━━━━━━━━━━━━━" \
                      f"\n<b>Current file:</b> <code>{status.get_name()}</code>\n\n<b>Transferred</b>: <code>{status.get_size()}</code>"
            if not statmsg == old_statmsg:
                editMessage(statmsg, msg)
                old_statmsg = statmsg
        except Exception as e:
            if str(e) == "Message to edit not found":
                break
            time.sleep(2)
            continue
    return

clone_handler = CommandHandler(BotCommands.BypassCommand, byPass,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(clone_handler)
