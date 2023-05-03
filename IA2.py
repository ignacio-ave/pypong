import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

def inicializar_actor():
    model = Sequential()
    model.add(Dense(64, input_dim=6, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(2, activation='linear'))
    model.compile(loss='mse', optimizer=Adam(lr=0.001))
    return model

def inicializar_critic():
    model = Sequential()
    model.add(Dense(64, input_dim=6, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer=Adam(lr=0.001))
    return model

def obtener_estado(paleta, pelota):
    return np.array([paleta.x, paleta.y, paleta.width, paleta.height, pelota.x, pelota.y])

def calcular_recompensa(estado_actual, estado_siguiente):
    distancia_actual = abs(estado_actual[1] - estado_actual[5])
    distancia_siguiente = abs(estado_siguiente[1] - estado_siguiente[5])
    return 1 if distancia_siguiente < distancia_actual else -1

def actualizar_actor_critic_globales(actor_local, critic_local, actor_global, critic_global):
    actor_global.set_weights(actor_local.get_weights())
    critic_global.set_weights(critic_local.get_weights())

class Trabajador:
    def __init__(self, paleta, actor_global, critic_global):
        self.paleta = paleta
        self.actor_local = inicializar_actor()
        self.critic_local = inicializar_critic()
        self.actor_global = actor_global
        self.critic_global = critic_global

    def actualizar(self, paleta, pelota):
        estado_actual = obtener_estado(paleta, pelota)
        accion = np.argmax(self.actor_local.predict(estado_actual.reshape(1, -1)))

        paleta.mover(accion)

        estado_siguiente = obtener_estado(paleta, pelota)
        recompensa = calcular_recompensa(estado_actual, estado_siguiente)

        target_action_value = recompensa + 0.99 * self.critic_local.predict(estado_siguiente.reshape(1, -1))

        self.critic_local.fit(estado_actual.reshape(1, -1), target_action_value, verbose=0)

        actor_target = self.actor_local.predict(estado_actual.reshape(1, -1))

        actor_target[0][accion] = target_action_value
        self.actor_local.fit(estado_actual.reshape(1, -1), actor_target, verbose=0)

        actualizar_actor_critic_globales(self.actor_local, self.critic_local, self.actor_global, self.critic_global)
