import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

class Memory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def store(self, transition):
        self.memory.append(transition)
        if len(self.memory) > self.capacity:
            self.memory.pop(0)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

def inicializar_actor():
    model = Sequential()
    model.add(Dense(128, input_dim=6, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(2, activation='linear'))
    model.compile(loss='mse', optimizer=Adam(lr=0.0005))
    return model

def inicializar_critic():
    model = Sequential()
    model.add(Dense(128, input_dim=6, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer=Adam(lr=0.0005))
    return model

def inicializar_memory():
    return Memory(capacity=20000)

def obtener_estado(paleta, pelota):
    return np.array([paleta.x, paleta.y, paleta.width, paleta.height, pelota.x, pelota.y])

def calcular_recompensa(estado_actual, estado_siguiente):
    distancia_actual = abs(estado_actual[1] - estado_actual[5])
    distancia_siguiente = abs(estado_siguiente[1] - estado_siguiente[5])
    return 1 if distancia_siguiente < distancia_actual else -1

def entrenar_actor_critic(actor, critic, batch, discount_factor=0.99):
    for estado, accion, recompensa, estado_siguiente in batch:
        target_action_value = recompensa + discount_factor * critic.predict(estado_siguiente.reshape(1, -1))
        critic.fit(estado.reshape(1, -1), target_action_value, verbose=0)

        actor_target = actor.predict(estado.reshape(1, -1))
        actor_target[0][accion] = target_action_value
        actor.fit(estado.reshape(1, -1), actor_target, verbose=0)


class Jugador:
    def __init__(self, paleta):
        self.paleta = paleta
        self.actor = inicializar_actor()
        self.critic = inicializar_critic()
        self.memory = inicializar_memory()

    def actualizar(self, paleta, pelota):
        estado_actual = obtener_estado(paleta, pelota)
        accion = np.argmax(self.actor.predict(estado_actual.reshape(1, -1)))
        paleta.mover(accion)

        estado_siguiente = obtener_estado(paleta, pelota)
        recompensa = calcular_recompensa(estado_actual, estado_siguiente)

        self.memory.store((estado_actual, accion, recompensa, estado_siguiente))

        if len(self.memory.memory) >= 64:
            batch = self.memory.sample(64)
            entrenar_actor_critic(self.actor, self.critic, batch)