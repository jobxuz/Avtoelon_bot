from .commands import router as commands_router
#from .registration import router as registration
from .user_update import router as user
from .mainmenu import router as menu



def setup_handlers(dp):
    dp.include_router(commands_router)
    dp.include_router(user)
    dp.include_router(menu)

    # dp.include_router(registration)




