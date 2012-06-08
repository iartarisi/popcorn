from functools import wraps
from flask import request, jsonify, render_template


def dump_datetime(value):
    """Serialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json',
                                               'text/html'])
    return best == 'application/json' and (request.accept_mimetypes[best] >
                                    request.accept_mimetypes['text/html'])


def render(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            render_type = request_wants_json()
            if render_type:
                return jsonify(ctx)
            return render_template(template, **ctx)
        return decorated_function
    return decorator
