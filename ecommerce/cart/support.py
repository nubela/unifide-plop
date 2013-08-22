from flask import request, session, jsonify


def _post_or_get(key, defa=None):
    return request.form.get(key, request.args.get(key, defa))


def add_to_cart():
    cart_name = _post_or_get("cart_name")
    item_id = _post_or_get("item_id")
    qty = _post_or_get("quantity", 1)
    if None in (cart_name, item_id, qty):
        return jsonify({
            "status": "error",
        })

    if cart_name not in session:
        session[cart_name] = {}
    if item_id in session[cart_name]:
        session[cart_name][item_id] += qty
    else:
        session[cart_name][item_id] = qty

    return jsonify({
        "status": "ok",
        "cart": session[cart_name],
    })


def rm_from_cart():
    cart_name = _post_or_get("cart_name")
    item_id = _post_or_get("item_id")
    if None in (cart_name, item_id):
        return jsonify({
            "status": "error",
        })

    if cart_name not in session:
        session[cart_name] = {}

    del session[cart_name][item_id]
    return jsonify({
        "status": "ok",
        "cart": session[cart_name],
    })