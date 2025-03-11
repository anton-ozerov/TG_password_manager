from typing import Callable, Awaitable, Dict, Any, List

from aiogram import BaseMiddleware
from aiogram import Bot
from aiogram.types import Message, TelegramObject


class RemoveReplyMarkupMiddleware(BaseMiddleware):
    """Удаление inline кнопок у старых Message'ей. Например, пользователь 2 раза нажал /start"""
    def __init__(self):
        self.last_bot_messages: Dict[int, List[int]] = {}  # Хранение последних сообщений {user_id: message_id}

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        bot: Bot = data["bot"]

        if event.message:  # Если пользователь отправляет Message
            user_id = event.message.from_user.id

            # Удаляем клавиатуру у предыдущих сообщений, если они есть
            if user_id in self.last_bot_messages:
                for message_id in self.last_bot_messages[user_id]:
                    try:
                        await bot.edit_message_reply_markup(
                            chat_id=user_id,
                            message_id=message_id,
                            reply_markup=None
                        )
                    except Exception as e:
                        print(e)

            self.last_bot_messages[user_id] = []  # очищаем список еще до result

            # Сохраняем ID нового сообщения
            result = await handler(event, data)
            try:
                self.last_bot_messages[result.chat.id].append(result.message_id)
            except AttributeError:  # когда UNHANDLED
                pass

            return result
        return await handler(event, data)
