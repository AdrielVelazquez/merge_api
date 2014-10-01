from flask import request, Blueprint

from app import db

quiz = Blueprint('quiz', __name__, url_prefix='/quiz')


@quiz.route("/next/<stream>", methods=['GET'])
def stream_list(stream):
    choice = stream.capitalize()
    choice_doc = db.get(choice)

    try:
        current_idx = choice_doc["idx"]
        last_stream = None
        if current_idx > 0:
            last_stream = choice_doc["list"][current_idx - 1]
        current_stream = choice_doc["list"][current_idx]
        choice_doc["idx"] += 1
        db.save(choice_doc)
    except:
        choice_doc["idx"] = 0
        db.save(choice_doc)
        return {"Warning": "End of List Reached Reseting Counter"}
    return {"last": last_stream, "current": current_stream, "stream": choice}


@quiz.route("/merge/", methods=['GET'])
def merge_list():
    named_streams = []
    for stream in request.args:
        stream_name = request.args[stream]
        if not db.get(stream_name):
            return {"Error": "Stream {} Doesn't Exist".format(stream_name)}
        named_streams.append(stream_name)
    unique_name = ''.join(sorted(named_streams))
    merge_doc = db.get('merge')
    if unique_name in merge_doc:
        try:
            current_idx = merge_doc[unique_name]['idx']
            m_list = merge_doc[unique_name]['list']
            last_stream = None
            if current_idx > 0:
                last_stream = m_list[current_idx - 1]
            m_list = merge_doc[unique_name]['list']
            merge_doc[unique_name]['idx'] += 1
            db.save(merge_doc)
            return {"last": last_stream, "current": m_list[current_idx]}
        except:
            merge_doc[unique_name]['idx'] = 0
            db.save(merge_doc)
            return {"Warning": "End of Merged List Reached Starting Over"}
    else:
        sorted_master = []
        for name in named_streams:
            stream_list = db.get(name)['list']
            sorted_master.extend(stream_list)
        new_sorted_master = sorted(sorted_master)
        merge_doc[unique_name] = {"list": new_sorted_master, "idx": 1}
        db.save(merge_doc)
        return {"last": None, "current": new_sorted_master[0]}