import os
from aiogram import F, Router, types

from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from api.filters.chat_types import IsAdmin

admin_router = Router()
admin_router.message.filter(IsAdmin())


