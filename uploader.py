import requests


class TelegramUploader:
    def __init__(self, bot_token):
        self.bot_token = bot_token

    def uploadFile(self, chat_id, path):
        url = "https://api.telegram.org/bot" + self.bot_token + "/sendaudio"
        files = {"audio": open(path, "rb")}
        data = {"chat_id": chat_id}

        response = requests.post(url, data=data, files=files)
        if response.status_code != requests.codes.ok:
            print("Status unerwarteterweise gleich " + response.status_code)

        result = response.json()
        print(result)


if __name__ == '__main__':
    path = '<path-to-file>'
    chat_id = '<chat-id>'
    bot_token = '<bot-token>'

    uploader = TelegramUploader(bot_token)
    uploader.uploadFile(chat_id, path)
