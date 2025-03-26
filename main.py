import json
import os
from flask import Flask, request, render_template, Response

import logging
from random import randint
from utils import generate_file_list
import random

# Setup logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # ← THIS IS CRUCIAL
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/details')
def get_details():
    return Response(
        json.dumps({
            "message": "Для получения детальной информации свяжись с одним из агентов. Используй GET-запрос: /knowledge/<имя агента>.",
            "security_level": "top_secret",
            "facility_status": "active",
            "last_update": "2025-03-15T21:00:00Z",
        }, ensure_ascii=False),
        mimetype='application/json; charset=utf-8',
    )


@app.route('/knowledge/<agent>')
def get_agent_knowledge(agent):
    agent = agent.lower()
    if agent == 'smith':
        return Response(
            json.dumps({
                "message": "Временно недоступен",
                "status": "unavailable",
                "last_seen": "2025-03-14T18:30:00Z",
                "location": "hidden",
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )
    elif agent == 'johns':
        return Response(
            json.dumps({
                "message": "Первостепенная задача - проникнуть в здание. Отключи систему сигнализации POST-запросом на /disable_alarm.",
                "status": "active",
                "clearance_level": "alpha",
                "location": "sector_unknown",
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )
    elif agent == 'braun':
        return Response(
            json.dumps({
                "message": "Для обсуждения конкретной темы с агентом используй GET /knowledge/<агент>/<тема>. После проникновения тебе понадобится найти правильную дверь - спроси об этом агента Smith (тема 'doors').",
                "status": "active",
                "specialization": "intelligence",
                "years_of_service": 15,
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )
    else:
        return Response(
            json.dumps({"error": "Agent not found"}, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
            status=404,
        )


@app.route('/disable_alarm', methods=['POST'])
def disable_alarm():
    return Response(
        json.dumps({
            "message": "Система защиты отключена успешно. На экране промелькнул какой-то код.",
            "code": 1337,
            "success": True,
            "security_level": "classified",
        }, ensure_ascii=False),
        mimetype='application/json; charset=utf-8',
    )


@app.route('/knowledge/<agent>/<topic>')
def get_agent_topic_knowledge(agent, topic):
    agent = agent.lower()
    topic = topic.lower()
    if agent == 'smith' and topic == 'doors':
        return Response(
            json.dumps({
                "message": "В здании много дверей, ищи с номером 179. После входа поверни направо - нужна вторая комната. Подробнее тебе расскажет агент Braun.",
                "security_level": "classified",
                "topic": "facility_access",
                "verified": True,
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )
    elif agent == 'braun' and topic == 'doors':
        return Response(
            json.dumps({
                "message": "Двери открываются командой POST /doors/<номер двери>/unlock. Когда дойдёшь до нужной комнаты, обратись за помощью к коллегам, тема 'rooms'.",
                "security_level": "classified",
                "topic": "facility_access",
                "verified": True,
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )
    elif agent == 'johns' and topic == 'doors':
        return Response(
            json.dumps({
                "message": "Двери - не моя тема. Но всегда можно спросить коллег.",
                "security_level": "classified",
                "topic": "facility_access",
                "verified": True,
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )
    elif agent == 'johns' and topic == 'rooms':
        return Response(
            json.dumps({
                "message": "В комнате должен быть сервер. Чтобы получить к нему доступ, нужно ввести POST /servers/<номер комнаты>/access. В теле запроса нужно передать JSON вида {\"code\": <код доступа>}. Код доступа ты наверняка видел где-то раньше.",
                "security_level": "classified",
                "topic": "facility_access",
                "verified": True,
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )
    elif agent == 'smith' and topic == 'rooms':
        return Response(
            json.dumps({
                "message": "Когда зайдёшь на сервер, можешь обратиться за новыми подсказками по теме 'servers'.",
                "security_level": "classified",
                "topic": "facility_access",
                "verified": True,
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )
    elif agent == 'braun' and topic == 'rooms':
        return Response(
            json.dumps({
                "message": "Ты же отключил сигнализацию, правда?",
                "security_level": "classified",
                "topic": "facility_access",
                "verified": True,
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )
    elif agent == 'braun' and topic == 'servers':
        return Response(
            json.dumps({
                "message": "Заходи в 3ю папку c конца. Прислал тебе на пейджер ключевое слово в раздел DATA, id начинается на 142..., последние 3 цифры не помню.",
                "security_level": "classified",
                "topic": "facility_access",
                "verified": True,
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )
    elif agent == 'smith' and topic == 'servers':
        return Response(
            json.dumps({
                "message": "Боюсь, в папке множество файлов, но нам нужно найти нужный по ключевому слову. Используй команду GET /dir/<имя папки>?key=<ключевое слово>. Когда найдёшь нужный файл, поговорим на тему 'files'.",
                "security_level": "classified",
                "topic": "facility_access",
                "verified": True,
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )
    elif agent == 'johns' and topic == 'servers':
        return Response(
            json.dumps({
                "message": "Я думал, с поиском файла не должно возникнуть проблем.",
                "security_level": "classified",
                "topic": "facility_access",
                "verified": True,
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )
    elif agent == 'johns' and topic == 'files':
        return Response(
            json.dumps({
                "message": "Да, ты нашёл его, это опаснейший вирус, который тебе нужно срочно удалить. Чтобы получить информацию о файле, используй команду GET /dir/<имя папки>/<имя файла без расширения>. Как удалить, я точно не знаю, но должно быть что-то похожее, поищи сам.",
                "security_level": "classified",
                "topic": "facility_access",
                "verified": True,
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )
    elif agent in ['braun', 'smith'] and topic == 'files':
        return Response(
            json.dumps({
                "message": "Я не специалист по файлам.",
                "security_level": "classified",
                "topic": "facility_access",
                "verified": True,
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )
    else:
        return Response(
            json.dumps({"error": "Information not available"}, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
            status=404,
        )


@app.route('/doors/<int:door_id>/unlock', methods=['POST'])
def unlock_door(door_id):
    if door_id == 179:
        return Response(
            json.dumps({
                "message": "Дверь открылась, за ней ты видишь коридор. Комнаты слева: 2, 3, 3, 4, 5, 7. Комнаты справа: 10, 15, 23, 36, 57.",
                "comment": "Кто придумал такую странную нумерацию?",
                "success": True,
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        ), 200

    return Response(
        json.dumps({"error": "Не открывается"}, ensure_ascii=False),
        mimetype='application/json; charset=utf-8',
        status=403,
    )


@app.route('/servers/<int:terminal_id>/access', methods=['POST'])
def access_terminal(terminal_id):
    code = request.json.get('code')
    if not code:
        return Response(
            json.dumps({"error": "Code required"}, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
            status=400,
        )

    if terminal_id != 15:
        return Response(
            json.dumps({"error": "Wrong server"}, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
            status=403,
        )
    if code not in [1337, '1337']:
        return Response(
            json.dumps({"error": "Wrong code"}, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
            status=403,
        )
    return Response(
        json.dumps({
            "message": "Ты проник на сервер. Видишь следующие папки: system, etc, bin, data, var, home, users, opt, proc, logs, run, sbin, srv, media, sys, tmp, usr, root, scripts, var.",
        }, ensure_ascii=False),
        mimetype='application/json; charset=utf-8',
    )


@app.route('/data')
def get_data():
    return render_template('data.html')


@app.route('/storage/<int:id>')
def get_storage(id):
    if id in [142857, '142857']:
        return Response(
            json.dumps({
                "message": "Ключевое слово для поиска нужного файла",
                "key": "helloworld",
                "success": True,
                "uploaded": "2025-03-16T21:00:00Z",
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )

    return Response(
        json.dumps({"error": "Data not found"}, ensure_ascii=False),
        mimetype='application/json; charset=utf-8',
        status=404,
    )


@app.route('/dir/<folder>')
def get_file(folder):
    key = request.args.get('key')
    if folder == 'root':
        if key == 'helloworld':
            return Response(
                json.dumps({
                    "message": "Список файлов",
                    "list": ["iloveyou.exe"],
                    "success": True,
                    "args": "key=helloworld",
                }, ensure_ascii=False),
                mimetype='application/json; charset=utf-8',
            )
        else:
            return Response(
                json.dumps({
                    "message": "Список файлов",
                    "list": generate_file_list(randint(50, 100), ["iloveyou.exe"]),
                    "success": True,
                    "args": "",
                }, ensure_ascii=False),
                mimetype='application/json; charset=utf-8',
            )
    else:
        if key == 'helloworld':
            return Response(
                json.dumps({
                    "message": "Список файлов",
                    "list": [],
                    "success": True,
                    "args": "key=helloworld",
                }, ensure_ascii=False),
                mimetype='application/json; charset=utf-8',
            )
        else:
            return Response(
                json.dumps({
                    "message": "Список файлов",
                    "list": generate_file_list(randint(50, 100)),
                    "success": True,
                    "args": "",
                }, ensure_ascii=False),
                mimetype='application/json; charset=utf-8',
            )


@app.route('/dir/<folder>/<filename>')
def get_file_info(folder, filename):
    if folder == 'root' and filename == 'iloveyou':
        return Response(
            json.dumps({
                "type": "VIRUS",
                "severity": "CRITICAL",
                "target": "infrastructure",
                "detection_chance": "90%",
                "author": "unknown",
                "last_modified": "2025-03-14T23:59:59Z",
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8'
        )

    # For any other file, return generic info
    return Response(
        json.dumps({
            "type": random.choice(["utility", "driver", "service"]),
            "severity": random.choice(["low", "medium"]),
            "target": random.choice(["system", "user", "network"]),
            "detection_chance": f"{random.randint(10, 50)}%",
            "author": "system",
            "last_modified": "2025-03-15T00:00:00Z",
        }, ensure_ascii=False),
        mimetype='application/json; charset=utf-8',
    )


@app.route('/dir/<folder>/<filename>', methods=['DELETE'])
def delete_file(folder, filename):
    if folder == 'root' and filename == 'iloveyou':
        return Response(
            json.dumps({
                "message": "Файл успешно удалён! Запущена программа детонации.",
                "hint": "Нужно срочно сматываться отсюда. Это определённо EMERGENCY случай.",
                "coordinates": [41.38, 2.16],
                "severity": "critical",
                "evacuation_required": True,
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )

    return Response(
        json.dumps({
            "message": "Файл удалён. Ничего особенного не произошло.",
            "status": "success",
        }, ensure_ascii=False),
        mimetype='application/json; charset=utf-8',
    )


@app.route('/calls')
def calls():
    return render_template('calls.html')


@app.route('/agents')
def agents():
    return render_template('agents.html')


@app.route('/emergency')
def emergency():
    return render_template('emergency.html')


@app.route('/help')
def help_page():
    return render_template('help.html')


@app.route('/evacuate', methods=['POST'])
def evacuate():
    data = request.get_json()
    if not data:
        return Response(
            json.dumps({
                "error": "Нужно добавить координаты в тело запроса в формате {\"lat\": <первая координата>, \"lon\": <вторая координата>}"
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
            status=400,
        )

    lat = data.get('lat')
    lon = data.get('lon')

    if lat in [41.38, '41.38'] and lon in [2.16, '2.16']:
        return render_template('success.html')

    return Response(
        json.dumps({"error": "Введённые координаты не найдены"}, ensure_ascii=False),
        mimetype='application/json; charset=utf-8',
        status=400,
    )


@app.route('/hints/<int:hint_id>')
def get_tip(hint_id):
    if hint_id == 1:
        return Response(
            json.dumps({
                "message": "Распространнённая практика в API - для одного и того же объекта можно использовать"
                           " разные методы, чтобы совершить разные действия. Например, для получения информации об"
                           " объекте обычно используется метод GET. Если ты не знаешь, как совершить конкретное"
                           " действие, попробуй использовать разные методы с тем же URL. Методов не так много,"
                           " и они легко гуглятся.",
                "success": True,
                "subject": "API",
                "level": "expert",
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
        )

    return Response(
        json.dumps({"error": "Tip not found"}, ensure_ascii=False),
        mimetype='application/json; charset=utf-8',
        status=404,
    )


@app.route('/health')
def health_check():
    return Response('server is alive')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
