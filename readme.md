# Получение токена
1. Открыть вкладку барузера
1. Запустить DevTools
1. На вкладке Network выставить эмуляцию низкоскоростной сети 3G (что бы успеть отловить хитрый запрос с токеном в хеше)
1. Выполнить запрос на вкладке: https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d
1. Если эмуляция низкоскоростной сети 3G включена, то вы успеете увидеть редирект на URL вида https://music.yandex.ru/#access_token=XXXXXXXXXXXXXXXX-YYYYYYY&token_type=bearer&expires_in=24199145
1. Останавливаем загрузку и копирует значение `access_token`
