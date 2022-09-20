# ---------------------------------------------------------------------------------
# Name: promote
# Description: Promote/demote users
# Author: hikkikomoa
# Commands:
# .promote | .demote
# ---------------------------------------------------------------------------------

# -*- coding: utf-8 -*-

# meta developer: @hikkikomoa

import io
import time

from PIL import Image
from telethon.errors import (
    ChatAdminRequiredError,
    UserAdminInvalidError,
)
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
)
from telethon.tl.functions.messages import EditChatAdminRequest
from telethon.tl.types import ChatAdminRights, ChatBannedRights

from .. import loader, utils

# ================== CONSTANS ========================

DEMOTE_RIGHTS = ChatAdminRights(
    post_messages=None,
    add_admins=None,
    invite_users=None,
    change_info=None,
    ban_users=None,
    delete_messages=None,
    pin_messages=None,
    edit_messages=None,
)

# =====================================================


@loader.tds
class PromoteMod(loader.Module):
    """Promote/demote users"""

    strings = {
        "name": "Promote",
        "promote_none": "<b>🫤 No one to promote.</b>",
        "who": "<b>❓ Who is it?</b>",
        "this_isn`t_a_chat": "<b>🧐 This isn`t a chat!</b>",
        "no_rights": "<b>🫤 I don`t have rights.</b>",
        "no_args": "<b>🫤 Invalid arguments specified.</b>",
        "not_admin": "<b>🤬 I`m not an admin here.</b>",
        "promoted": "<b>🫣 {} promoted to admin rights.\n✍️ Rank: {}</b>",
        "demote_none": "<b>🤬No one to demote.</b>",
        "demoted": "<b>😂 {} demoted to admin rights. 👎</b>",
    }
    async def promotecmd(self, message):
        """Command .promote for promote user to admin rights.\nUse: .promote <@ or reply> <rank>."""
        if not message.chat:
            return await utils.answer(
                message, self.strings("this_isn`t_a_chat", message)
            )
        try:
            args = utils.get_args_raw(message).split(" ")
            reply = await message.get_reply_message()
            rank = "Admin"

            chat = await message.get_chat()
            adm_rights = chat.admin_rights
            if not adm_rights and not chat.creator:
                return await utils.answer(message, self.strings("not_admin", message))

            if reply:
                args = utils.get_args_raw(message)
                rank = args or rank
                user = await message.client.get_entity(reply.sender_id)
            else:
                user = await message.client.get_entity(
                    args[0] if not args[0].isnumeric() else int(args[0])
                )
                if len(args) == 1:
                    rank = rank
                elif len(args) >= 2:
                    rank = utils.get_args_raw(message).split(" ", 1)[1]
            try:
                await message.client(
                    EditAdminRequest(
                        message.chat_id,
                        user.id,
                        ChatAdminRights(
                            add_admins=False,
                            invite_users=adm_rights.invite_users,
                            change_info=False,
                            ban_users=False,
                            delete_messages=False,
                            pin_messages=False,
                        ),
                        rank,
                    )
                )
            except ChatAdminRequiredError:
                return await utils.answer(message, self.strings("no_rights", message))
            else:
                return await utils.answer(
                    message,
                    self.strings("promoted", message).format(user.first_name, rank),
                )
        except ValueError:
            return await utils.answer(message, self.strings("no_args", message))

    async def demotecmd(self, message):
        """Command .demote for demote user to admin rights.\nUse: .demote <@ or reply>."""
        if message.is_private:
            return await utils.answer(
                message, self.strings("this_isn`t_a_chat", message)
            )
        try:
            reply = await message.get_reply_message()

            chat = await message.get_chat()
            if not chat.admin_rights and not chat.creator:
                return await utils.answer(message, self.strings("not_admin", message))

            if reply:
                user = await message.client.get_entity(reply.sender_id)
            else:
                args = utils.get_args_raw(message)
                if not args:
                    return await utils.answer(
                        message, self.strings("demote_none", message)
                    )
                user = await message.client.get_entity(
                    args if not args.isnumeric() else int(args)
                )

            try:
                if message.is_channel:
                    await message.client(
                        EditAdminRequest(message.chat_id, user.id, DEMOTE_RIGHTS, "")
                    )
                else:
                    await message.client(
                        EditChatAdminRequest(message.chat_id, user.id, False)
                    )
            except ChatAdminRequiredError:
                return await utils.answer(message, self.strings("no_rights", message))
            else:
                return await utils.answer(
                    message, self.strings("demoted", message).format(user.first_name)
                )
        except ValueError:
            return await utils.answer(message, self.strings("no_args"))