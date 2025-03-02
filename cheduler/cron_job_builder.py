
class CronJobBuilder:
  
  def build_cron_expression(self, interval: int, unit='minutes', days="*") -> str:
    """
    Возвращает cron-выражение для заданного интервала.
    
    :param interval: интервал (целое число)
    :param unit: 'minutes' или 'hours'
    :param days: 1-7 (задание дней недели, * - каждый день, 1-2 - пн и вт, 1-5 - будни)
    :return: строка с cron-выражением
    """
    if unit == 'minutes':
        # Если интервал меньше 60 минут – задаём выражение вида "*/N * * * *"
        if interval < 60:
            return f"*/{interval} * * * {days}"
        else:
            # Если интервал в минутах больше или равен 60, преобразуем его в часы и минуты
            hours = interval // 60
            minutes = interval % 60
            if minutes == 0:
                # Запуск каждые N часов, в начале часа
                return f"0 */{hours} * * {days}"
            else:
                # Если интервал не кратен 60, задаем более сложное выражение:
                # Это выражение означает, что задание будет запускаться в те минуты часа, которые равны "minutes",
                # и затем каждые hours часов.
                return f"*/{minutes} */{hours} * * {days}"
    elif unit == 'hours':
        return f"0 */{interval} * * *"
    else:
        raise ValueError("unit must be either 'minutes' or 'hours'")
