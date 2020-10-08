from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from utils.prepaudio import get_large_audio_transcription
from utils.analyzetext import determine_tense_input
from utils.TranslateOutput import get_translation
from utils.misc import predict, open_model, User_Directory, enumerated_filename
from pydub import AudioSegment
import warnings
import os
warnings.filterwarnings('ignore')
PORT = int(os.environ.get('PORT', 5000))
TOKEN = '1392640204:AAFLxDf3Q8AgAmQNL85Bfg3-dD1hJOOypmY'
model = open_model()
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi, welcome to Unbias Translator ! \n'
                              'Please record an audio to the chat and get translated to hebrew '
                              'text in seconds')


# def help(update, context):
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Help!')


# def echo(update, context):
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)


# def error(update, context):
#     """Log Errors caused by Updates."""
#     logger.warning('Update "%s" caused error "%s"', update, context.error)


def invoke_pipeline(audiofile):
    pred = predict(audiofile, model=model)
    text = get_large_audio_transcription(audiofile)
    split_sentence = determine_tense_input(text)
    res = get_translation(split_sentence, pred)
    return res


def convert_ogg_to_wav(path, wav_path):
    """create wav file"""
    ogg_version = AudioSegment.from_ogg(path)
    ogg_version.export(wav_path, format='wav')


def delete_files(path, wav_path):
    """delete used files"""
    if os.path.isfile(path) or os.path.islink(path):
        os.unlink(path)
    if os.path.isfile(wav_path) or os.path.islink(wav_path):
        os.unlink(wav_path)


def voice_handler(update: Update, context: CallbackContext):
    """Get user unique name and create a destination folder on server"""
    user_name = str(update.message.chat_id) + '_' + str(update.message.from_user.first_name)
    user_directory = User_Directory(user_name)
    '''get file details from telegram and download to the user's specific folder'''
    file_id = update["message"]["voice"]["file_id"]
    file = context.bot.getFile(file_id)
    path = os.path.join(user_directory, enumerated_filename(user_directory) + '.ogg')
    file.download(path)
    '''convert to a wave file'''
    wav_path = path.split('.')[0] + '.wav'
    convert_ogg_to_wav(path, wav_path)
    '''start pipeline:'''
    res = ''
    try:
        res = invoke_pipeline(wav_path)
    except Exception as E:
        res = E
    '''return response to user'''
    try:
        if res == '':
            res = 'audio was empty or vocals were too low, please try again'
        context.bot.send_message(chat_id=update.message.chat_id, text=res)
        '''delete used files'''
        delete_files(path, wav_path)
    except Exception:
        '''delete used files'''
        delete_files(path, wav_path)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", help))
    
    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.voice, voice_handler))
    # log all errors
    # dp.add_error_handler(error)

    '''Start the Bot locally:'''
    updater.start_polling()

    '''OR'''

    '''Start the bot on Heroku: (problem with deployment due to size of slug - allowed 500, this is currently 630) '''
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TOKEN)
    # updater.bot.setWebhook('https://aqueous-garden-12251.herokuapp.com/' + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()