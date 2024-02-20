from aiogram.filters.callback_data import CallbackData


class CloseRecommendationKBCallback(CallbackData, prefix="close_kb"):
    ...


class NothingFindingCallback(CallbackData, prefix="nothing_happend"):
    ...