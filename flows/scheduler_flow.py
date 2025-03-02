
from datetime import datetime, timedelta
import telebot

from bot_commands import BotCommands
from cheduler.cron_job_builder import CronJobBuilder
from cheduler.fast_cron import FastCron
from make_integration import make
from make_integration.data import Data, SchedulerData


class SchedulerFlow:

    bot: telebot = None
    cron: FastCron = None

    def __init__(self, bot: telebot, cron: FastCron, data: Data, callback_url: str, commands: BotCommands):
        self.cron = cron
        self.bot = bot
        self.data = data
        self.callback_url = callback_url
        self.commands = commands

    def setup_flow(self, call, chat_id: int, schedule_data: SchedulerData):
        if call.data == "set_time":
            self.__send_setup_time_message(call, chat_id, schedule_data)
        elif call.data == "set_interval":
            self.__send_setup_interval_message(call, chat_id, schedule_data)
        elif call.data == "start_schedule":
            self.__send_setup_schedule_message(call, chat_id, schedule_data)
  
    def remove_flow(self, call): 
        self.bot.answer_callback_query(call.id)
        list = self.cron.get_cron_list()
        ids = [item['id'] for item in list['data']]
        for id in ids:
            self.cron.cron_delete(id)
        
        self.bot.send_message(call.message.chat.id, "Расписание удалено.")
        self.commands.create_commands(call.message, False)
    
    def get_flow_count(self) -> int:
        list = self.cron.get_cron_list()
        ids = [item['id'] for item in list['data']]
        return len(ids)
    
    def __process_time_input(self, message, schedule_data: SchedulerData):
        chat_id = message.chat.id
        try:
            now = datetime.now()
            input_time = datetime.strptime(message.text, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            # Если введённое время уже прошло, берем время следующего дня
            if input_time < now:
                input_time += timedelta(days=1)
            schedule_data.time = input_time
            self.bot.send_message(chat_id, f"Время установлено на {input_time.strftime('%H:%M')}.")
            self.commands.add_set_interval(message)
        except Exception as e:
            self.bot.send_message(chat_id, f"Ошибка ввода времени: {e}. Попробуйте снова.")

    def __process_interval_input(self, message, schedule_data: SchedulerData):
        chat_id = message.chat.id
        try:
            interval = int(message.text)
            cronjob_builder = CronJobBuilder()
            
            schedule_data.frequency = cronjob_builder.build_cron_expression(interval)
            schedule_data.interval = interval

            self.bot.send_message(chat_id, f"Интервал публикаций установлен на {interval} минут.")
            self.commands.add_start_scheduler(message)
        except Exception as e:
            self.bot.send_message(chat_id, f"Ошибка ввода интервала: {e}. Попробуйте снова.")

    def __send_setup_time_message(self, call, chat_id, schedule_data: SchedulerData):
        self.bot.answer_callback_query(call.id)
        msg = self.bot.send_message(chat_id, "Введите время для первой публикации в формате ЧЧ:ММ (например, 15:30):")
        self.bot.register_next_step_handler(msg, self.__process_time_input, schedule_data)

    def __send_setup_interval_message(self, call, chat_id, schedule_data: SchedulerData):
        self.bot.answer_callback_query(call.id)
        msg = self.bot.send_message(chat_id, "Введите интервал публикаций в минутах (например, 60):")
        self.bot.register_next_step_handler(msg, self.__process_interval_input, schedule_data)

    def __send_setup_schedule_message(self, call, chat_id, schedule_data: SchedulerData):
        self.bot.answer_callback_query(call.id)
        if schedule_data.time == None or schedule_data.frequency == None:
            self.bot.send_message(chat_id, "Сначала установите и время, и интервал публикаций.")
            return

        scheduled_time = schedule_data.time
        frequency = schedule_data.frequency
        interval = schedule_data.interval
        self.cron.cron_create(self.callback_url, scheduled_time, frequency, self.data.to_dict())
        self.bot.send_message(chat_id, f"Расписание установлено.\nПервая публикация в {scheduled_time.strftime('%H:%M')}, затем каждые {interval} минут.")    
     