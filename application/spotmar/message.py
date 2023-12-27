from itertools import groupby
from typing import List

from more_itertools import consume

from application import confirmation as cfm
from .trade import Trade

PRODUCT = cfm.SPOT_MAR


def reuter(trades: List[Trade]):
    grouped_trades = by_entity_rate(trades)
    grouped_messages = {}
    for entity, rate_trades in grouped_trades.items():
        messages = []
        template = cfm.get_reuter_template(PRODUCT, entity)
        for rate, _trades in rate_trades.items():
            consume(
                messages.append(
                    f"""
                    {template.render_header(**t.message_dict(entity))}
                    {template.render_body(**t.message_dict(entity))}
                    {template.render_tail(**t.message_dict(entity))}
                    """
                )
                for t in _trades
            )
        grouped_messages[entity] = messages
    return grouped_messages


def by_entity_rate(trades: List[Trade]):
    grouped_trades = {}
    for t in trades:
        _trades = grouped_trades.get(t.bid, [])
        _trades.append(t)
        grouped_trades[t.bid] = _trades
        _trades = grouped_trades.get(t.offer, [])
        _trades.append(t)
        grouped_trades[t.offer] = _trades
    return {
        entity: {r: list(t) for r, t in groupby(_trades, lambda x: x.rate)}
        for entity, _trades in grouped_trades.items()
    }
