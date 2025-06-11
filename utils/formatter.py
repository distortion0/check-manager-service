def format_check_text(check, width: int = 32) -> str:
    """
    Format a check object into a nicely centered and aligned text receipt.

    Args:
        check: Check object containing products, totals, payment info, and timestamps.
        width (int): Total line width for formatting (default=32) (gt=10, le=80)

    Returns:
        str: Formatted text receipt as a string.
    """
    def center(text: str) -> str:
        return text.center(width)

    def line(char='='):
        return char * width

    def format_product(p):
        total = p.quantity * p.price
        lines = []
        qty_price = f"{p.quantity:.2f} x {p.price:,.2f}"
        lines.append(qty_price)
        lines.append(p.name.ljust(width - len(f"{total:,.2f}")) + f"{total:,.2f}")
        return "\n".join(lines)

    lines = [
        center("ФОП Джонсонюк Борис"),
        line(),
    ]

    for p in check.products:
        lines.append(format_product(p))
        lines.append('-' * width)

    lines.append(line())
    lines.append("СУМА".ljust(width - len(f"{check.total:,.2f}")) + f"{check.total:,.2f}")
    lines.append(f"{check.payment_type.capitalize()}".ljust(
        width - len(f"{check.payment_amount:,.2f}")) + f"{check.payment_amount:,.2f}")
    change = check.payment_amount - check.total
    lines.append("Решта".ljust(width - len(f"{change:,.2f}")) + f"{change:,.2f}")
    lines.append(line())
    lines.append(center(check.created_at.strftime("%d.%m.%Y %H:%M")))
    lines.append(center("Дякуємо за покупку!"))

    return "\n".join(lines)
