from app import db
from app.models import User, DeliveryTask, Role

def init_db():
    """Initiates the DB with set of users and tasks"""

    sm1 = User('John Sena', 'john@cena.com', 'johncena', Role.STORE_MANAGER)
    sm2 = User('Tony Stark', 'tony@stark.com', 'tonystark', Role.STORE_MANAGER)
    da1 = User('Agent Vinod', 'agent@vinod.com', 'agentvinod', Role.DELIVERY_AGENT)
    da2 = User('Flash Superhero', 'flash@superhero.com', 'flashsuperhero', Role.DELIVERY_AGENT)
    da3 = User('Spider Man', 'spider@man.com', 'spiderman', Role.DELIVERY_AGENT)

    task1 = sm1.create_delivery_task('Hot Chicken Kathi Roll', 'Down Town', 'medium')
    task2 = sm1.create_delivery_task('Mutton Biryani', 'Home', 'high')
    task3 = sm2.create_delivery_task('Gulab Jamun, Phirni', 'Home', 'low')

    da1.accept_task(task1)

    db.session.add_all([sm1, sm2, da1, da2, da3])
    db.session.commit()


if __name__ == "__main__":
    init_db()