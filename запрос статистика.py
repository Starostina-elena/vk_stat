import os

import vk_api
from flask import Flask, render_template

from my_data import data

app = Flask(__name__)


@app.route('/vk_stat/<int:group_id>')
def main(group_id):
    login, password = data['LOGIN'], data['PASSWORD']
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    stat = vk.stats.get(group_id=group_id, fields='activity', intervals_count=10)

    stat_data = {'activities': {'likes': 0, 'comments': 0, 'subscribed': 0},
                 'ages': {'12-18': 0, '18-21': 0, '21-24': 0, '24-27': 0, '27-30': 0, '30-35': 0, '35-45': 0,
                          '45-100': 0},
                 'cities': {}}

    for i in stat:
        if 'activity' in i:
            if 'likes' in i['activity']:
                stat_data['activities']['likes'] = i['activity']['likes']
            if 'comments' in i['activity']:
                stat_data['activities']['comments'] = i['activity']['comments']
            if 'subscribed' in i['activity']:
                stat_data['activities']['subscribed'] = i['activity']['subscribed']
        try:
            for j in i['visitors']['age']:
                stat_data['ages'][j['value']] = j['count']
        except KeyError as e:
            print(e)
        try:
            for j in i['visitors']['cities']:
                stat_data['cities'][j['name']] = j['count']
        except KeyError as e:
            print(e)

    print(stat_data)

    return render_template('index.html', stat_data=stat_data, colors=[('#A85BAD', '#D18AD6'), ('#5DB292', '#8BD9BB'), ('#FFAA00', '#FFBF40')])


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
