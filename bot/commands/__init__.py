__all__ = ['start']

from aiogram import Router, F
from aiogram.filters import Command

from .add_user import add_user_start, add_user_name, AddUserState, add_user_role, finish, update_user_name
from .set_user_active import set_active_command, set_active_function, SetUserActive
from .set_user_inactive import SetUserInactive, set_inactive_function, set_inactive_command
from .start import start
from bot.middlewares.check_user import UserCheck
from .tag_user import tag_user


def register_commands(router: Router) -> None:
    router.message.register(start, Command(commands=['start']))
    router.callback_query.register(add_user_start, F.data == 'function:addUser')
    router.message.register(add_user_name, AddUserState.user_name)
    router.message.register(update_user_name, AddUserState.update_name)
    router.message.register(set_active_command, Command(commands=['inactive']))
    router.message.register(set_inactive_command, Command(commands=['active']))
    router.callback_query.register(add_user_role, F.data.startswith('role:'), AddUserState.role)
    router.callback_query.register(set_active_function, F.data.startswith('set_active:'), SetUserActive.set_active)
    router.callback_query.register(set_inactive_function, F.data.startswith('set_inactive:'), SetUserInactive.set_inactive)
    router.callback_query.register(finish, F.data.startswith('update:'), AddUserState.finish)
    router.message.register(tag_user, Command(commands=['tag']))