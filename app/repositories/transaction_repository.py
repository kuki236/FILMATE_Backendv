from sqlalchemy.orm import Session

from app.models.reservation import Reserva
from app.models.user import Usuario
from app.models.showtime import Funcion
from app.models.movie import Pelicula
from app.models.room import Sala


def list_transactions(db: Session):

    results = (
        db.query(
            Reserva.id_reserva,
            Usuario.nombres,
            Usuario.apellidos,
            Pelicula.titulo,
            Sala.nombre,
            Reserva.monto_total,
            Reserva.estado_pago,
            Reserva.metodo_pago
        )
        .join(Usuario, Usuario.id_usuario == Reserva.id_usuario)
        .join(Funcion, Funcion.id_funcion == Reserva.id_funcion)
        .join(Pelicula, Pelicula.id_pelicula == Funcion.id_pelicula)
        .join(Sala, Sala.id_sala == Funcion.id_sala)
        .all()
    )

    transactions = []

    for row in results:
        transactions.append({
            "id_reserva": row[0],
            "cliente": f"{row[1]} {row[2]}",
            "pelicula": row[3],
            "sala": row[4],
            "monto_total": row[5],
            "estado_pago": row[6],
            "metodo_pago": row[7]
        })

    return transactions


def get_transaction_detail(
    db: Session,
    reservation_id: int
):

    row = (
        db.query(
            Reserva,
            Usuario,
            Funcion,
            Pelicula,
            Sala
        )
        .join(Usuario, Usuario.id_usuario == Reserva.id_usuario)
        .join(Funcion, Funcion.id_funcion == Reserva.id_funcion)
        .join(Pelicula, Pelicula.id_pelicula == Funcion.id_pelicula)
        .join(Sala, Sala.id_sala == Funcion.id_sala)
        .filter(Reserva.id_reserva == reservation_id)
        .first()
    )

    if not row:
        return None

    reserva, usuario, funcion, pelicula, sala = row

    return {
        "id_reserva": reserva.id_reserva,

        "cliente": f"{usuario.nombres} {usuario.apellidos}",
        "correo": usuario.correo,

        "pelicula": pelicula.titulo,
        "sala": sala.nombre,

        "monto_subtotal": reserva.monto_subtotal,
        "descuento_aplicado": reserva.descuento_aplicado,
        "monto_total": reserva.monto_total,

        "estado_pago": reserva.estado_pago,
        "metodo_pago": reserva.metodo_pago,
        "transaccion_id": reserva.transaccion_id
    }